# from . import ResultItem, requests, BeautifulSoup
import asyncio


from pydantic import BaseModel
from datetime import datetime, timedelta
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By


class ResultItem(BaseModel):
    title: str
    keyword: str
    channel: str
    url: str


async def yahoo(keyword: str, channel: str) -> ResultItem | None:
    from bs4 import BeautifulSoup
    import requests
    try:
        base_url = f'https://news.search.yahoo.com/search;_ylt={keyword}'
        soup = BeautifulSoup(requests.get(base_url).text, 'lxml')
        item = soup.find('img', class_='s-img')
        title = item.get('alt')

        link = soup.find('h4', class_='s-title fz-16 lh-20')
        link = link.find('a').get('href')

        print('yahoo parsed')

        return ResultItem(title=title, keyword=keyword, channel=channel, url=link)
    except AttributeError:
        print('не найден по элементу, возможно рбк не загрузил новости :(')
        return None
    except Exception as e:
        print(f'ошибка: {e}')

    #
# async def main():
#     print(await yahoo('Путин', 'rbcnews'))
#
# asyncio.run(main())