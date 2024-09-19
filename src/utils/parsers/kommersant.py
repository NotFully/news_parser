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
from utils.logging.logger import logger


async def kommersant(keyword: str, channel: str) -> ResultItem | None:
    try:
        query = f'https://www.kommersant.ru/search/results?search_query={keyword}&sort_type=0&search_full=1'
        driver = webdriver.Chrome(
            service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
            options=options)
        driver.get(query)

        link = driver.find_element(By.XPATH, '/html/body/main/div/div/section/div[1]/div[4]/article[1]/div/h2/a')
        link = link.get_attribute('href')
        title = driver.find_element(By.XPATH, '/html/body/main/div/div/section/div[1]/div[4]/article[1]/div/h2/a/span')
        title = title.text

        driver.quit()

        print('kommersant parsed')

        return ResultItem(title=title, keyword=keyword, channel=channel, url=link)
    except Exception as e:
        logger.error(e)


# async def main():
#     print(await kommersant('Москва', 'rbcnews'))

# asyncio.run(main())