set -e 

echo Setup Python Environment
pip install -r requirements.txt

echo run mypy/type checks + flake8/linting + pytest/unit tests
./ci-tests.sh

echo Build Docker Image Application
./build.sh

echo Setup PostgreSQL Database
./setup_postgres.sh

echo Initialize Airflow
docker compose up airflow-init

echo Start Airflow
docker compose up -d
