import logging
from pathlib import Path


"""Logging utilities"""

def setup_logging(level=logging.INFO, log_to_file=True):
    """Set up logging configuration."""
    try:
        handlers = [logging.StreamHandler()]
        
        if log_to_file:
            # create logs directory if it doesn't exist in the project root
            project_root = Path(__file__).parent.parent.parent
            log_path = project_root / "logs"
            log_path.mkdir(exist_ok=True)
            handlers.append(logging.FileHandler(log_path / 'readtome.log'))
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=handlers,
            force=True  # Override any existing configuration
        )
        
    except Exception as e:
        # Fallback to console-only logging
        logging.basicConfig(level=level)
        logging.error(f"Failed to setup file logging: {e}")
def get_logger(name: str):
    """Get a logger with the specified name."""
    return logging.getLogger(name)

def log_tts_operation(operation: str, duration: float, **context):
    """Log TTS operation details."""
    logger = get_logger(__name__)
    context_str = ", ".join(f"{k}={v}" for k, v in context.items())
    logger.info(f"TTS: {operation} completed in {duration:.2f}s [{context_str}]")

def log_performance_metric(metric_name: str, value: float):
    """Log performance metrics."""
    logger = get_logger(__name__)
    logger.info(f"{metric_name}: {value}")