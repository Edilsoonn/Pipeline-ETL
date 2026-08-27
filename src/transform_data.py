import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'
columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']
columns_name_to_rename = {
    "base": "base",
    "visibility": "visibility",
    "dt": "data_calculada",
    "timezone": "timezone",
    "id": "cidade_id",
    "name": "cidade_nome",
    "cod": "code",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperatura",
    "main.feels_like": "sensacao_termica",
    "main.temp_min": "temperatura_minima",
    "main.temp_max": "temperatura_maxima",
    "main.pressure": "pressao",
    "main.humidity": "umidade",
    "wind.speed": "velocidade_vento",
    "wind.deg": "direcao_vento",
    "clouds.all": "nuvens",
    "sys.country": "pais",
    "sys.sunrise": "nascer_sol",
    "sys.sunset": "por_do_sol"

    #weather_id, weather_main, weather_description
}
columns_to_normalize_datetime = ['data_calculada', 'nascer_sol', 'por_do_sol']

def create_dataframe(path_name:str) -> pd.DataFrame:
    logging.info(f"Criando DataFrame a partir do arquivo JSON...")
    path = Path(path_name)


    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info(f"DataFrame criado com {len(df)} linha(s)")
    return df

def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)
    logging.info(f"Colunas de clima normalizadas e adicionadas ao DataFrame.")

    return df


def drop_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    logging.info(f"\n Removendo colunas: {columns_name}")
    df = df.drop(columns=columns_name)
    logging.info(f"Colunas removidas - {len(df.columns)} colunas restantes.")

    return df

def rename_columns(df: pd.DataFrame, columns_names: dict[str, str]) -> pd.DataFrame:
    logging.info(f"\nRenomeando {len(columns_names)} colunas...")
    df = df.rename(columns=columns_names)
    logging.info(f"Colunas renomeadas")
    return df

def normalize_datetime_columns(df: pd.DataFrame, columns_names: list[str]) -> pd.DataFrame:
    logging.info(f"\nNormalizando colunas de datetime: {columns_names}")

    for name in columns_names:
        df[name] = (
            pd.to_datetime(df[name], unit="s", utc=True)
            .dt.tz_convert("America/Sao_Paulo")
        )
        logging.info(f"Coluna {name} normalizada para datetime")

    return df

def data_transfomation():
    print("Iniciando transformação de dados...")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_name_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info(f"Transformação de dados concluída com sucesso.")
    return df

