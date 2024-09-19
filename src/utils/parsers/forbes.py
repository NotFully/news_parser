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


async def forbes(keyword: str, channel: str) -> ResultItem | None:
    query = 'https://www.forbes.ru/search'
    try:
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
        driver.get(query)

        search_button = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div/div/main/div/div/div/div/form/div/label/input')
        if search_button.get_attribute('placeholder') == 'Поиск материала...':
            search_button.send_keys(keyword)
            search_button.submit()

            sleep(3)  # ждем прогрузку

            times_button = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div/div/main/div/div/div/div[1]/div/div[2]/label')
            times_button.click()
            sleep(1.3)  # кликаем по списки дат с разным временем

            sort_by_day_button = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div/div/main/div/div/div/div[1]/div/div[2]/div/ul/li[2]/label')
            sort_by_day_button.click()  # выбираем за сегодня новости
            sleep(1.8)  # выбираем по дате разным временем

            search_button.submit()  # ищем заново, но с датой

            wait = WebDriverWait(driver, 10)
            # Поиск элемента <a> с ссылкой, начинающейся с "/milliardery/"
            link_element = wait.until(EC.presence_of_element_located((
                By.XPATH, "//a[starts-with(@href, '/milliardery/')]/h3"
            )))
            news_url = link_element.find_element(By.XPATH, "..").get_attribute(
                "href")

            driver.get(news_url)  # переходим на новость
            title = driver.find_element(By.XPATH, '//*[@id="article_519838"]/div/div[1]/div[2]/h1')
            title = title.text

            print('forbes parsed')

            return ResultItem(title=title, keyword=keyword, channel=channel, url=news_url)
    except NoSuchElementException as e:
        logger.error(e)
        # print('не найден по элементу, возможно за сегодня такой новости нету :(')
    except TimeoutException as e:
        logger.error(e)
        # print('не найден по элементу, возможно за сегодня такой новости нету :(')
    except Exception as e:
        logger.error(e)


# async def main():
#     print(await forbes('Дуров', 'rbcnews'))
#
# asyncio.run(main())