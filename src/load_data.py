from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Lê as credenciais locais, mantidas fora do repositório Git.
env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('data_base')
# No Docker, "postgres" é o nome do serviço na rede interna do Compose.
host = os.getenv("DB_HOST", "postgres")
port = os.getenv('DB_PORT', '5432')

def get_engine():
    # Cria o mecanismo de conexão reutilizado pelo Pandas/SQLAlchemy.
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}" 
        f"@{host}:{port}/{database}"
    )

engine = get_engine()

def load_weather_data(table_name:str, df):
    # Acrescenta a nova coleta sem apagar os registros anteriores.
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )

    logging.info(f"Dados carregados com sucesso na tabela '{table_name}' do banco de dados '{database}'.")

    # Confere quantos registros existem após a carga.
    df_check = pd.read_sql_query(text(f"SELECT * FROM {table_name}"), con=engine)
    logging.info(f"Total de registros na tabela: {len(df_check)}")

