import os
import logging
import requests
import traceback
from datetime import datetime


class MyLogger():
    def __init__(self) -> None:
        self.create_log_dir()

        today = datetime.now().strftime('%d_%m_%Y')
        log_file_path = os.path.join('logs', f'{today}.txt')

        logging.basicConfig(
            filename=f'{log_file_path}',
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def create_log_dir(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')
            print("Папка 'logs' успешно создана")

    def info(self, message: str, ) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        error_type = type(message).__name__
        error_message = str(message)
        traceback_info = traceback.format_exc()
        self.logger.error(f'{error_type} - {error_message}:\n{traceback_info}')

    def critical(self, message: str) -> None:
        error_type = type(message).__name__
        error_message = str(message)
        traceback_info = traceback.format_exc()
        self.logger.critical(f'{error_type} - {error_message}:\n{traceback_info}')


logger = MyLogger()
logger.info(f'Логгер активирован')

# try:
#     2/0
# except Exception as e:
#     logger.error(e)