from src.constants import PostgresHook, POSTGRES_CONN_ID
from rich import print


class PostHook:
    def __init__(self):
        pass

    def CreateHook(self, conn_id: str = POSTGRES_CONN_ID):
        try:
            f = PostgresHook(
                enable_log_db_messages="True",
                postgres_conn_id=conn_id,
            )
            return f
        except RuntimeError:
            return "Failed to make a connection to Postgres DB"
        finally:
            print("Connection Established Succesfully")
