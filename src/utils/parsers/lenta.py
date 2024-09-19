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
    selenium
)
from selenium.common.exceptions import *
from datetime import datetime

from utils.logging.logger import logger


async def lenta(keyword: str, channel: str) -> ResultItem | None:
    now_date = datetime.now().strftime('%Y-%m-%d')
    try:
        query = f'https://lenta.ru/search?query={keyword}#size=10|sort=2|domain=1|modified,format=yyyy-MM-dd|type=1|modified,from={now_date}|modified,to={now_date}'
        driver = webdriver.Chrome(
            service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
            options=options)
        driver.get(query)

        title = driver.find_element(By.CLASS_NAME, 'card-full-news__title')

        link = driver.find_element(By.XPATH, '//*[@id="body"]/div[3]/div[3]/main/div[2]/section/div[1]/ul/li[1]/a')
        link = link.get_attribute('href')

        print('lenta parsed')

        return ResultItem(title=title.text, keyword=keyword, channel=channel, url=link+'.html')
    except NoSuchElementException as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)


# async def main():
#     print(await lenta('биткойн', 'rbcnews'))
#
# asyncio.run(main())
