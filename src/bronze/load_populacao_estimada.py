from src.utils.minio_functions import minio_uploader
from pathlib import Path

def load_bronze_populacao_estimada():
    current_dir = Path(__file__).parent.resolve()
    root = current_dir.parent.parent
    raw_data = root / 'data' /'raw' / 'populacao_estimada_2024.json'

    minio_uploader(
        source_file=str(raw_data),
        destination_file=f"bronze/populacao_estimada_2024.json",
        bucket_name="datalake"
    )
    