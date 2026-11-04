from src.utils.minio_functions import minio_uploader, get_from_minio
from src.utils.postgres_functions import get_engine,load_data
import src.utils.pandas_functions as utils
from pathlib import Path
from io import BytesIO
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

def select_base_and_prefixed_columns(df: pd.DataFrame, base_columns: list, prefix: str) -> pd.DataFrame:
    logger.info("Iniciando seleção de colunas...\n")
    try:
        prefixed_cols = [col for col in df.columns if col.startswith(prefix)]
        final_columns = base_columns + prefixed_cols
        
        return df[final_columns]
        
    except Exception as e:
        logger.error(f"Erro ao selecionar as colunas: {e}")
        raise e
    
def data_transformation_censo_escolar():
    logger.info("Iniciando transformações...\n")

    data = get_from_minio('datalake', 'bronze/censo_escolar_2024.csv') 
    
    df_silver = pd.read_csv(BytesIO(data), encoding='latin1', delimiter= ';', engine='pyarrow')
    df_silver = utils.filter_active_rows(df_silver, 'TP_SITUACAO_FUNCIONAMENTO', 1)

    base_columns = ['NO_REGIAO', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'SG_UF']
    infra_prefixes = ('IN_AGUA', 'IN_ENERGIA', 'IN_ESGOTO', 'IN_LIXO', 'IN_INTERNET', 
                      'IN_BANHEIRO', 'IN_ACESSABILIDADE', 'IN_COZINHA', 'IN_REFEITORIO', 
                      'IN_BIBLIOTECA', 'IN_QUADRA_ESPORTES', 'IN_ALIMENTACAO', 'IN_LABORATORIO')
    regions = ['Nordeste', 'Sudeste']

    df_silver = select_base_and_prefixed_columns(df_silver, base_columns, infra_prefixes)

    cols_to_cast = [c for c in df_silver.columns if c.startswith(infra_prefixes)]
    df_silver = utils.cast_type(df_silver, cols_to_cast, 'int64')

    df_silver = utils.columns_name_to_lower(df_silver)
    df_silver['co_municipio'] = df_silver['co_municipio'].astype(str).str[:-1]

    caminho_temp = "/tmp/censo_escolar_silver.parquet"
    df_silver.to_parquet(caminho_temp, index=False, compression='snappy')
   
    minio_uploader(
        source_file=caminho_temp,
        destination_file=f"silver/censo_escolar_2024.parquet",
        bucket_name="datalake"
    )

    os.remove(caminho_temp)
    
    logger.info("Transformações do dataset Censo Escolar finalizadas...\n")
    
    return df_silver

def load_censo_escolar_to_postgres():
    logger.info("Iniciando carregamento do Censo Escolar para o Data Warehouse...\n")
    
    data = get_from_minio(
        bucket_name='datalake', 
        object_name='silver/censo_escolar_2024.parquet', 
    )
    
    df_silver = pd.read_parquet(BytesIO(data))
    
    engine = get_engine()

    load_data("censo_escolar_2024", engine, 'silver', df_silver)
    
    logger.info("Carregamento do Censo Escolar finalizado com sucesso!\n")