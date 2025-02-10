from sqlalchemy.exc import IntegrityError
from config.env import msk_objects
from jinja2 import Environment, FileSystemLoader
from logs.logging_config import logger
from sqlalchemy import text
from tables.models import PatientJourneyScheduleWindow
from utils.helpers import extract_schedule_info, get_engine, get_session

# Initialize Jinja2 environment
queries = Environment(loader=FileSystemLoader("templates"))


def populate_patient_journey_schedule(batch_size: int = None, offset: int = None):
    engine = get_engine()
    session = get_session()
    template = queries.get_template(msk_objects["query"])

    logger.info("Starting patient journey schedule pipeline...")

    while True:
        try:
            # Fetch data from database using Jinja2 query template
            query = template.render(limit=batch_size, offset=offset)
            results = engine.execute(text(query)).fetchall()

            if not results:
                logger.info("No more records found. Stopping pipeline.")
                break  # Stop when no more records are returned

            batch_entries = []
            for row in results:
                (
                    schedule_start_offset_days,
                    schedule_end_offset_days,
                    schedule_milestone_slug,
                ) = extract_schedule_info(row.schedule_slug)

                batch_entries.append(
                    PatientJourneyScheduleWindow(
                        patient_id=row.patient_id,
                        patient_journey_id=row.patient_journey_id,
                        activity_id=row.activity_id,
                        activity_content_slug=row.activity_content_slug,
                        schedule_id=row.schedule_id,
                        schedule_slug=row.schedule_slug,
                        schedule_start_offset_days=schedule_start_offset_days,
                        schedule_end_offset_days=schedule_end_offset_days,
                        schedule_milestone_slug=schedule_milestone_slug,
                    )
                )

            logger.info(f"Fetched {len(batch_entries)} records from database.")

            # Step 1: Get existing records from the DB to avoid duplicates
            existing_entries = (
                session.query(PatientJourneyScheduleWindow)
                .filter(
                    PatientJourneyScheduleWindow.patient_id.in_(
                        [entry.patient_id for entry in batch_entries]
                    ),
                    PatientJourneyScheduleWindow.patient_journey_id.in_(
                        [entry.patient_journey_id for entry in batch_entries]
                    ),
                )
                .all()
            )

            # Step 2: Convert existing records to a set for fast lookup
            existing_records = {
                (e.patient_id, e.patient_journey_id) for e in existing_entries
            }

            # Step 3: Filter batch_entries to include only new records
            new_entries = [
                entry
                for entry in batch_entries
                if (entry.patient_id, entry.patient_journey_id) not in existing_records
            ]

            logger.info(f"Skipping {len(existing_records)} duplicate records.")
            logger.info(f"Inserting {len(new_entries)} new records.")

            # Step 4: Insert only new entries if they exist
            if new_entries:
                try:
                    session.bulk_save_objects(new_entries)
                    session.commit()
                    logger.info("Batch committed successfully.")
                except IntegrityError as e:
                    error_message = str(e).split("\n")[0]  # Extract only the first line
                    logger.error(
                        f"Skipping duplicate entry due to unique constraint violation: {error_message}"
                    )
                    session.rollback()  # Rollback only the conflicting batch and continue execution.

            offset += batch_size

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            session.rollback()  # Rollback in case of failure
        finally:
            session.close()  # Ensure session is always closed

    logger.info("Patient journey schedule pipeline executed successfully!")


if __name__ == "__main__":
    populate_patient_journey_schedule(
        batch_size=msk_objects["batch_size"], offset=msk_objects["offset"]
    )
    logger.info("Pipeline execution complete!")
