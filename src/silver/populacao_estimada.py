from src.utils.pandas_functions import drop_columns, rename_columns, cast_type
from src.utils.minio_functions import get_from_minio, minio_uploader
from src.utils.postgres_functions import get_engine,load_data
from io import BytesIO
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

def data_transformation_populacao_estimada():
    logger.info("Iniciando transformações no dataset População Estimada 2024...\n")
    columns_to_drop = ['NC','NN','MC','MN','D1C','D1N','D2C','D2N']
    columns_to_rename = {'V':'cont_populacao', 'D3C': 'co_municipio', 'D3N':'no_municipio'}

    data = get_from_minio('datalake','bronze/populacao_estimada_2024.json')

    df = pd.read_json(BytesIO(data))

    df_silver = drop_columns(df, columns_to_drop)
    df_silver = rename_columns(df_silver,columns_to_rename)

    df_silver['sg_uf'] = df_silver['no_municipio'].str[-2:]

    df_silver['no_municipio'] = df_silver['no_municipio'].str[:-5]

    df_silver = df_silver.iloc[1:].reset_index(drop=True)

    df_silver['cont_populacao'] = pd.to_numeric(df_silver['cont_populacao'], errors='coerce')

    df_silver = cast_type(df_silver,['cont_populacao','co_municipio'],'Int64')

    caminho_temp = "/tmp/populacao_estimada_2024.parquet"
    df_silver.to_parquet(caminho_temp, index=False, compression='snappy')
    
    minio_uploader(
        source_file=caminho_temp,
        destination_file=f"silver/populacao_estimada_2024.parquet",
        bucket_name="datalake"
    )

    os.remove(caminho_temp)
    
    logger.info("Transformações do dataset População Estimada 2024 finalizadas...\n")
    
    return df_silver

def load_populacao_estimada_to_postgres():
    logger.info("Iniciando carregamento da Populacao Estimada para o Data Warehouse...\n")
    
    data = get_from_minio(
        bucket_name='datalake', 
        object_name='silver/populacao_estimada_2024.parquet', 
    )
    
    df_silver = pd.read_parquet(BytesIO(data))
    
    engine = get_engine()

    load_data("populacao_estimada_2024", engine, 'silver', df_silver)
    
    logger.info("Carregamento do Censo Escolar finalizado com sucesso!\n")