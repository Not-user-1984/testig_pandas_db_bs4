import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download_xls.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)