import time
import argparse
from logger_config import logger

from parse import main as parse_main
from download_xls import main as download_main
from to_results_csv import main as results_main


def run_stage(stage_name, stage_function):
    """
    Запускает указанный этап парсинга и логирует время его выполнения.
    """
    logger.info(f"Начало этапа: {stage_name}")
    start_time = time.time()

    # Запуск этапа
    stage_function()

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Завершение этапа: {stage_name}. Время выполнения: {elapsed_time:.2f} секунд.")


def main():
    """
    Основная функция для запуска всех этапов парсинга.
    """
    parser = argparse.ArgumentParser(description="Запуск этапов парсинга.")
    parser.add_argument(
        "--stage",
        choices=["parse", "download", "results", "all"],
        default="all",
        help="Выберите этап для запуска: parse, download, results или all (по умолчанию)."
    )
    args = parser.parse_args()

    if args.stage == "parse" or args.stage == "all":
        run_stage("Парсинг ссылок на XLS-файлы", parse_main)

    if args.stage == "download" or args.stage == "all":
        run_stage("Скачивание XLS-файлов", download_main)

    if args.stage == "results" or args.stage == "all":
        run_stage("Обработка XLS-файлов и сохранение результатов", results_main)

    if args.stage == "all":
        logger.info("Все этапы парсинга завершены.")


if __name__ == "__main__":
    main()