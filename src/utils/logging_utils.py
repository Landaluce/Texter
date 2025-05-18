from logging_config import setup_logging
import logging

setup_logging()
info_logger = logging.getLogger('general_logger')
error_logger = logging.getLogger('error_logger')
warning_logger = logging.getLogger('warning_logger')