import requests
from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
import json

@browser(headless=False,
         output=None,
         output_formats=None,
         create_error_logs=None)
def imdb_parser(driver: Driver, data):
    driver.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
    driver.short_random_sleep()
    soup = soupify(driver.page_html)
    select = soup.select('.ipc-title.ipc-title--base.ipc-title--title.ipc-title-link-no-icon.ipc-title--on-textPrimary.sc-143a3ae8-2.ezwMlU.cli-title.with-margin a')
    urls = ['https://www.imdb.com/' + i.attrs.get('href') for i in select]
    
    data = []
    i=0
    for url in urls:
        if i > 3:
            break
        i+=1
        try:
            driver.get(url)
            driver.scroll_to_bottom()
            driver.short_random_sleep()

            soup = soupify(driver.page_html)

            year_select = soup.select('.ipc-inline-list.ipc-inline-list--show-dividers.sc-103e4e3c-2.cMcwpt.baseAlt.baseAlt li a')
            
            rate = soup.select_one('.sc-d541859f-2.kxphVf')

            duration = soup.select_one('.ipc-inline-list.ipc-inline-list--show-dividers.sc-103e4e3c-2.cMcwpt.baseAlt.baseAlt :nth-of-type(3)')

            director = soup.select_one('.sc-bf57f3f2-2.dvWMNJ .ipc-metadata-list-item__content-container ul li .ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link')
            name = soup.select_one('.hero__primary-text')

            genres = soup.select('.ipc-chip.ipc-chip--on-baseAlt')
            metascore = soup.select_one('.ipc-inline-list__item.sc-e687d503-1.lbJJKq .three-Elements .score .sc-ae9e80c5-0.gXcoKx.metacritic-score-box')
        except Exception as e:
            print(e)
            continue

        film = {
            'name': name.text.strip(),
            'duration': duration.text.strip(),
            'rate': rate.text.strip(),
            'year': year_select[0].text.strip(),
            'censore': year_select[1].text.strip(),
            'director': director.text.strip(),
            'genres': [i.text.strip() for i in genres],
            'metascore': metascore.text.strip()
        }
        data.append(film)

        print('parsed url:', url)
    
    with open('imdb.json','w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False, indent = 4)


imdb_parser()