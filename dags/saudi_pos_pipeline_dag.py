from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_PATH = "/opt/airflow/project"


with DAG(
    dag_id="saudi_pos_spending_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["saudi", "pos", "data-modeling"],
) as dag:

    extract_data = BashOperator(
        task_id="extract_data",
        bash_command=f"python {PROJECT_PATH}/scripts/extract.py",
    )

    transform_data = BashOperator(
        task_id="transform_data",
        bash_command=f"python {PROJECT_PATH}/scripts/transform.py",
    )

    model_data = BashOperator(
        task_id="model_data",
        bash_command=f"python {PROJECT_PATH}/scripts/model_data.py",
    )

    run_quality_checks = BashOperator(
        task_id="run_quality_checks",
        bash_command=f"python {PROJECT_PATH}/scripts/quality_checks.py",
    )

    load_to_postgres = BashOperator(
        task_id="load_to_postgres",
        bash_command=f"python {PROJECT_PATH}/scripts/load_to_postgres.py",
    )

    extract_data >> transform_data >> model_data >> run_quality_checks >> load_to_postgres