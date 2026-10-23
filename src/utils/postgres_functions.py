import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import logging

logger = logging.getLogger(__name__)

def get_engine():
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    database = os.getenv('POSTGRES_DW')
    host = 'postgres'
    logger.info(f"Conectando em {host}:5432/{database}\n")
    
    url = f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"

    return create_engine(url)

def load_data(table_name, engine, schema, df):
    logger.info(f"Carregando dados na tabela {table_name}...\n")
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            schema = schema,
            if_exists='append',
            index = False
        )
    except Exception as e:
        logger.error(f"Erro ao carregar os dados na tabela {table_name}...\n")
        raise e