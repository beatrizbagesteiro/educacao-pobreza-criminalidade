from src.utils.minio_uploader import minio_uploader
import polars as pl
from pathlib import Path
import os


def read_file(path, file_type):
    extension_map = {
        "xlsx": (path.glob("*.xlsx"), pl.read_excel), # First Class Function
        "xls": (path.glob("*.xls"), pl.read_excel),
        "csv": (path.glob("*.csv"), lambda f: pl.read_csv(f, encoding="latin1",separator=";",infer_schema_length=10000)),
    }

    if file_type not in extension_map:
        raise ValueError(f"Tipo de arquivo não suportado: {file_type}")

    files, reader = extension_map[file_type]

    for file in files:
        print(f"Processando: {file.name}")
        df = reader(file)

        parquet_name = file.with_suffix('.parquet').name
        temp_path = f"temp_{parquet_name}" # Caminho do arquivo no container

        df.write_parquet(temp_path)

        minio_uploader(
            source_file=temp_path,
            destination_file=f"bronze/{parquet_name}",
            bucket_name="datalake"
        )

        os.remove(temp_path)  # Para não lotar o disco do container, excluimos após a inserção no  datalake

def main():
    current_dir = Path(__file__).parent.resolve()
    root = current_dir.parent.parent
    raw_data = root / 'data' /'raw'

    read_file(raw_data,"xlsx")
    read_file(raw_data, "xls")
    read_file(raw_data,"csv")

if __name__ == "__main__":
    main()
    