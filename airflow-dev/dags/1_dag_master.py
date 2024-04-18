import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
csv_source = AIRFLOW_HOME + '/steam_dataset'

local_workflow = DAG(
    "1_dag_master",
    schedule_interval=None,
    catchup=False,
    start_date=datetime(2024, 4, 18),
    max_active_runs=3
)

with local_workflow:

    kaggle_to_gcs = TriggerDagRunOperator(
    task_id='kaggle_to_gcs_process',
    trigger_dag_id = '2_kaggle_to_gcs',
    wait_for_completion = True
    )


    pyspark_process = TriggerDagRunOperator(
    task_id='pyspark_submit_process',
    trigger_dag_id = '3_pyspark_submit_process',
    wait_for_completion = True
    )

    parquet_to_bigquery= TriggerDagRunOperator(
    task_id='parquet_to_bigquery',
    trigger_dag_id = '4_parquet_to_bigquery',
    wait_for_completion = True
    )

    dbt_run = TriggerDagRunOperator(
    task_id='dbt_run',
    trigger_dag_id = '5_dbt_run',
    wait_for_completion = True
    )


    # Set task dependencies
    kaggle_to_gcs >> pyspark_process >> parquet_to_bigquery >> dbt_run
