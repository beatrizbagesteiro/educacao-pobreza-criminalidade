from airflow.sdk import dag, task
from src.bronze.load_censo_escolar import load_bronze_censo_escolar
from src.bronze.load_cad_unico import load_bronze_cad_unico
from src.bronze.load_populacao_estimada import load_bronze_populacao_estimada
from src.silver.cad_unico import data_transformation_cad_unico, load_cad_unico_to_postgres
from src.silver.censo_escolar import data_transformation_censo_escolar, load_censo_escolar_to_postgres
from src.silver.populacao_estimada import data_transformation_populacao_estimada, load_populacao_estimada_to_postgres

@dag(dag_id="pipeline")
def pipeline():

    @task.python
    def bronze_load_censo_escolar():
        load_bronze_censo_escolar()

    @task.python
    def bronze_load_cad_unico():
        load_bronze_cad_unico()

    @task.python
    def bronze_load_populacao_estimada():
        load_bronze_populacao_estimada()

    @task.python
    def silver_transformation_cad_unico():
        data_transformation_cad_unico()

    @task.python
    def silver_transformation_censo_escolar():
        data_transformation_censo_escolar()

    @task.python
    def silver_transformation_populacao_estimada():
        data_transformation_populacao_estimada()

    @task.sql(conn_id="postgres_dw")
    def silver_create_tables():
        caminho = "/opt/airflow/src/silver/create_tables.sql"
        with open(caminho, "r") as sql:
            query_sql = sql.read()
        
        return query_sql

    @task.python
    def silver_load_cad_unico_to_postgres():
        load_cad_unico_to_postgres()

    @task.python
    def silver_load_censo_escolar_to_postgres():
        load_censo_escolar_to_postgres()

    @task.python
    def silver_load_populacao_estimada_to_postgres():
        load_populacao_estimada_to_postgres()

    @task.sql(conn_id="postgres_dw")
    def gold_create_dim_table():
        caminho = "/opt/airflow/src/gold/create_dim_table.sql"
        with open(caminho, "r") as sql:
            query_sql = sql.read()
        return query_sql

    @task.sql(conn_id="postgres_dw")
    def gold_create_fact_table():
        caminho = "/opt/airflow/src/gold/create_fact_table.sql"
        with open(caminho, "r") as sql:
            query_sql = sql.read()
        
        return query_sql

    # Task Dependencies
    bronze_load_censo_escolar = bronze_load_censo_escolar()
    bronze_load_cad_unico = bronze_load_cad_unico()
    bronze_load_populacao_estimada = bronze_load_populacao_estimada()
    silver_transformation_censo_escolar= silver_transformation_censo_escolar()
    silver_transformation_cad_unico = silver_transformation_cad_unico()
    silver_transformation_populacao_estimada = silver_transformation_populacao_estimada()
    silver_create_tables = silver_create_tables()
    silver_load_censo_escolar_to_postgres = silver_load_censo_escolar_to_postgres()
    silver_load_cad_unico_to_postgres = silver_load_cad_unico_to_postgres()
    silver_load_populacao_estimada_to_postgres = silver_load_populacao_estimada_to_postgres()
    gold_create_dim_table = gold_create_dim_table()
    gold_create_fact_table = gold_create_fact_table()

    silver_create_tables >> [silver_load_censo_escolar_to_postgres, silver_load_cad_unico_to_postgres, silver_load_populacao_estimada_to_postgres] >> gold_create_dim_table >> gold_create_fact_table
    
    bronze_load_censo_escolar >> silver_transformation_censo_escolar >> silver_load_censo_escolar_to_postgres
    bronze_load_cad_unico >> silver_transformation_cad_unico >> silver_load_cad_unico_to_postgres
    bronze_load_populacao_estimada >> silver_transformation_populacao_estimada >> silver_load_populacao_estimada_to_postgres



# Instância da DAG
pipeline() 