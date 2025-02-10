import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from config.env import POSTGRESQL_DB_URI
from logs.logging_config import logger  # Importing logger from logging_config


def extract_schedule_info(schedule_slug: str) -> tuple:
    try:
        logger.debug(f"Extracting schedule info from slug: {schedule_slug}")

        if schedule_slug in ["always", "pre-op", "post-op", "op", "inv"]:
            logger.debug(f"Slug '{schedule_slug}' mapped to 'operation'.")
            return None, None, "operation"

        # Mapping units to days
        unit_to_days = {"d": 1, "w": 7, "m": 30, "y": 365}

        # Regex for two-duration schedules (e.g., "1d-6w-post-op")
        match = re.match(r"(\d+)([dwmy])-(\d+)([dwmy])-(\w+)", schedule_slug)
        if match:
            start_value, start_unit, end_value, end_unit, milestone = match.groups()

            start_days = -int(start_value) * unit_to_days.get(start_unit, 1)
            end_days = -int(end_value) * unit_to_days.get(end_unit, 1)

            logger.debug(
                f"Extracted: start_days={start_days}, end_days={end_days}, milestone=operation"
            )
            return start_days, end_days, "operation"

        # Regex for single-duration schedules (e.g., "3y-post-op")
        match = re.match(r"(\d+)([dwmy])-(\w+)", schedule_slug)
        if match:
            value, unit, milestone = match.groups()
            days = -int(value) * unit_to_days.get(unit, 1)

            logger.debug(
                f"Extracted: start_days={days}, end_days={days}, milestone=operation"
            )
            return days, days, "operation"

        logger.debug(f"Unknown format for schedule_slug: {schedule_slug}")
        return None, None, "unknown"

    except Exception as e:
        logger.error(f"Error extracting schedule info from '{schedule_slug}': {e}")
        return None, None, "error"


def get_engine():
    try:
        logger.info("Creating database engine.")
        engine = create_engine(POSTGRESQL_DB_URI).connect()
        logger.info("Database connection established successfully.")
        return engine
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {e}")
        raise


def get_session():
    try:
        logger.info("Creating a new database session.")
        engine = get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        logger.info("Database session created successfully.")
        return session
    except SQLAlchemyError as e:
        logger.error(f"Error creating database session: {e}")
        raise
