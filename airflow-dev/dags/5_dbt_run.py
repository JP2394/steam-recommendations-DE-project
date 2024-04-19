import os
from datetime import datetime,timedelta
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import GoogleCloudServiceAccountFileProfileMapping

BQ_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DBT_DATASET = "dbt_prod"

profile_config = ProfileConfig(
    profile_name="data_pipeline",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountFileProfileMapping(
        conn_id="google_cloud_connection",
        profile_args={
            "project": BQ_PROJECT_ID,
            "dataset": DBT_DATASET,
            "keyfile": "/usr/local/airflow/.google/credentials/google_credentials.json",
            "location":"us-central1",
        },
    ),
)

dbt_run_dag = DbtDag(
    project_config=ProjectConfig("/usr/local/airflow/dbt/data_pipeline",),
    operator_args={"install_deps": True},
    profile_config=profile_config,
    execution_config=ExecutionConfig(dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",),
    schedule_interval=None,
    start_date=datetime(2024, 4, 18),
    catchup=False,
    dag_id="5_dbt_run",
)

dbt_run_dag
