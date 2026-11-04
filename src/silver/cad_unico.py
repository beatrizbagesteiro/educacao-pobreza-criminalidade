from src.utils.minio_functions import minio_uploader, get_from_minio
from src.utils.postgres_functions import get_engine,load_data
import src.utils.pandas_functions as utils
from io import BytesIO
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

def data_transformation_cad_unico():
    logger.info("Iniciando transformações...\n")

    data = get_from_minio('datalake','bronze/cad_unico_2024.csv')

    df_cad_unico = pd.read_csv(BytesIO(data), encoding= 'latin-1')
    
    mapeamento_nomes = {
        "Código": "co_municipio",
        "Referência" : "referencia",
        "Unidade Territorial": "no_municipio",
        "UF": "sg_uf",
        "Número de famílias cadastradas no Cadastro Único em situação de pobreza, segundo a faixa do Programa Bolsa Família*": "familias_pobreza",
        "Número de famílias cadastradas no Cadastro Único com renda per capita de até meio salário-mínimo (Pobreza + Baixa renda)": "familias_baixa_renda",
        "Número de famílias cadastradas no Cadastro Único com renda per capita acima de meio salário-mínimo***": "familias_acima_meio_sm"
    }

    df_silver = utils.rename_columns(df_cad_unico, mapeamento_nomes)
    df_silver['referencia'] = pd.to_datetime(df_silver['referencia'], format='%m/%Y')

    caminho_temp = "/tmp/cad_unico_silver.parquet"
    df_silver.to_parquet(caminho_temp, index=False, compression='snappy')

    minio_uploader(
        source_file=caminho_temp,
        destination_file=f"silver/cad_unico_2024.parquet",
        bucket_name="datalake"
    )

    os.remove(caminho_temp) 

    logger.info("Transformações do dataset Cadastro Único finalizadas...\n")

def load_cad_unico_to_postgres():
    logger.info("Iniciando carregamento do CadÚnico para o Data Warehouse...\n")
    
    data = get_from_minio(
        bucket_name='datalake', 
        object_name='silver/cad_unico_2024.parquet'
    )
    
    df_silver = pd.read_parquet(BytesIO(data))
    
    engine = get_engine()

    load_data("cad_unico_2024", engine, 'silver', df_silver)
    
    logger.info("Carregamento do CadÚnico finalizado com sucesso!\n")