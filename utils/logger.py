"""
Logging utility for Career Advisor Chatbot.

Provides centralized logging with both file and console output.
Handles error tracking and application flow monitoring.
"""

import logging
import logging.handlers
from logging import Formatter
from config import Config


class ChatbotLogger:
    """
    Centralized logger for the Career Advisor Chatbot application.
    
    Provides structured logging with timestamps, log levels, and module tracking.
    Outputs logs to both console and file.
    """
    
    _logger = None
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: The name of the logger (usually __name__ from the calling module).
            
        Returns:
            logging.Logger: Configured logger instance.
        """
        if ChatbotLogger._logger is None:
            ChatbotLogger._initialize_logger()
        
        return logging.getLogger(name)
    
    @staticmethod
    def _initialize_logger():
        """
        Initialize the logger with handlers and formatters.
        
        Configures both file handler and console handler.
        Sets appropriate log levels and formatting.
        """
        # Create main logger
        logger = logging.getLogger("chatbot")
        log_level = getattr(logging, Config.LOG_LEVEL, logging.INFO)
        logger.setLevel(log_level)
        
        # Clear any existing handlers
        logger.handlers = []
        
        # Create formatter
        formatter = Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                Config.LOG_FILE,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Failed to configure file handler: {e}")
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        ChatbotLogger._logger = logger
    
    @staticmethod
    def log_api_call(model: str, input_length: int, output_length: int = 0):
        """
        Log API call details for monitoring and debugging.
        
        Args:
            model: The model name used.
            input_length: Number of input tokens.
            output_length: Number of output tokens.
        """
        logger = ChatbotLogger.get_logger(__name__)
        logger.debug(
            f"API Call - Model: {model}, Input Tokens: {input_length}, "
            f"Output Tokens: {output_length}"
        )
    
    @staticmethod
    def log_error(error_type: str, error_message: str, traceback_info: str = ""):
        """
        Log error information with context.
        
        Args:
            error_type: Type of error (e.g., APIError, ValidationError).
            error_message: Detailed error message.
            traceback_info: Optional traceback information.
        """
        logger = ChatbotLogger.get_logger(__name__)
        logger.error(
            f"{error_type}: {error_message}\n{traceback_info}" if traceback_info
            else f"{error_type}: {error_message}"
        )
    
    @staticmethod
    def log_user_interaction(user_message: str, response_length: int):
        """
        Log user interactions for audit trail and debugging.
        
        Args:
            user_message: The user's message.
            response_length: Length of the bot's response.
        """
        logger = ChatbotLogger.get_logger(__name__)
        logger.info(
            f"User Interaction - Message Length: {len(user_message)}, "
            f"Response Length: {response_length}"
        )
