
from datetime import datetime,timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import os


# Define your Google Cloud Storage and BigQuery parameters
GCS_BUCKET = os.environ.get("GCP_GCS_BUCKET")
BQ_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BQ_DATASET = 'steam_data'


# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    '4_parquet_to_bigquery',
    default_args=default_args,
    description='Create an external table in BigQuery from PARQUET in GCS',
    schedule_interval=None,  # Set your desired schedule interval
    start_date=datetime(2024, 4, 18),  # Set your desired start date
    tags=['example'],
)


GCS_OBJECTS_LIST = ['users','games','recommendations']

for  gcs_object in GCS_OBJECTS_LIST:
    task_id = f'processed_{gcs_object}_parquet_to_bigquery'
    # Define the task to transfer CSV from GCS to BigQuery
    transfer_parquet_to_bigquery = GCSToBigQueryOperator(
        task_id = task_id,
        bucket=GCS_BUCKET,
        source_objects=[f'processed/{gcs_object}/part-*.parquet'],
        destination_project_dataset_table=f"{BQ_PROJECT_ID}.{BQ_DATASET}.{gcs_object}",
        source_format='PARQUET',
        create_disposition='CREATE_IF_NEEDED',
        skip_leading_rows=1,
        autodetect=True,
        write_disposition='WRITE_TRUNCATE',
        dag=dag,
    )

    transfer_parquet_to_bigquery