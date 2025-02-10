
# msk.ai

Prerequisites:
- Python 3.9.10
- Docker

To run the project, execute the following command:

```bash
./init.sh
```

The application (i.e. Airflow) will be available at http://localhost:8080.

[DAG](./dags/msk_denormalize_patient_journey.py) will be executed every hour.

## Automated Tests

- They will be executed as part of the `init.sh` script.
- They will also be executed as part of the CI/CD pipeline (GitHub Actions).
