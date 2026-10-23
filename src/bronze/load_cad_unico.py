from src.utils.minio_functions import minio_uploader
from pathlib import Path

def load_bronze_cad_unico():
    current_dir = Path(__file__).parent.resolve()
    root = current_dir.parent.parent
    raw_data = root / 'data' /'raw' / 'cad_unico_2024.csv'

    minio_uploader(
        source_file=str(raw_data),
        destination_file=f"bronze/cad_unico_2024.csv",
        bucket_name="datalake"
    )
    