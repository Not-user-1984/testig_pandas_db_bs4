import logging
import os
from utils import get_output_path
from config import LOG_SAVE_DIR

base_path = os.path.abspath(os.path.dirname(__file__))

# Получаем путь для сохранения файла
output_path = get_output_path(base_path, LOG_SAVE_DIR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(output_path), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
