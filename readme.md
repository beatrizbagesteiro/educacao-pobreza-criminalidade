CSV (data/raw/)
   ↓ (Airflow lê e processa)
MinIO → bucket "bronze"   (dados brutos, direto da fonte, pouca transformação)
   ↓ (Airflow limpa/tipa/deduplica)
MinIO → bucket "silver"   (dados tratados, ainda em formato de arquivo/Parquet)
   ↓ (Airflow agrega e carrega)
Postgres → schema "gold"  (dados finais, prontos pro dashboard)
   ↓
Dashboard (PowerBI/Metabase/Streamlit conectando direto no Postgres)