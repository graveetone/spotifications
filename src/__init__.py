from loguru import logger
import sys

logger.remove()

log_format = "<green>{time}</green> | <level>{level}</level> | <level>{message}</level>"
logger.add(sys.stderr, level="ERROR", format=log_format)
logger.add(sys.stdout, level="DEBUG", format=log_format)
# logger.add("logs/spotifications.log", level="DEBUG", format=log_format)
