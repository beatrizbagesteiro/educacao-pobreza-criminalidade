from src.utils.minio_functions import minio_uploader
from pathlib import Path
from io import BytesIO
import logging
import json
import requests
logger = logging.getLogger(__name__)

def load_bronze_populacao_estimada():
    url = 'https://apisidra.ibge.gov.br/values/t/6579/p/2024/v/all/n6/all'
    
    try:
        logger.info("Iniciando solicitação HTTP...\n")
        raw_data = requests.get(url).json()
        
        data = json.dumps(raw_data).encode('utf-8')
        data = BytesIO(data)
        
        minio_uploader(
            source_file=data,
            destination_file="bronze/populacao_estimada_2024.json",
            bucket_name="datalake"
        )
        logger.info('Solicitação realizada com sucesso. JSON salvo no MinIO\n')
        
    except Exception as e:
        logger.error(f"Erro na extração ou envio: {e}\n")
        raise e