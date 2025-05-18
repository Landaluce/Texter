import logging
import os
import sys

class ExcludeLogFilter(logging.Filter):
    """Filter to exclude specific log messages."""
    def filter(self, record):
        # List of messages to exclude
        excluded_messages = ["Could not understand audio", "waiting time error"]
        return not any(excluded_msg in record.getMessage() for excluded_msg in excluded_messages)


def setup_logging():
    """
    Configures logging settings for different loggers, handlers, and formatters.
    - Logs of level INFO and higher to 'general.log'.
    - Logs of level ERROR and higher to 'errors.log'.
    - Logs of level WARNING and higher to the console, excluding ERROR logs.
    """
    # Create formatters
    detailed_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s')
    simple_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create handlers
    general_file_handler = logging.FileHandler('../logs/general.log')
    general_file_handler.setLevel(logging.INFO)
    general_file_handler.setFormatter(detailed_formatter)

    warning_file_handler = logging.FileHandler('../logs/warnings.log')
    warning_file_handler.setLevel(logging.WARNING)
    warning_file_handler.setFormatter(simple_formatter)
    warning_file_handler.addFilter(ExcludeLogFilter())

    error_file_handler = logging.FileHandler('../logs/errors.log')
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(detailed_formatter)
    error_file_handler.addFilter(ExcludeLogFilter())

    # Create loggers
    general_logger = logging.getLogger('general_logger')
    general_logger.setLevel(logging.INFO)
    general_logger.addHandler(general_file_handler)

    warning_logger = logging.getLogger('warning_logger')
    warning_logger.setLevel(logging.WARNING)
    warning_logger.addHandler(warning_file_handler)

    error_logger = logging.getLogger('error_logger')
    error_logger.setLevel(logging.ERROR)
    error_logger.addHandler(error_file_handler)

    # Set up the root logger to log to the console without errors
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)

    # Remove the default console handler (if any)
    for handler in root_logger.handlers[:]:
        if isinstance(handler, logging.StreamHandler):
            root_logger.removeHandler(handler)

    # Optionally suppress standard input/output from terminal
    sys.stderr = open(os.devnull, 'w')

    logging.info("Logging setup complete.")