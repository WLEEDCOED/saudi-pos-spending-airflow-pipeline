from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="test_dag",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["test"],
) as dag:

    print_hello = BashOperator(
        task_id="print_hello",
        bash_command="echo 'Airflow is working successfully!'"
    )