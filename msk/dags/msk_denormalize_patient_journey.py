from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone

from airflow.models import DAG
from airflow.providers.docker.operators.docker import DockerOperator


@dataclass
class CustomDefaultArgs:
    owner: str = "AndreaTonali"
    depends_on_past: bool = False
    start_date: datetime = datetime.now(timezone.utc)  # Start immediately
    email_on_failure: bool = False
    email_on_retry: bool = False
    retries: int = 2
    retry_delay: timedelta = timedelta(minutes=5)


# Convert the dataclass instance to a dictionary
default_args_dict = asdict(CustomDefaultArgs())

with DAG(
    "msk_denormalize_patient_journey",
    default_args=default_args_dict,
    schedule_interval="0 * * * *",  # Run every hour
    catchup=False,  # Ensures only future runs execute
    tags=["msk", "ETL", "denormalize"],
) as dag:

    DockerOperator(
        task_id="run_etls_container",
        image="etls-denormalize-patient-journey",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )
