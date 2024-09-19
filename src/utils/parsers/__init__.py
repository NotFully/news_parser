import asyncio
import selenium
import requests
from time import sleep
from pydantic import BaseModel
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--headless")  # Запуск в безголовом режиме
options.add_argument("--no-sandbox")  # Отключение песочницы
options.add_argument("--disable-dev-shm-usage")  # Использование /tmp вместо /dev/shm
options.add_argument("--disable-gpu")  # Отключение графического процессора (если используется)


class ResultItem(BaseModel):
    title: str
    keyword: str
    channel: str
    url: str
