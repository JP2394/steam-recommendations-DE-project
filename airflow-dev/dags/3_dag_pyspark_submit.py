import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocDeleteClusterOperator
from airflow.operators.dummy_operator import DummyOperator
from utils.upload_to_gcs  import upload_to_gcs

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
CLUSTER_NAME = 'dataproc-airflow-cluster'
REGION='us-west3' # region central1
PROJECT_ID= os.environ.get("GCP_PROJECT_ID")
GCS_BUCKET =  os.environ.get("GCP_GCS_BUCKET")
PYSPARK_FOLDER_SCRIPT_LOCAL= AIRFLOW_HOME + '/dags'
SCRIPT_NAME = 'pyspark_transform.py'
TO_SAVE_SCRIPT= 'script/'
PYSPARK_URI=f'gs://{GCS_BUCKET}/{TO_SAVE_SCRIPT}{SCRIPT_NAME}' # spark job location in cloud storage




CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 85},
    },
    "worker_config": {
        "num_instances": 2, 
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 200},
    }
}

PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {"main_python_file_uri": PYSPARK_URI},
}




local_workflow = DAG(
    "3_pyspark_submit_process",
    schedule_interval=None,
    catchup=False,
    start_date=datetime(2024, 4, 18),
    max_active_runs=3
)

with local_workflow:

        ingest_script_to_gcs = PythonOperator(
            task_id=f'ingest_pyspark_script',
            python_callable=upload_to_gcs,
            op_kwargs={
                "file_":SCRIPT_NAME,
                "downloadpath": PYSPARK_FOLDER_SCRIPT_LOCAL,
                "save_to": TO_SAVE_SCRIPT
            }
        )

             # Define the task to create a Dataproc cluster
        create_cluster = DataprocCreateClusterOperator(
            task_id="create_cluster",
            project_id=PROJECT_ID,
            cluster_config=CLUSTER_CONFIG,
            region=REGION,
            cluster_name=CLUSTER_NAME,
        )        

        submit_job = DataprocSubmitJobOperator(
            task_id="submit_job", 
            job=PYSPARK_JOB, 
            region=REGION, 
            project_id=PROJECT_ID
        ) 

        delete_cluster = DataprocDeleteClusterOperator(
            task_id="delete_cluster", 
            project_id=PROJECT_ID, 
            cluster_name=CLUSTER_NAME, 
            region=REGION
        )



        # Define the task to mark the end of the DAG
        dummy_task_end = DummyOperator(
            task_id='dummy_task_end'
        )

        # Set task dependencies
        create_cluster >> ingest_script_to_gcs  >> submit_job >> delete_cluster >> dummy_task_end 