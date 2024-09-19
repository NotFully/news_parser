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
from utils.logging.logger import logger


async def gazeta(keyword: str, channel: str) -> ResultItem | None:
    base_url = None
    match keyword:
        case 'спорт':
            base_url = 'https://www.gazeta.ru/sport/'
        case 'политика':
            base_url = 'https://www.gazeta.ru/politics/'
        case 'бизнес':
            base_url = 'https://www.gazeta.ru/business/'
        case "общество":
            base_url = 'https://www.gazeta.ru/social/'
        case 'армия':
            base_url = 'https://www.gazeta.ru/army/'
        case 'культура':
            base_url = 'https://www.gazeta.ru/culture/'
        case 'наука':
            base_url = 'https://www.gazeta.ru/science/'
        case 'семья':
            base_url = 'https://www.gazeta.ru/family/'
        case 'технологии':
            base_url = 'https://www.gazeta.ru/tech/'
        case 'авто':
            base_url = 'https://www.gazeta.ru/auto/'
        case 'стиль':
            base_url = 'https://www.gazeta.ru/style/'
    if base_url is not None:
        try:
            site = requests.get(base_url)
            soup = BeautifulSoup(site.content, 'html.parser')

            link = soup.find('a', class_='b_ear m_simple').get('href')
            title = soup.find('div', class_='b_ear-title').text.strip()

            print('gazeta parsed')

            return ResultItem(title=title, url='https://www.gazeta.ru' + link, keyword=keyword, channel=channel)
        except Exception as e:
            logger.error(e)
    else:
        try:
            base_url = f'https://www.gazeta.ru/search.shtml?text={keyword}&p=main&input=utf8'
            site = requests.get(base_url)
            soup = BeautifulSoup(site.content, 'html.parser')
            ear_title_div = soup.find('div', class_='b_ear-title')
            title = ear_title_div.text.strip()
            link = ear_title_div.find('a').get('href')

            print('gazeta parsed')

            return ResultItem(title=title, url='https://www.gazeta.ru' + link, keyword=keyword, channel=channel)
        except AttributeError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)

# async def main():
#     print(await gazeta('Путин', 'rbcnews'))
#
# asyncio.run(main())