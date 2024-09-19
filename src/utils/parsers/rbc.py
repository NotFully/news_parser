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
    BeautifulSoup,
    sleep
)
from datetime import datetime
from selenium.common.exceptions import *
from utils.logging.logger import logger


async def rbc(keyword: str, channel: str) -> ResultItem | None:
    print(f'Начат парсинг сайтов {datetime.now()}')
    if keyword == 'политика':
        base_url = 'https://www.rbc.ru/politics/'

    elif keyword == 'бизнес':
        base_url = 'https://www.rbc.ru/business/'

    elif keyword == 'экономика':
        base_url = 'https://www.rbc.ru/economics/'

    elif keyword == 'мнения':
        base_url = 'https://www.rbc.ru/opinions/'

    elif keyword == 'технологии':
        base_url = 'https://www.rbc.ru/technology_and_media/'

    elif keyword == 'медиа':
        base_url = 'https://www.rbc.ru/technology_and_media/'

    elif keyword == 'финансы':
        base_url = 'https://www.rbc.ru/finances/'

    elif keyword == 'свое дело':
        base_url = 'https://www.rbc.ru/finances/'
    else:
        base_url = None

    if base_url is not None:
        try:
            # Если слово понятное - ищем по рубрикам
            site = requests.get(base_url)
            soup = BeautifulSoup(site.content, 'html.parser')
            title = soup.find('span', class_='normal-wrap').text.strip()
            link = soup.find('a', class_='item__link rm-cm-item-link js-rm-central-column-item-link').get('href')
            return ResultItem(title=title, url=link, keyword=keyword, channel=channel)
        except AttributeError as e:
            logger.error(e)
    else:
        try:
            now_date = datetime.now().strftime('%d.%m.%Y')
            query = f'https://www.rbc.ru/search/?query={keyword}&dateFrom={now_date}&dateTo={now_date}'
            driver = webdriver.Chrome(
                service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                options=options)
            driver.get(query)
            # ждем 3 сек, т.к рбк загружает новости
            sleep(3)

            title = driver.find_element(By.CLASS_NAME, "search-item__title ")
            title = title.text

            links = driver.find_elements(By.CSS_SELECTOR, ".search-item__link.js-search-item-link")
            links = [l.get_attribute('href') for l in links]
            link = (links[0])

            driver.quit()
            return ResultItem(title=title, url=link, keyword=keyword, channel=channel)
        except NoSuchElementException:
            try:
                # пробуем ещё раз
                now_date = datetime.now().strftime('%d.%m.%Y')
                query = f'https://www.rbc.ru/search/?query={keyword}&dateFrom={now_date}&dateTo={now_date}'
                driver = webdriver.Chrome(
                    service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                    options=options)
                driver.get(query)
                # ждем 3 сек, т.к рбк загружает новости
                sleep(3)

                title = driver.find_element(By.CLASS_NAME, "search-item__title ")
                title = title.text

                links = driver.find_elements(By.CSS_SELECTOR, ".search-item__link.js-search-item-link")
                links = [l.get_attribute('href') for l in links]
                link = (links[0])

                driver.quit()

                print('rbc parsed')

                return ResultItem(title=title, url=link, keyword=keyword, channel=channel)
            except NoSuchElementException as e:
                logger.error(e)
            except Exception as e:
                logger.error(e)
        except Exception as e:
            logger.error(e)


# async def main():
#     print(await rbc('Украина', 'rbcnews'))
#
# asyncio.run(main())