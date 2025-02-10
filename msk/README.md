
# msk.ai

Prerequisites:
- Python 3.9.10
- Docker

To run the project, execute the following bash script:

```bash
./init.sh
```

The application (i.e. Airflow) will be available at http://localhost:8080.

[DAG](./dags/msk_denormalize_patient_journey.py) will be executed every hour.

## Automated Tests

- They will be executed as part of the `init.sh` script.
- They will also be executed as part of the CI/CD pipeline ([GitHub Actions](../.github/workflows/unittests_msk_etl.yml)).

## Folder Structure

Please follow the folder structure below for information on the project:

```shell
msk
├── Pipfile
├── Pipfile.lock
├── README.md
├── __init__.py
├── alembic
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions                                                        # Database migrations
│       ├── 577ec630a715_0001_create_patient_journey_schedule_.py
│       └── a3cfbbeab93d_0000_baseline.py
├── alembic.ini
├── build.sh                                                            # Build the Docker image for the ETL
├── ci-tests.sh                                                         # Run the tests
├── config
├── dags
│   └── msk_denormalize_patient_journey.py                              # Airflow DAG
├── docker-compose.yaml
├── etls
│   ├── __init__.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── env.py                                                     # Environment variables
│   │   └── metadata.yml                                               # Metadata for the ETL
│   ├── coverage.xml
│   ├── etls.Dockerfile                                                # Dockerfile for the ETL
│   ├── logs                                                           # ETL logs
│   │   ├── __init__.py
│   │   ├── debug_file.log
│   │   ├── error.log
│   │   └── logging_config.py
│   ├── main.py                                                        # ETL main script
│   ├── requirements.txt
│   ├── templates
│   │   └── basedata.jinja.sql                                         # Jinja template for the ETL extract query
│   ├── tests                                                          # ETL unit tests
│   │   ├── conftest.py
│   │   └── test_helpers.py
│   └── utils
│       └── helpers.py                                                 # ETL helper functions
├── init.sh
├── logs
├── plugins
├── requirements.txt                                                   # Python requirements
├── requirements_test.txt                                              # Python requirements for tests
├── setup.cfg
├── setup_postgres.sh
└── tables
    ├── __init__.py
    └── models.py                                                      # SQLAlchemy data models

```