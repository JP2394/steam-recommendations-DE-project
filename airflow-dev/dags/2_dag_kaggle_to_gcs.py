import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils.download_from_kaggle import download_from_kaggle
from utils.upload_to_gcs  import upload_to_gcs

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
csv_source = AIRFLOW_HOME + '/steam_dataset'
save_to_folder = "raw/"

local_workflow = DAG(
    "2_kaggle_to_gcs",
    schedule_interval=None,
    catchup=False,
    start_date=datetime(2024, 4, 18),
    max_active_runs=3
)

with local_workflow:

    downloadDataset = PythonOperator(
        task_id="dataset_download",
        python_callable=download_from_kaggle,
        op_kwargs={
            "downloadpath": csv_source
        }
    )


        # Define the tasks to ingest each CSV file to GCS
    files_to_ingest = ['games.csv', 'recommendations.csv', 'users.csv']

    for file_ in files_to_ingest:
        ingest_to_gcs = PythonOperator(
            task_id=f'ingest_{file_}_to_bucket',
            python_callable=upload_to_gcs,
            op_kwargs={
                "file_": file_,
                "downloadpath": csv_source,
                "save_to": save_to_folder
            }
        )

        # Set task dependencies
        downloadDataset >> ingest_to_gcs
