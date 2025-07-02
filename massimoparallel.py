from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
import json
import re
import requests


@browser(create_error_logs=None,
         output=None,
         output_formats=None,
         headless=False,
         parallel=5,
         max_retry=5)
def parse_product(driver: Driver, url: str):
    end_data = []
    try:
        driver.get(url.format(page=url))

        try:    
            driver.wait_for_element('.text-nowrap.title-l')
        except Exception as e:
            driver.short_random_sleep()
        
        soup = soupify(driver.page_html)
        description = soup.select_one('p.text-l').text.strip()
        price = soup.select_one('formatted-price-detail div[aria-label]').text.strip()
        name = soup.select_one('h1[class*="product-name"]').text.strip()
        colors_select = soup.select('.is-flex.list-clear.content-center.flex-wrap button')
        colors = [color.attrs.get('title') for color in colors_select]
        cleaned_colors = [re.sub(r',?\s*Ref\..*', '', color) for color in colors]

        driver.click('[aria-label = "СОСТАВ / УХОД"]')

        try:    
            driver.wait_for_element('[class*="ma-product-compo-zone-list"] span')
        except Exception as e:
            driver.short_random_sleep()

        soup = soupify(driver.page_html)
            
        fabric_select = soup.select('[class*="ma-product-compo-zone-list"] span')
        fabrics = [fabric.text.strip() for fabric in fabric_select]

        rules_select = soup.select('[class*="ma-product-care"] .text-l')
        rules = [rule.text.strip() for rule in rules_select]

        jeans = {
                'name': name,
                'price': price,
                'description': description,
                'colors': cleaned_colors,
                'fabric': fabrics,
                'specification': rules,
                'url': url

            }
        end_data.append(jeans)
        print(f'page {url} was parsed')
    except Exception as e:
        print(e)
        print('problem url:', url)

    return end_data

@browser(create_error_logs=None,
         output=None,
         output_formats=None,
         headless=False)
def scrape_ids(driver: Driver, data):
    id_url = 'https://www.massimodutti.com/itxrest/3/catalog/store/35009503/30359534/category/1835017/product?languageId=-20&appId=1&showProducts=false&ts=1747327759141'
    driver.get(id_url)

    text_for_id = json.loads(driver.page_text)
    ids = text_for_id['filters']["sizeGroupFilter"][1]['productIds']
    print(f'total pages: {len(ids)}')
    
    return [f'https://www.massimodutti.com/kz/straight-midrise-jeans-l05050750?pelement={id}' for id in ids]

if __name__ == "__main__":
    urls = scrape_ids()
    results= parse_product(urls)
    with open('massimodutyparallel.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print('✔️ Parsing complete')
