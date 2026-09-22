# utils/file_uploader.py
from minio import Minio
from minio.error import S3Error
import os

def minio_uploader(source_file, destination_file, bucket_name):
    client = Minio(
        "minio:9000", # nome_container:porta
        access_key=os.environ.get("MINIO_ROOT_USER"),
        secret_key=os.environ.get("MINIO_ROOT_PASSWORD"),
        secure=False 
    )

    try:
        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
            print("Criado o bucket", bucket_name)
        else:
            print("O bucket", bucket_name, "já existe")

        client.fput_object(
            bucket_name, destination_file, source_file,
        )
        print(f"Sucesso! {source_file} salvo como {destination_file} no bucket {bucket_name}")

    except S3Error as err:
        print(f"Ocorreu um erro no MinIO: {err}")
    except Exception as e:
        print(f"Erro inesperado: {e}")