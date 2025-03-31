import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure the logger
def setup_logger():
    """
    Set up and configure the frontend error logger.
    """
    # Create a logger instance
    logger = logging.getLogger('frontend_logger')
    logger.setLevel(logging.DEBUG)
    
    # Create a file handler
    log_file = os.path.join(logs_dir, f'frontend_errors_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger
frontend_logger = setup_logger()

def log_frontend_error(error_type: str, error_message: str, additional_info: dict = None):
    """
    Log frontend errors with detailed information.
    
    Args:
        error_type (str): Type of error (e.g., 'Arrow Conversion', 'Model Training', etc.)
        error_message (str): The error message
        additional_info (dict, optional): Additional context about the error
    """
    error_details = f"Type: {error_type}\nMessage: {error_message}"
    if additional_info:
        error_details += f"\nAdditional Info: {additional_info}"
    
    frontend_logger.error(error_details)

def log_frontend_warning(warning_type: str, warning_message: str, additional_info: dict = None):
    """
    Log frontend warnings with detailed information.
    
    Args:
        warning_type (str): Type of warning
        warning_message (str): The warning message
        additional_info (dict, optional): Additional context about the warning
    """
    warning_details = f"Type: {warning_type}\nMessage: {warning_message}"
    if additional_info:
        warning_details += f"\nAdditional Info: {additional_info}"
    
    frontend_logger.warning(warning_details) 