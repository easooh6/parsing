from botasaurus.browser import browser, Driver, Wait
from botasaurus.soupify import soupify
from botasaurus.user_agent import UserAgent
import time
import json
import re

@browser(headless=False,
         close_on_crash=False,
         output=None,
         output_formats=None,
         create_error_logs=None,
         profile='Profile1',
         tiny_profile=True)
def kinopoisk_scrapper(driver: Driver, data):
    page = 1
    total  = []
    while page < 2:

        kino = 'https://www.kinopoisk.ru/lists/movies/top250/?page={page}'

        driver.google_get(kino.format(page=page))
        driver.short_random_sleep()

        soup = soupify(driver.page_html)

        links = soup.select('a[class*="base-movie-main-info_link"]')

        urls = ['https://www.kinopoisk.ru/' + i.attrs.get('href') for i in links]


        for url in urls:
            driver.google_get(url)
            driver.scroll_to_bottom()
            driver.short_random_sleep()

            soup = soupify(driver.page_html)

            temporary = soup.select_one('h1[itemprop*="name"] span')

            match = re.match(r"^(?P<title>.+?) \((?P<year>\d{4})\)$", temporary.text.strip())

            if match:
                name=  match.group("title")
                year = match.group("year")
            

            total_rank = soup.select_one('span[class*="styles_rating"]')
            rates_count = soup.select_one('span[class*="styles_count"]')
            
            data  = {
                'name': name,
                'year': year,
                'total_rank': total_rank.text.strip(),
                'rates_count': rates_count.text.strip(),
                'url': url
            }
            total.append(data)

        page += 1
    
    with open('kinopoisk.json','w',encoding='utf-8') as file:
        json.dump(total,file,ensure_ascii=False,indent=4)

        


kinopoisk_scrapper()