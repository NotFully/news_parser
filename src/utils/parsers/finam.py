from . import ResultItem, webdriver, ChromiumService, ChromeDriverManager, ChromeType, Options, WebDriverWait, EC, By, options
from utils.logging.logger import logger


async def finam(keyword: str, channel: str) -> ResultItem | None:
    base_url = None
    match keyword:
        case 'криптовалюты':
            try:
                query = 'https://www.finam.ru/publications/section/cryptonews/'
                driver = webdriver.Chrome(
                    service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options))
                driver.get(query)

                wait = WebDriverWait(driver, 1)
                link_element = wait.until(EC.presence_of_element_located((
                    By.XPATH, "//a[starts-with(@href, '/publications/item/') and contains(@class, 'cl-blue font-l bold')]")
                ))

                news_link = link_element.get_attribute("href")

                driver.get(news_link)
                title = driver.find_element(By.XPATH, "//*[starts-with(@id, 'finfin-local-plugin-publication-item-item-')]")
                title = title.text.split('\n')[3]

                print('finam parsed')

                return ResultItem(title=title, keyword=keyword, channel=channel, url=news_link)
            except Exception as e:
               logger.error(e)
#
# async def main():
#     print(await finam('криптовалюты', 'rbcnews'))
#
# asyncio.run(main())