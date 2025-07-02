from botasaurus.soupify import soupify
from botasaurus.browser import browser, Driver, Wait
import requests
import re
import json


@browser(
    output=None,
    output_formats=None,
    create_error_logs=False,
    headless=True
)
def scraping_urls(driver: Driver, data: dict):
    page = 1
    urls = []
    while True:
        url = 'https://www.technodom.kz/search?recommended_by=instant_search&source=search&recommended_code=%D0%BC%D1%8B%D1%88%D1%8C&r46_search_query=%D0%BC%D1%8B%D1%88%D1%8C&r46_input_query=%D0%BC%D1%8B%D1%88%D1%8C&page={page}&price_min=&price_max=&rees46_search_filters=&rees46_search_categories=myshi'
        driver.get(url.format(page=page))
        driver.wait_for_element('[class*="ProductItem_itemLink"]', wait=Wait.LONG)

        soup = soupify(driver.page_html)
        check = soup.select('div[class*="CategoryPageList_titleWrapper"] p[class*="CategoryPageList_subtitle"]')

        if len(check) > 1:
            return urls

        links = soup.select('[class*="ProductItem_itemLink"]')

        for i in links:
            href = i.attrs.get('href', '')
            match = re.search(r"-(\d+)\?recommended_by", href)
            if match:
                urls.append(match.group(1))
        
        print('parsed page:', page )
        
        page += 1


def scraping_tech():

    mice = scraping_urls()
    data = []

    for mouse in mice:
        try:

            id = int(mouse)
            result = requests.get(f'https://api.technodom.kz/katalog/api/v2/products/{id}')
            attributes: dict = result.json()

            name = attributes.get('title')
            cashback_amount = attributes.get('cashback_amount')
            reviews = attributes.get('reviews')
            rating = attributes.get('rating')
            price = attributes.get('price')
            price_usd = attributes.get('price_usd')
            old_price = attributes.get('old_price')
            discount = attributes.get('discount')

            cur = attributes.get('attributes', [])

        
            main_attributes = next((attr.get('items', []) for attr in cur if attr.get('title') == 'Основные характеристики'), [])
            featured_attributes = next((attr.get('items', []) for attr in cur if attr.get('title') == 'Сенсор'), [])
            gabars_attributes = next((attr.get('items', []) for attr in cur if attr.get('title') == 'Габариты'), [])

            main = {char.get('title'): char.get('value') for char in main_attributes}
            features = {char.get('title'): char.get('value') for char in featured_attributes}
            gabars = {char.get('title'): char.get('value') for char in gabars_attributes}


            temp_data = {
                'Название': name,
                'Кешбек': cashback_amount,
                'Отзывы': reviews,
                'Рейтинг': rating,
                'Цена': price,
                'Цена в USD': price_usd,
                'Старая цена': old_price,
                'Скидка': discount,
                'Основные характеристики': main,
                'Дополнительные характеристики': features,
                'Габариты': gabars
            }
            data.append(temp_data)

            print('parsed mouse:',id)
        except Exception as e:
            print(e)
            
    with open('tech.json', 'w', encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False,indent=4)
    
scraping_tech()