import requests
import cloudscraper
from bs4 import BeautifulSoup
import json
import time

scraper = cloudscraper.create_scraper()

url = 'https://www.dns-shop.kz/catalog/17a892f816404e77/noutbuki/?p={page}'
page = 18
aboba = []

while True:
    current_url=url.format(page=page)

    response = scraper.get(current_url)
    if not response.ok:
        print(response.status_code)
        print(current_url)
        break
        
    soup = BeautifulSoup(response.text)

    data = soup.select('div.catalog-product__name-wrapper a span')

    if not data:
        break

    for i in data:
        note = i.text
        try:
            
            model, temp = note.split('[')
        except Exception:
            print(note)
            print(current_url)

        chars = list(map(lambda x: x.strip(), temp.replace(']','').split(',')))

        try:
            data = {
                'model_name' : model,
                'resolution': chars[1],
                'screen': chars[2],
                'CPU name': chars[3],
                'CPU cores': chars[4].replace('ядра: ', ''),
                'RAM': chars[5].replace('RAM ',''),
                'storage': chars[6],
                'GPU': chars[7],
                'OS': chars[8]
            }
        except IndexError:
            continue

        aboba.append(data)
    print(f'Parsed: {current_url}')
    page+=1
    time.sleep(5)

with open('dns_parsed.json', 'a', encoding='utf-8') as file:
    json.dump(aboba, file, ensure_ascii=False, indent= 4)


