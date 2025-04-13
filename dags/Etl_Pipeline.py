from airflow.decorators import task, dag
from airflow.models.baseoperator import chain
from airflow.providers.http.sensors.http import HttpSensor, HttpHook
from datetime import datetime
from src.config import *
from src.constants import *
from rich import print
import os
import json


@dag(
    start_date=datetime(2025, 4, 9),
    schedule="@daily",
    catchup=False,
    tags=["ETL_DAG", "POSTGRES"],
)
def CollegeDataPipelineDag():
    check_api_health = HttpSensor(
        task_id="check_api_health",
        endpoint="schools",
        http_conn_id="college_scorecard_api",
        method="GET",
        request_params=PARAMS,
        response_check=lambda response: response.status_code == 200,
        poke_interval=60,
        timeout=300,
        mode="poke",
    )

    @task
    def MakeConnection():
        hook_obj = PostHook()
        try:
            hook = hook_obj.CreateHook(conn_id=POSTGRES_CONN_ID)
            hook.run(CREATION_QUERY)
            print("Connection and Table Created")
        except RuntimeError as e:
            print(e)
            return None

    @task
    def ExtractData():
        try:
            http_hook = HttpHook(http_conn_id="college_scorecard_api", method="GET")
            response = http_hook.run(endpoint="schools", data=PARAMS)
            results = response.json()
            return results
        except Exception as e:
            print(e)

    @task
    def TransformData(DataDict: dict):
        data_list = DataDict
        for uni_data in data_list['results']:
            mapped_data = {
                "student_size": uni_data.get("latest.student.size"),
                "admission_rate": uni_data.get(
                    "latest.admissions.admission_rate.overall"
                ),
                "tuition_in_state": uni_data.get("latest.cost.tuition.in_state"),
                "tuition_out_of_state": uni_data.get(
                    "latest.cost.tuition.out_of_state"
                ),
                "earnings": uni_data.get("latest.earnings.10_yrs_after_entry.median"),
                "completion_rate_150percent": None,  # This doesn't appear to have a direct mapping
                "completion_rate_4yr": uni_data.get(
                    "latest.completion.rate_suppressed.four_year"
                ),
                "completion_rate_4yr_200percent": uni_data.get(
                    "latest.completion.rate_suppressed.four_year_200percent"
                ),
                "completion_rate_4yr_100_pooled": uni_data.get(
                    "latest.completion.rate_suppressed.four_year_100_pooled"
                ),
                "completion_rate_consumer_median": uni_data.get(
                    "latest.completion.rate_suppressed.consumer.median_by_pred_degree"
                ),
                "completion_rate_consumer_overall": uni_data.get(
                    "latest.completion.rate_suppressed.consumer.overall_median"
                ),
                "completion_rate_pell_150_pooled": uni_data.get(
                    "latest.completion.rate_suppressed_pell.four_year_150_pooled"
                ),
                "completion_rate_overall": uni_data.get(
                    "latest.completion.rate_suppressed.overall"
                ),
                "school_name": uni_data.get("school.name"),
                "school_city": uni_data.get("school.city"),
                "school_state": uni_data.get("school.state"),
                "school_id": uni_data.get("id"),
            }

        return mapped_data

    @task
    def LoadData(mapped_data):
        insert_sql = INSERTION_QUERY
        postgres_hook = PostHook().CreateHook(conn_id=POSTGRES_CONN_ID)
        try:
            # Execute insert for each record
            postgres_hook.run(insert_sql, parameters=mapped_data)
            print(f"Successfully inserted data for {mapped_data['school_name']}")
        except Exception as e:
            print(
                f"Error inserting data for school ID {mapped_data['school_id']}: {str(e)}"
            )

    hook = MakeConnection()
    data = ExtractData()
    transformed_data = TransformData(data)
    loading_data = LoadData(transformed_data)

    chain(hook, check_api_health, data, transformed_data, loading_data)


my_dag = CollegeDataPipelineDag()
