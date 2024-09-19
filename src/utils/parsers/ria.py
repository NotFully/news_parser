from . import (
    ResultItem,
    webdriver,
    ChromiumService,
    ChromeDriverManager,
    ChromeType,
    options,
    WebDriverWait,
    EC,
    By,
    sleep,
    selenium,
    requests,
    BeautifulSoup
)
from selenium.common.exceptions import *
from utils.logging.logger import logger


async def ria(keyword: str, channel: str) -> ResultItem | None:
    base_url = None
    match keyword:
        case 'политика':
            base_url = 'https://ria.ru/politics/'
        case 'в мире':
            base_url = 'https://ria.ru/world/'
        case 'экономика':
            base_url = 'https://ria.ru/economics/'
        case 'общество':
            base_url = 'https://ria.ru/society/'
        case 'происшествия':
            base_url = 'https://ria.ru/incidents/'
        case 'армия':
            base_url = 'https://ria.ru/defense_safety/'
        case 'наука':
            base_url = 'https://ria.ru/science/'
        case 'спорт':
            base_url = 'https://rsport.ria.ru/'
            site = requests.get(base_url)
            soup = BeautifulSoup(site.content, 'html.parser')
            title = soup.find('span', class_='cell-list__item-title').text.strip()
            link = soup.find('a', class_='cell-list__item-link color-font-hover-only').get('href')
            return ResultItem(title=title, url=link, keyword=keyword, channel=channel)
        case 'культура':
            base_url = 'https://ria.ru/culture/'
        case 'религия':
            base_url = 'https://ria.ru/religion/'
        case 'туризм':
            base_url = 'https://ria.ru/tourism/'

    if base_url is not None:
        try:
            site = requests.get(base_url)
            soup = BeautifulSoup(site.content, 'html.parser')
            title = soup.find('a', class_='list-item__title color-font-hover-only').text.strip()
            link = soup.find('a', class_='list-item__title color-font-hover-only').get('href')
            return ResultItem(title=title, url=link, keyword=keyword, channel=channel)
        except AttributeError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
    else:
        try:
            base_url = f'https://ria.ru/search/?query={keyword}'
            site = requests.get(base_url)
            soup = BeautifulSoup(site.content, 'html.parser')

            title = soup.find('a', class_='list-item__title color-font-hover-only').text.strip()
            if 'Главные темы часа' not in title:
                link = soup.find('a', class_='list-item__title color-font-hover-only').get('href')

                print('ria parsed')

                return ResultItem(title=title, url=link, keyword=keyword, channel=channel)
            else:
                next_title = soup.findNext('a', class_='list-item__title color-font-hover-only').text.strip()
                next_link = soup.findNext('a', class_='list-item__title color-font-hover-only').get('href')

                print('ria parsed')

                return ResultItem(title=next_title, url=next_link, keyword=keyword, channel=channel)
        except AttributeError as e:
            logger.error(e)
            # print(f'В обход установленных слов ничего не найдено по слову {keyword} :(')
        except Exception as e:
            logger.error(e)
#
# async def main():
#     print(await ria('госдума', 'rbcnews'))
#
# asyncio.run(main())