# Pipeline ETL meteorológico com Apache Airflow

Projeto de engenharia de dados em desenvolvimento para extrair informações meteorológicas da OpenWeather API, transformar os dados com Pandas e carregá-los em PostgreSQL. A infraestrutura de orquestração utiliza Apache Airflow 3, Celery, Redis e Docker Compose.

## Arquitetura

```text
OpenWeather API -> extração JSON -> transformação com Pandas -> PostgreSQL
                                      |
                               Apache Airflow
                         Celery + Redis + PostgreSQL
```

## Tecnologias

- Python 3.12
- Apache Airflow 3.1.7
- Pandas e SQLAlchemy
- PostgreSQL e Redis
- Docker Compose
- Jupyter Notebook para análise exploratória

## Estrutura

```text
src/extract_data.py    # consulta da API e persistência em JSON
src/transform_data.py  # normalização e tratamento dos dados
src/load_data.py       # carga no PostgreSQL
dags/weather_dag.py    # orquestração horária do pipeline
notebooks/             # análise exploratória
docker-compose.yaml    # ambiente local do Airflow
```

## Execução do Airflow

Crie um arquivo `.env` na raiz:

```env
AIRFLOW_UID=1000
```

Inicialize e suba os serviços:

```bash
docker compose up airflow-init
docker compose up -d
docker compose ps
```

A interface fica disponível em [http://localhost:8081](http://localhost:8081). A porta externa é 8081 para evitar conflito com outros serviços locais; entre os containers, o Airflow continua usando a porta 8080.

## Configuração da pipeline

Crie `config/.env` localmente com suas próprias credenciais. Esse arquivo é ignorado pelo Git:

```env
API_KEY=sua_chave_openweather
data_base=nome_do_banco
user=usuario_postgres
password=senha_postgres
DB_HOST=postgres
DB_PORT=5432
```

## Status

A pipeline completa está orquestrada pela DAG `weather_dag`, executada a cada hora. Ela extrai os dados da OpenWeather, transforma e persiste um arquivo Parquet e carrega os registros na tabela `sp_weather` do PostgreSQL em container. O próximo passo é acrescentar testes automatizados e monitoramento.

> Projeto de estudo em evolução. Nenhuma credencial é armazenada no repositório.

