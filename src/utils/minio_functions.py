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
    logging.info(f"Iniciando ingestão do dataset {source_file}...")
    client = get_minio_client()
    try:
        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
            logger.info("Criado o bucket", bucket_name)
        else:
            logger.info("O bucket", bucket_name, "já existe")

        client.fput_object(
            bucket_name, destination_file, source_file,
        )
        logger.info(f"Sucesso! {source_file} salvo como {destination_file} no bucket {bucket_name}")

    except S3Error as err:
        logger.error(f"Ocorreu um erro no MinIO: {err}")
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
