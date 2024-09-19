import asyncio

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
from selenium.common.exceptions import *
from utils.logging.logger import logger


channels = [
        'https://t.me/s/breakingmash',
        'https://t.me/s/ostorozhno_novosti',
        # 'https://t.me/s/rt_russian',
        'https://t.me/s/bbcrussian',
        'https://t.me/s/infantmilitario',
        'https://t.me/s/topor',
        # 'https://t.me/s/vestiru24',
        'https://t.me/s/mintsifry',
        'https://t.me/s/bbbreaking',
        'https://t.me/s/Match_TV',
        'https://t.me/s/sportsru'
]


async def async_generator(data):
    for item in data:
        await asyncio.sleep(0.05)
        yield item


async def telegram(keyword: str, channel: str) -> list[ResultItem | None]:
    driver = webdriver.Chrome(
        service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options)

    res_by_channels = []
    async for c in async_generator(channels):
        try:
            driver.get(c)
            sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            if keyword:
                keyword_in_text = False

                part_of_keyword = len(keyword) // 2
                keyword_forms = [
                    keyword.title(),
                    keyword.lower(),
                    keyword[:part_of_keyword],
                    keyword[:part_of_keyword].lower(),
                    keyword[part_of_keyword:]
                ]
            else:
                keyword_in_text = True
                # Допускаем любые новости
            try:
                wait = WebDriverWait(driver, 10)
                wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//*[starts-with(@class, 'tgme_widget_message_wrap')]")))

                posts = driver.find_elements(By.XPATH, "//*[starts-with(@class, 'tgme_widget_message_wrap')]")
                last_post_id = 0

                # Я не нашёл решения для получения последней новости,
                # поэтому пробежимся по списки и запишем в last_post
                async for p in async_generator(posts):
                    last_post = p

                    last_post_id = posts.index(p) + 1
                    last_post = p

                last_post = posts[last_post_id - 1]
                last_post_text = last_post.find_element(By.XPATH, "//*[starts-with(@class, 'tgme_widget_message_tex')]")
                not_clear_text = last_post_text.text

                link = last_post.find_element(By.XPATH, "//*[starts-with(@class, 'tgme_widget_message_da')]")
                link = link.get_attribute('href')

                async for word in async_generator(not_clear_text.split(' ')):
                    if word in keyword_forms:
                        # print(f'слово {word} совпало с {keyword}')
                        keyword_in_text = True

                if keyword_in_text:
                    full_text = '\n'.join([s for s in not_clear_text.split('\n') if 'Подписывайся' or 'Подписывайтесь' not in s])
                    res_by_channels.append(ResultItem(title=full_text, keyword=keyword, channel=channel, url=link))
                else:
                    res_by_channels.append(None)

                print('telegram parsed')

            except Exception as e:
                logger.error(e)
                res_by_channels.append(None)

        except:
            print(f'cant parse {c}')
            continue

    return res_by_channels

#
# async def main():
#     print(await telegram('в', 'rbcnews'))
#
# asyncio.run(main())