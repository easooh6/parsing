import requests
from bs4 import BeautifulSoup
import json
import time
from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify

krisha = 'https://krisha.kz/arenda/kvartiry/almaty/?das[live.rooms][0]=1&das[live.rooms][1]=2&das[who]=1&rent-period-switch=%2Farenda%2Fkvartiry&page={page}'



@browser(block_images_and_css=True,
         headless=True,
         close_on_crash=True,
         output=None,
         output_formats=None,
         create_error_logs=None)
def krisha_scrapper(driver: Driver, data):
    parsed = []
    page = 1
    while page < 2:
            
        driver.get(krisha.format(page=page))

        soup = soupify(driver.page_html)

        select = soup.select('.a-card__header-left a')

        urls = ['https://krisha.kz' + i.attrs.get('href') for i in select]
        
        for url in urls:

            driver.get(url)

            soup = soupify(driver.page_html)

            name = soup.select('.offer__advert-title h1')
            green_price = soup.select('.green-price')
            green_text = soup.select('.first:nth-child(1) small')

            blue_price = soup.select('.middle .blue-price')
            blue_text= soup.select('.middle small')


            base= {
                'name': name[0].text.strip(),
                'url': url,
                green_text[0].text.strip(): green_price[0].text.strip(),
                blue_text[0].text.strip(): blue_price[0].text.strip()

            }

            left = soup.select('.offer__info-title')
            chars = [i.text.strip() for i in left]
            
            right = soup.select('.offer__advert-short-info')
            description = [i.text.strip() for i in right]
            

            apartment = dict(zip(chars,description))

            apartment.update(base)

            parsed.append(apartment)
            
            print('parsed url:', url)
            driver.short_random_sleep()

        page+=1
        print('parsed page:', page)

    with open('krisha.json', 'w', encoding='utf-8') as file:
        json.dump(parsed,file,ensure_ascii=False, indent=4)

krisha_scrapper()