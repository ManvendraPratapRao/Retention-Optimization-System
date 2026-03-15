import logging
import sys

# Configure a detailed format for production clarity
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(filename)s:%(lineno)d - %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("churn-api")