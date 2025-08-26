import sys
from airflow import DAG
from docker.types import Mount
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator

sys.path.append('/opt/airflow/api-request')

def safe_main_callable():
    from insert_records import main
    return main()

default_arguments = {
    'description': 'A DAG to Orchestrate data',
    'start_date': datetime(2025, 8, 25),
    'catchup': False
}

dag = DAG(
    dag_id='weather-api-dbt-orchestrator',
    default_args=default_arguments,
    schedule=timedelta(minutes=1)
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data_task',
        python_callable=safe_main_callable
    )

    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run --select stg_weather_data',
        working_dir='/usr/app',
        mounts=[
            Mount(
                source='/home/mel-harc/weather_data_project/dbt/weather_project',
                target='/usr/app',
                type='bind',
            ),
            Mount(
                source='/home/mel-harc/weather_data_project/dbt/profiles.yml',
                target='/root/.dbt/profiles.yml',
                type='bind',
            ),
        ],
        network_mode='weather_data_project_weather-network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success'
    )

    task1 >> task2