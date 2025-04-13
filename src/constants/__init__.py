from dotenv import load_dotenv
import os
from airflow.providers.postgres.hooks.postgres import PostgresHook

load_dotenv()
API_ENDPOINT = f"""
https://api.data.gov/ed/collegescorecard/v1/schools?api_key={os.getenv("API_KEY")}&id=123961,193900,190150,167358,211440,145637,190415,228787,170976,104151
&fields=id,school.name,school.city,school.state,latest.student.size,
latest.admissions.admission_rate.overall,latest.cost.tuition.in_state,
latest.cost.tuition.out_of_state,latest.completion.rate,
latest.earnings.10_yrs_after_entry.median
"""
POSTGRES_CONN_ID = "postgres_conn"


CREATION_QUERY = """

CREATE TABLE IF NOT EXISTS university_data (
    id SERIAL PRIMARY KEY,
    student_size INTEGER,
    admission_rate NUMERIC(5,4),
    tuition_in_state INTEGER,
    tuition_out_of_state INTEGER,
    earnings_10yrs_after_entry INTEGER,
    completion_rate_150percent NUMERIC(5,4),
    completion_rate_4yr NUMERIC(5,4),
    completion_rate_4yr_200percent NUMERIC(5,4),
    completion_rate_4yr_100_pooled NUMERIC(5,4),
    completion_rate_consumer_median NUMERIC(5,4),
    completion_rate_consumer_overall NUMERIC(5,4),
    completion_rate_pell_150_pooled NUMERIC(5,4),
    completion_rate_overall NUMERIC(5,4),
    school_name VARCHAR(255),
    school_city VARCHAR(100),
    school_state CHAR(2),
    school_id INTEGER UNIQUE
);
"""


INSERTION_QUERY = """

    INSERT INTO university_data (
        student_size,
        admission_rate,
        tuition_in_state,
        tuition_out_of_state,
        earnings_10yrs_after_entry,
        completion_rate_150percent,
        completion_rate_4yr,
        completion_rate_4yr_200percent,
        completion_rate_4yr_100_pooled,
        completion_rate_consumer_median,
        completion_rate_consumer_overall,
        completion_rate_pell_150_pooled,
        completion_rate_overall,
        school_name,
        school_city,
        school_state,
        school_id
    ) VALUES (
        %(student_size)s,
        %(admission_rate)s,
        %(tuition_in_state)s,
        %(tuition_out_of_state)s,
        %(earnings)s,
        %(completion_rate_150percent)s,
        %(completion_rate_4yr)s,
        %(completion_rate_4yr_200percent)s,
        %(completion_rate_4yr_100_pooled)s,
        %(completion_rate_consumer_median)s,
        %(completion_rate_consumer_overall)s,
        %(completion_rate_pell_150_pooled)s,
        %(completion_rate_overall)s,
        %(school_name)s,
        %(school_city)s,
        %(school_state)s,
        %(school_id)s
    ) 
    ON CONFLICT (school_id) 
    DO UPDATE SET
        student_size = EXCLUDED.student_size,
        admission_rate = EXCLUDED.admission_rate,
        tuition_in_state = EXCLUDED.tuition_in_state,
        tuition_out_of_state = EXCLUDED.tuition_out_of_state,
        earnings_10yrs_after_entry = EXCLUDED.earnings_10yrs_after_entry,
        completion_rate_150percent = EXCLUDED.completion_rate_150percent,
        completion_rate_4yr = EXCLUDED.completion_rate_4yr,
        completion_rate_4yr_200percent = EXCLUDED.completion_rate_4yr_200percent,
        completion_rate_4yr_100_pooled = EXCLUDED.completion_rate_4yr_100_pooled,
        completion_rate_consumer_median = EXCLUDED.completion_rate_consumer_median,
        completion_rate_consumer_overall = EXCLUDED.completion_rate_consumer_overall,
        completion_rate_pell_150_pooled = EXCLUDED.completion_rate_pell_150_pooled,
        completion_rate_overall = EXCLUDED.completion_rate_overall,
        school_name = EXCLUDED.school_name,
        school_city = EXCLUDED.school_city,
        school_state = EXCLUDED.school_state;

"""


PARAMS = {
    "api_key": os.getenv("API_KEY"),
    "id": "123961,193900,190150,167358,211440,145637,190415,228787,170976,104151",
    "fields": "id,school.name,school.city,school.state,latest.student.size,latest.admissions.admission_rate.overall,latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,latest.completion.rate,latest.earnings.10_yrs_after_entry.median",
}
