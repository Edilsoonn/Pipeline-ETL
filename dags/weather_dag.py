from datetime import datetime, timedelta
import os
from pathlib import Path
from airflow.sdk import dag, task
import sys

# Disponibiliza os módulos ETL montados pelo Docker dentro do container.
sys.path.insert(0, '/opt/airflow/src')

from extract_data import extract_weather_data
from load_data import load_weather_data
from transform_data import data_transfomation
from dotenv import load_dotenv

# Carrega configurações locais sem expor credenciais no código.
env_path = Path(__file__).resolve().parent.parent /'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')
url = f"https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo&units=metric&appid={API_KEY}"

@dag(
    dag_id="weather_dag",
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    },
    description = 'Pipeline ETL - Clima SP',
    # Executa a pipeline no início de cada hora.
    schedule = '0 */1 * * *', 
    start_date = datetime(2026, 8, 26),
    catchup = False,
    tags = ['weather', 'ETL', 'clima_sp'],
)

def weather_dag():
    
    @task
    def extract():
        # Consulta a OpenWeather e persiste a resposta bruta em JSON.
        extract_weather_data(url)

    @task
    def transform():
        # Trata os campos e usa Parquet como arquivo intermediário.
        df = data_transfomation()
        df.to_parquet('/opt/airflow/data/weather_data.parquet', index=False)

    @task
    def load():
        import pandas as pd
        # Recupera os dados tratados e os envia ao PostgreSQL.
        df = pd.read_parquet('/opt/airflow/data/weather_data.parquet')
        load_weather_data('sp_weather', df)

    # Define a ordem obrigatória das tarefas da pipeline ETL.
    extract() >> transform() >> load()

 
# Registra a DAG para que o Airflow possa encontrá-la.
weather_dag()



