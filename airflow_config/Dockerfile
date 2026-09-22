FROM apache/airflow:slim-3.3.1-python3.10

COPY airflow_config/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.3.1/constraints-3.10.txt"

COPY dags/ /opt/airflow/dags/
COPY src/ /opt/airflow/dags/src