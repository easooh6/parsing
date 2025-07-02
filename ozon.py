import requests
import cloudscraper
import time
from botasaurus.browser import Driver, browser
from botasaurus.soupify import soupify
from botasaurus.request import request,Request
import json 

# scraper = cloudscraper.create_scraper(
#     browser={
#         'browser': 'chrome',
#         'platform': 'linux',
#         'desktop': True
#     }
# )

# headers = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Referer': 'https://www.ozon.ru/',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Cache-Control': 'max-age=0'
# }

# # Add a small delay to avoid triggering rate limits
# time.sleep(2)
# result = scraper.get(url='https://www.ozon.ru/category/naushniki-15547/',headers=headers)
# print(result.status_code)

@browser(
    headless=False,
    close_on_crash=True,
    output=None,
    output_formats=None,
    create_error_logs=None,
    block_images_and_css=True
)
def getting_urls(driver: Driver, data):
    driver.enable_human_mode()
    driver.google_get('https://ozon.kz/category/chulki-zhenskie-36472/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=%D1%87%D1%83%D0%BB%D0%BA%D0%B8')
    driver.short_random_sleep()
    links=[]

    while len(links) < 100:
        driver.scroll_to_bottom()
        
        links.append(driver.select('.rj7_25.tile-root.j9w_25.xj_25 a[href]:nth-child(1)'))

    soup = soupify(driver.page_html)
    links = soup.select('.rj7_25.tile-root.j9w_25.xj_25 a[href]:nth-child(1)')
    parsed_urls = ['https://ozon.kz' + i.attrs.get('href') for i in links]
    return parsed_urls


@browser(
    headless=False,
    close_on_crash=True,
    output=None,
    output_formats=None,
    create_error_logs=None
)
def parsing_urls(driver: Driver, data):
    urls = getting_urls()
    data = []
    print(len(urls))
    for url in urls:
        driver.google_get(url)
        driver.short_random_sleep()
        driver.scroll_to_bottom()
        try:
            driver.wait_for_element('.p4m_28.p5m_28.p3m_28.mp5_28')
        except Exception as e:
            print(e)
            continue
        soup = soupify(driver.page_html)
        
        price = 0
        short_price = soup.select_one('.m5p_28.pm5_28.p9m_28')
        if short_price:
            price = short_price.text.replace('&thinsp;', '')
        else:
            price = soup.select_one('.p4m_28.p5m_28.p3m_28.mp5_28')
            price = price.text.replace('&thinsp;', '')
        
        left = soup.select('.kv8_28')
        
        chars = [i.text.strip() for i in left]
        chars.append('Цена')

        right = soup.select('.k8v_28')

        description = [i.text.strip() for i in right]
        description.append(price)


        stocking = dict(zip(chars,description))
        data.append(stocking)

       
        
        print('parsed url:', url)

    with open('ozon.json','w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False,indent=4)

parsing_urls()