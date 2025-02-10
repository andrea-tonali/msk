import logging
import logging.config
import os

# Define a configuration variable to switch log levels
DEFAULT_LOG_LEVEL = logging.DEBUG
log_directory = os.path.join(os.getcwd(), "logs")


def setup_logging():
    # Define the logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": logging.INFO,  # Console always logs INFO and above
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "debug_file": {
                "class": "logging.FileHandler",
                "level": logging.DEBUG,  # File always logs DEBUG and above
                "formatter": "detailed",
                "filename": os.path.join(log_directory, "debug_file.log"),
                # "mode": "a", # Append to the file
                "mode": "w",  # Overwrite the file each run
            },
            "error_file": {
                "class": "logging.FileHandler",
                "level": logging.ERROR,
                "formatter": "detailed",
                "filename": os.path.join(log_directory, "error.log"),
                # "mode": "a", # Append to the file
                "mode": "w",  # Overwrite the file each run
            },
        },
        "loggers": {
            "": {
                "level": DEFAULT_LOG_LEVEL,  # Use the switch here
                "handlers": ["console", "debug_file", "error_file"],
            },
            "py.warnings": {  # Redirect warnings to debug_file
                "handlers": ["debug_file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    # Apply the logging configuration
    logging.config.dictConfig(logging_config)


# Call setup_logging to configure the logging system
setup_logging()

# Create a logger instance that can be imported
logger = logging.getLogger("msk.etl")
