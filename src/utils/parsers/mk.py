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
from utils.logging.logger import logger


async def mk(keyword: str, channel: str) -> ResultItem | None:
    try:
        query = f'https://www.mk.ru/search/?q={keyword}'
        driver = webdriver.Chrome(
            service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
            options=options)
        driver.get(query)

        title = driver.find_element(By.CLASS_NAME, 'listing-preview__title')
        title = title.text
        link = driver.find_element(By.CLASS_NAME, 'listing-preview__content')
        link = link.get_attribute('href')

        print('mk parsed')

        return ResultItem(title=title, keyword=keyword, channel=channel, url=link)
    except NoSuchElementException as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)


# async def main():
#     print(await mk('Культура', 'rbcnews'))
#
# asyncio.run(main())