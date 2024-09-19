import asyncio

import selenium.common.exceptions
from pydantic import BaseModel
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


class ResultItem(BaseModel):
    title: str
    keyword: str
    channel: str
    url: str


# async def bbc(keyword: str, channel: str) -> ResultItem | None:
#     query = f'https://www.bbc.com/search?q={keyword}'

#     driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
#     driver.get(query)

#     title = driver.find_element(By.NAME, 'h2')
#     print(title.text)


# async def main():
#     print(await bbc('Украина', 'rbcnews'))
#
# asyncio.run(main())