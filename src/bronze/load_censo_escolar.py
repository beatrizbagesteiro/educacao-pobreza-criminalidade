from src.utils.minio_functions import minio_uploader
from pathlib import Path

def load_bronze_censo_escolar():
    current_dir = Path(__file__).parent.resolve()
    root = current_dir.parent.parent
    raw_data = root / 'data' /'raw' / 'censo_escolar_2024.csv'

    minio_uploader(
        source_file=str(raw_data),
        destination_file=f"bronze/censo_escolar_2024.csv",
        bucket_name="datalake"
    )
    