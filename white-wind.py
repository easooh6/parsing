import requests
import cloudscraper
from bs4 import BeautifulSoup
import json
from botasaurus.soupify import soupify
from botasaurus.browser import browser, Driver, Wait

scraper = cloudscraper.create_scraper()

url = 'https://sort.diginetica.net/search?apiKey=Z72L941338&strategy=advanced_xname%2Czero_queries&fullData=true&withCorrection=true&withFacets=true&treeFacets=true&useCategoryPrediction=false&withSku=false&useCompletion=true&showUnavailable=true&unavailableMultiplier=0.2&size=40&regionId=global&st=%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80&lang=ru&sort=DEFAULT&offset={page}&filter=categories:195'

full_data = []

urls = []

def scratch_urls():
    page = 0

    while True:
        try:
            response = scraper.get(url.format(page=page))

            data = response.json()

            products = data.get('products')

            if not products:
                print('parsed urls number:', len(urls))
                return urls
            
            for product in products:
                urls.append('https://shop.kz' + product.get('link_url'))

            print('parsed page:', page)
            page += 40

        except Exception as e:
            print(e)
            return urls
@browser(
    output=None,
    output_formats=None,
    create_error_logs=False,
    headless=True
)
def scratch_monitors(driver: Driver, data: dict):

    data_urls = scratch_urls()

    i = 0
    try:
        for url in data_urls:

            if i > 50:
                break
            
            driver.get(url)

            try:
                driver.wait_for_element('.dotted-item.left .dotted-item__title')
            except Exception as e:
                print(e)

            soup = soupify(driver.page_html)
            
            if soup.select('bx_notavailable'):
                continue

            chars_left = soup.select('.dotted-item.left .dotted-item__title')
            new_chars_left = [chars_l.text.strip() for chars_l in chars_left ]
            chars_right = soup.select('.dotted-item.left .dotted-item__value')
            new_chars_right = [chars_r.text.strip() for chars_r in chars_right ]

            temp_data = dict(zip(new_chars_left,new_chars_right))

            producer = temp_data.get('Производитель')
            model = temp_data.get('Модель')
            type_model = temp_data.get('Тип поверхности экрана')
            type_matrix = temp_data.get('Тип матрицы')
            diagonal_screen = temp_data.get('Диагональ экрана, дюйм')
            aspect_ratio = temp_data.get('Соотношение сторон')
            maximum_resolution = temp_data.get('Максимальное разрешение')
            frequency = temp_data.get('Частота при максимальном разрешении, Гц')
            brightness = temp_data.get('Яркость, кд/м2')
            pixel_response_time = temp_data.get('Мин. время отклика пикселя, мс')
            connection_interface = temp_data.get('Интерфейс подключения')
            power_consumption = temp_data.get('Потребляемая мощность (максимальная), Вт')
            dimensions = temp_data.get('Размеры (Ш х В х Г)')
            weight  = temp_data.get('Вес изделия')

            rate = soup.select_one('.d-flex.flex-gap-4 .bxcm-rd')
            article = soup.select_one('.article-value')
            price = soup.select_one('.item_current_price')
            name = soup.select_one('.bx-title.dbg_title')

            data = {
                'url': url,
                'Название': name.text.strip() if name else None,
                'Производитель': producer,
                'Модель': model,
                'Артикль': article.text.strip() if article else None,
                'Цена': price.text.strip() if price else None,
                'Рейтинг': rate.text.strip() if rate else None,
                'Тип поверхности экрана': type_model,
                'Тип матрицы': type_matrix,
                'Диагональ экрана, дюйм': diagonal_screen,
                'Соотношение сторон': aspect_ratio,
                'Максимальное разрешение': maximum_resolution,
                'Частота при максимальном разрешении, Гц': frequency,
                'Яркость, кд/м2': brightness,
                'Мин. время отклика пикселя, мс': pixel_response_time,
                'Интерфейс подключения': connection_interface,
                'Потребляемая мощность (максимальная), Вт': power_consumption,
                'Размеры (Ш х В х Г)': dimensions,
                'Вес изделия': weight
            }
            full_data.append(data)
            i+=1

            print('parsed url:', url)
    except Exception as e:
        print(e)
    
    with open('white.json', 'w', encoding='utf-8') as file:
        json.dump(full_data,file,indent=4,ensure_ascii=False)

scratch_monitors()

    