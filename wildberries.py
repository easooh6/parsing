import requests
from bs4 import BeautifulSoup
from botasaurus.browser import browser, Driver, Wait
from botasaurus.soupify import soupify
from botasaurus.request import request, Request
import json

url = 'https://www.wildberries.ru/catalog/0/search.aspx?page={page}&sort=popular&search=%D0%BA%D0%BE%D1%84%D0%B5'

# response = requests.get(url)



# # with open('wild.html','w',encoding='utf-8') as file:
# #     file.write(response.text)


# selector_url = '.product-card__link.j-card-link.j-open-full-product-card'

# soup = BeautifulSoup(response.text, 'html.parser')

# parsed_url = soup.select_one('.product-card__link.j-card-link.j-open-full-product-card')
# print(response)
# print(parsed_url)

@browser(
        close_on_crash=True,
        output=None,
        output_formats=None,
        create_error_logs=None,
        headless=True
)
def scrape_wild(driver: Driver, data: dict):
    #driver.block_images_and_css()
    url = 'https://www.wildberries.ru/catalog/0/search.aspx?page={page}&sort=popular&search=%D0%BA%D0%BE%D1%84%D0%B5'
    page = 1
    while page < 2:
        driver.get(url.format(page=page))
        try:
            driver.wait_for_element('.product-card__link.j-card-link.j-open-full-product-card',wait=Wait.LONG)
        except Exception as e:
            print(e)
            return
        soup = soupify(driver.page_html)

        result = soup.select('.product-card__link.j-card-link.j-open-full-product-card')
        
        parsed_urls = [i.attrs.get('href') for i in result]
        
        output_data=[]
        for _url in parsed_urls:
            driver.get(_url)
            #driver.scroll_to_bottom()
            try:
                driver.wait_for_element('div.product-page__grid')
            except Exception as e:
                print(e)
                break
            
            soup = soupify(driver.page_html)
            price = 0
            red_price = soup.select_one('div.product-page__grid span.price-block__wallet-price.red-price')
            if red_price:
                price=red_price
            else:
                price = soup.select_one('div.product-page__grid .price-block__final-price.wallet')
            description = soup.select_one('.product-params__table')

            description_left = description.select('.product-params__table th.product-params__cell')

            description_right = description.select('.product-params__table td.product-params__cell')

            left = [i.text.strip() for i in description_left]
            left.append('price')

            right = [i.text.strip() for i in description_right]
            right.append(price.text.replace('\xa0',''))
    
            product = dict(zip(left,right))
            output_data.append(product)

            driver.short_random_sleep()

            print('parsed:', _url)
        page +=1

    with open('wild.json','w',encoding='utf-8') as file:
        json.dump(output_data,file,ensure_ascii=False,indent=4)
    


scrape_wild()


