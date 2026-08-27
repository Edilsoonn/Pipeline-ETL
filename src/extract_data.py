import requests
import json
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_weather_data(url:str) -> list:
    # Faz a requisição e converte a resposta da API para um dicionário Python.
    response = requests.get(url)
    data = response.json()

    # Interrompe a etapa quando a API responde com erro ou sem conteúdo.
    if response.status_code != 200:
        logging.error("Erro na Requisição")
        return []

    if not data:
        logging.warning("Nenhum dado encontrado")
        return []

    # Mantém uma cópia dos dados brutos para auditoria e transformação.
    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    logging.info(f"Dados extraídos e salvos em {output_path}")
    return data  

