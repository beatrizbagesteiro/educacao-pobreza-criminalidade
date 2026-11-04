from minio.error import S3Error
from minio import Minio
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)

# Lazy initialization
def get_minio_client() -> Minio:
    return Minio(
        "minio:9000", # nome_container:porta
        access_key=os.environ.get("MINIO_ROOT_USER"),
        secret_key=os.environ.get("MINIO_ROOT_PASSWORD"),
        secure=False 
    )

def minio_uploader(source_file, destination_file, bucket_name):
    logger.info(f"Iniciando ingestão do dataset para {destination_file}...")
    client = get_minio_client()
    
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logger.info(f"Criado o bucket {bucket_name}")

        if isinstance(source_file, str):
            client.fput_object(bucket_name, destination_file, source_file)
        else:
            file_length = source_file.getbuffer().nbytes
            client.put_object(
                bucket_name, 
                destination_file, 
                source_file, 
                length=file_length
            )
            
        logger.info(f"Sucesso! Salvo como {destination_file} no bucket {bucket_name}")

    except Exception as e:
        logger.error(f"Erro inesperado: {e}")

def get_from_minio(bucket_name, object_name):
    client = get_minio_client()
    try:
        response = client.get_object(bucket_name, object_name)
        
        file_data = response.read()
        
        response.close()
        response.release_conn()
        
        logger.info(f"Arquivo '{object_name}' carregado na memória com sucesso.")
        return file_data
        
    except S3Error as err:
        logger.error(f"A leitura falhou: {err}")
        return None
