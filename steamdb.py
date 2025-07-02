from typing import List, Dict, Union

from datetime import datetime

import csv
import pandas as pd

from botasaurus.browser import browser, Wait, Driver
from botasaurus.soupify import soupify
from botasaurus.lang import Lang
import re
import sys



@browser(
    headless = True,
    output = None,
    output_formats = None,
    create_error_logs = False,
    close_on_crash = True,
    lang = Lang.English,
    add_arguments = [
        "--start-maximized",
        "--disable-blink-features=AutomationControlled",
        '--no-sandbox',
        '--no-first-run'
    ]
    
)
def get_data(driver: Driver, data: dict) -> Union[List, List[Dict]]:
    timestamp = datetime.now().isoformat()

    url = "https://steamdb.info/stats/mostwished/"
    
    output_data = []
    counter = 0

    driver.get(url)
    driver.sleep(5)


    while counter < 200:
        driver.sleep(3)

        soup = soupify(driver.page_html)
        apps = soup.select("tbody tr.app")

        for app in apps:
            if counter < 200:
                ranking = app.select_one("tbody tr.app > td.dt-type-numeric:nth-child(1)")
                ranking = int(ranking.text.replace(".", "").replace(",", "").strip()) if ranking else None

                name = app.select_one("tbody tr.app a.b")
                name = name.text.strip() if name else ""

                price = app.select_one("tbody tr.app td:has(a.b) + td + td")
                price = price.text.replace(",",".").strip() if price else None

                if price:
                    pattern = r"\d+\.\d+"
                    matches = re.findall(pattern, price) 
                    if matches:
                        price = float(matches[0])
                    else:
                        price = None

                rating = app.select_one("tbody tr.app td:has(a.b) + td + td + td")
                rating = rating.text.replace(",", ".").strip() if rating else None


                if rating:
                    pattern = r"\d+\.\d+"
                    matches = re.findall(pattern, rating) 
                    if matches:
                        rating = float(matches[0])
                    else:
                        rating = None
                
                release = app.select_one("tbody tr.app td:has(a.b) + td + td + td + td")
                release = release.text.strip() if release else None

                date_type = None

                if release:
                    if release in ("TBA", "Soon"):
                        date_type = "other"
                    elif any(f"Q{i}" in release for i in range(1, 5)):
                        date_type = "quater"
                    elif re.findall("^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}$", release):
                        date_type = "month"
                        release = datetime.utcfromtimestamp(int(app.select_one("tbody tr.app td:has(a.b) + td + td + td + td").attrs["data-sort"])).strftime('%#d/%#m/%Y')
                    else:
                        date_type = "year"
                
                follows = app.select_one("tbody tr.app td:has(a.b) + td + td + td + td + td")
                follows = int(follows.attrs["data-sort"]) if int(follows.attrs["data-sort"]) != 0 else None
                
                output_data.append(
                    {
                        "scrape_datetime": timestamp,
                        "ranking": ranking,
                        "name": name,
                        "price": price,
                        "rating": rating,
                        "date_type": date_type,
                        "release": release,
                        "follows": follows
                    }
                )
                counter += 1
            else:
                break
        print("Scraped {} items".format(counter))

        driver.scroll_into_view("button.dt-paging-button:last-child")
        driver.click("button.dt-paging-button:last-child")
        

    driver.close()
    return output_data


if __name__ == "__main__":
    filename = "data/sample.csv"

    data = get_data()
    
    output = pd.DataFrame(data)

    output["price"] = output["price"].astype("Float64")
    output["rating"] = output["rating"].astype("Float64")
    output["follows"] = output["follows"].astype("Int64")

    output.to_csv(
        filename,
        encoding="utf-8",
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        index=False
    )