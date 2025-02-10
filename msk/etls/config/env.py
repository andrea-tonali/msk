from pathlib import Path

import yaml
from environs import Env
from logs.logging_config import logger

env = Env()

POSTGRESQL_DB_URI = env.str(
    "POSTGRESQL_DB",
    "postgresql+psycopg2://postgres:postgres@host.docker.internal:5433/msk_db",
)
MSK_DATABASE = env.str("DB_NAME", "msk_db")

DATABASE_CONFIG = Path(__file__).parent / "metadata.yml"

with open(DATABASE_CONFIG) as stream:
    try:
        msk_objects = yaml.safe_load(stream)
        msk_objects = msk_objects[MSK_DATABASE]
    except yaml.YAMLError as exc:
        logger.error(exc)
