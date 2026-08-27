import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow.sdk import dag, task
from dotenv import load_dotenv

sys.path.insert(0, "/opt/airflow/src")

from extract_data import extract_weather_data
from load_data import load_weather_data
from transform_data import data_transfomation


env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("API_KEY")
url = (
    "https://api.openweathermap.org/data/2.5/weather"
    f"?q=Sao Paulo&units=metric&appid={API_KEY}"
)


@dag(
    dag_id="weather_dag",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    description="Pipeline ETL - Clima SP",
    schedule="0 */1 * * *",
    start_date=datetime(2026, 8, 26),
    catchup=False,
    tags=["weather", "ETL", "clima_sp"],
)
def weather_dag():
    @task
    def extract():
        extract_weather_data(url)

    @task
    def transform():
        df = data_transfomation()
        df.to_parquet(
            "/opt/airflow/data/weather_data.parquet",
            index=False,
        )

    @task
    def load():
        import pandas as pd

        df = pd.read_parquet(
            "/opt/airflow/data/weather_data.parquet"
        )
        load_weather_data("sp_weather", df)

    extract() >> transform() >> load()


weather_dag()

