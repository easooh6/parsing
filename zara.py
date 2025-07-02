from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify

def has_reached_end(driver: Driver):
    return len(driver.select_all('.product-link.product-grid-product__link.link'))

@browser(output=None,
         output_formats=None,
         create_error_logs=None,
         headless=True,
         parallel=40,
         max_retry=5)
def scratch(driver: Driver, data: dict):
    url = data["url"]
    driver.get(url)
    driver.short_random_sleep()
    
    current = -1
    while True:
        driver.scroll_to_bottom()
        driver.short_random_sleep()
        select = has_reached_end(driver)
        if select == current:
            print(select)
            break
        current = select

    soup = soupify(driver.page_html)
    links = soup.select('.product-link.product-grid-product__link.link')
    urls = [url.attrs.get('href') for url in links]
    return urls
    
data_links = [
    {"url": "https://www.zara.com/kz/ru/zhenschiny-topy-bez-rukavov-l1791.html?v1=2419920"},
    {"url": "https://www.zara.com/kz/ru/zhenshchiny-dzhinsy-sredniaya-posadka-l1463.html?v1=2419238"},
]

results = scratch(data_links)

all_urls = [url for sublist in results for url in sublist]
print(all_urls)

# @browser(output=None,
#          output_formats=None,
#          create_error_logs=None,
#          headless=True,
#          parallel=40)
# # def scratch_urls(driver: Driver, data: dict):
# #     for url in all_urls:

# example_url = 'https://www.zara.com/kz/ru/%D0%B4%D0%B6%D0%B8%D0%BD%D1%81%D1%8B%C2%A0%E2%80%94-zw-collection-p06840284.html'
# @browser(output=None,
#           output_formats=None,
#           create_error_logs=None,
#           headless=False)
# def example(driver:Driver, data):
#     # driver.get(example_url)
#     # driver.short_random_sleep()
#     # driver.click('[data-qa-action="store-stock"]')
#     # driver.short_random_sleep()
#     # driver.select_iframe('join-ad-interest-group')
#     # driver.click('.form__column:nth-of-type(2)')
#     # input()
#     driver.get(example_url)
#     driver.short_random_sleep()
#     cur = driver.select('[data-compress="true"]:nth-child(3)')
#     print(cur)


# cookie = {'Cookie': 'MicrosoftApplicationsTelemetryDeviceId=97accb1b-29f9-4259-a789-513cbee20127; MicrosoftApplicationsTelemetryFirstLaunchTime=2025-05-13T15:15:31.590Z; MicrosoftApplicationsTelemetryDeviceId=97accb1b-29f9-4259-a789-513cbee20127; MicrosoftApplicationsTelemetryFirstLaunchTime=2025-05-13T15:15:31.590Z; access_token=eyJ4NXQjUzI1NiI6ImV6eW96cXZrQjJqem1NMmZSNElBZklJWm5sYjZYN2VidUdwYmxhb2ZXeWciLCJraWQiOiIxNDExNTcwOTA5OTE2MDAyMzA0MiIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIyMDAzMTk4NzM4NzIxIiwiYXVkaXRUcmFja2luZ0lkIjoiYmUyZjRiZDMtMzA5Ni00NDgwLTljYWUtZDM2MzdiMmRmZDI1IiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50LnphcmEuY29tIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwic2Vzc2lvbklkIjoiNDgzOTY1MDY2MTQzMTg2NzM5MyIsInN0b3JlSWQiOiIxMTc0OSIsInVzZXJJZCI6IjIwMDMxOTg3Mzg3MjEiLCJ1bmlxdWVVc2VySWQiOiIyMDAzMTk4NzM4NzIxIiwiYXVkIjoibWljLW1lY2FjY291bnRjb3JlLW9hdXRoMiIsImFjY291bnRJZCI6ImNmMDNmZDUwLWYzOGMtNGYxMC04ZjJhLWIyNjc5ZmJiNWIzZCIsIm5iZiI6MTc0NzE0OTUwOSwiaWRlbnRpdHlUeXBlIjoiRyIsImF1dGhfdGltZSI6MTc0NzE0OTUwOSwicmVhbG0iOiIvemEvZ3Vlc3QvIiwidXNlclR5cGUiOiJjdXN0b21lciIsImV4cCI6MTc0NzIzNTkwOSwidG9rZW5UeXBlIjoiSldUVG9rZW4iLCJhdXRoTWV0aG9kIjoiTGVnYWN5LlphcmEuU2Vzc2lvblRva2VuIiwiaWF0IjoxNzQ3MTQ5NTA5LCJhdXRoTGV2ZWwiOiIxIiwiYnJhbmQiOiJ6YSIsImp0aSI6IjkzNGEyNTQ3LWQyYzItNGJjZS04YzJkLWM4ZmM1NWZkMDNlZCJ9.TNKNXlw7H0HGMwZTgqhDXdO-LYAcv6gxfrZGOzqHy47k-PBfVv6XzOyvTCsLg8bn_nNLhfOVadLKTklFKoGWbzWjFQwRURcWNmxplNjLjYagyWSEpxUKQJAS5J-ifvtkVb9m8L_90IAeeOHx2blWAFe8CDnYkSQO2uo0rHdxNkNJh9x2nc4M4YjKVXGyej_MTBGE4vV6_I-Hc_aHlpk0BW5Yk0lyfj8lt486K6HHwWC2WFST5t-LJNV2eSmZJsHGlt-ijPxRM_0W62rw2VuqyncU4pl3iZzmLV6T_0TqrCWiLbPIRzBSdgDrVTgukAixXY5EC4gRFVIf3IUhFs9LwjLnfjLVliSc2l7Uxr-eueIg5xaEKR9Rz77wo58hIrlh90gqvhSPw9vlzeVH6q4WCujbs9X3U9FahA9D1VgB9f5LE_x9kMyLaXzjuWDAMbGoNnb_gHs_vaiGmOO3WdNGVlIG1XVBpy0DF15yH_dNd-zDmjgslB9_353ZkG1Svy-PKPlG7CzQDh9Ocw274NKmFxK9q5qWsUo6rxE_cloNnKz9_iCqCrLuNxmAGOnODfo__l-_DGFvkhzYeknmmnwpAq7XpKGV7MFeYgFsUraQk2l5iHbX5QlKJfLKHcyzO6soLDHj9lNwttDdD4CH81-5cDpjhrcIwhDRhY4HN3z_PrA; access_token_expires=j%3A%222025-05-14T15%3A18%3A26.272Z%22; user_type=guest; user_id=2003198738721; sids=s%3AH6Ly5S81Oo0U7-wIMcKlGBwmfjJYZr7l.6lphrH58GlQfrfnpeYD%2BlvGRJF1IhOoFZjEkzfHPH3g; TS0183864b=01d57b118cde621b8cda9300ab5e4e48463ad6f37a449f4a84d5fe17f8a9c4b6401d3dc1aa5957e48385f2227e6ca3320904fa3c28; ITXDEVICEID=ee868fe6ad4add6fa21ad57401310721; rid=395dfc3e-59e7-4007-bab8-635b711c0197; UAITXID=e91e93a504f5e110efd768345380dbbbd996458588ee8409503436ebe7dc2bcd; cart-was-updated-in-standard=true; rskxRunCookie=0; rCookie=grz4ifkhcfmjs59wsh407amamnlo7g; _gcl_au=1.1.679115576.1747149339; _ga=GA1.1.436080499.1747149339; optimizelyEndUserId=oeu1747149339359r0.4255017334941522; 826b75e46a856af63aa6a715b40616e7=99e86687658a97fa205e5aba535c502c; isShippingByDeliveryEnabled=true; _UserReference=925faa3ff1a057b4b3ed01fdb1ce2a40; optimizelySession=0; OptanonConsent=isGpcEnabled=0&datestamp=Tue+May+13+2025+23%3A00%3A45+GMT%2B0500+(GMT%2B05%3A00)&version=202503.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=c235f8e8-dcac-4f66-badf-99719e750b84&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&intType=3&geolocation=KZ%3B75&AwaitingReconsent=false; OptanonAlertBoxClosed=2025-05-13T18:00:45.484Z; lastRskxRun=1747159246798; _ga_NOTFORGA4TRACKING=GS2.1.s1747162194$o3$g0$t1747162194$j0$l0$h432242668; IDROSTA=f1bfeb0ef719:13c27de3c834ee5451bcd2ef9; ITXSESSIONID=2c807be3fd0d31a042ba57586bca836f; _abck=117C6330102233552343C090F83D3C4D~0~YAAQTM8ti6xCFcWWAQAAaNxGyw25mTMde+xRbO29rZwWuRnevpj5vhXCYtmdWxabaNYdXKIBA4VHD+gO5tKmuqs4+ws6RR03M2k6e6GdPLUnobvrXSt+4VT0cIX1I9wROP5LMxLKbSHumKHE4ktk4v5ufjfha2Hlo1ttiM12x3vAHnNlnxMVnqULIv7zFSZr1myZ0LIU9LWo1d1vds7Wfmjcxn/SSm2wE/HLhKQ4yf9D+ld5xONUyIvT2ff5CDdRh8Ypype0CDd29nxz98gf7PKw4QjsJ/WuWUPQgcYYI2IwELW/+yeFjzj+Ruz0d4/WnLnGV+/gsFK5cxHFKJIgeZ8vdF1zzR1tTmybPrIHSTqwkg9eOMSYw1//46QqHIRN+zAs7hKX1DkxUHsnNJgleCtCv1QR/EjuZmJBleoGkVO07KNSVOxw8sF5eB/7ogONJ+ymbIC0na56Jd9oBE88tW92T9WxSxf1oZfUnVm8tgHqA5NR57mE6jUFwHeShOws2qOG9ZMFmDnXqDKfS2vUQQ/kqVLZRyMQMzN2XZARbBjWaDGVYBCK/S2XOTwJEQREpzt0tEI0pRKCkw5fCIaqaPWQ55LUbo00Wj5zOprN6la8/F+6q/xzFl1S4KQjl5QRe2xrMWCnnMN0c32WPlkIdKHMlVnZ1fxjJfzZpfOfo/EsDEXYc14p4Sov9nYDqxxTXMfT3zdsZvp00pBnQl9VEzOBtHc05nQLLMxez7LiUh/riRgEYIjYLdAbdhV6IJeKsLiWucxK7HPAob+9cAbqF5oJFM0lo1ch8jEmLykWYrTd6hnQ1RwatLRX3/R02ND2ySwl0P+HriA1LBNLAKAua65tXdqMS66HNXIDyyBA00I/QsAWl+wcCcT8lFnoECX3tPJL1vDFF9r0NyVswtVY02atNsfibXlnGGYpaPnVBe2MaqHGNfFGgyBipJE68kYZqK+6wrGE0wxCiePz4dnPMt9JnytMNj5amsKmOK60vSQs3C52rCMeQ0q2A/A=~-1~-1~1747170668; bm_sz=B280E1CF5BC2991E142628D0747EED1C~YAAQTM8ti65CFcWWAQAAaNxGyxvJ+SPzCZKIMYyyqOBPXmisznIWfg2NgRRxcefASm/X/t4L6BXfmb2d8S3ClpzN7TlqYpkouYJ4VionbmhVF3cEOu0be+bNM5UV6iPkFAIvLc/0RT6E3xT/edryMpGuJJXeVOohPa6F2RYQ1oWiNpIovSrNdYrn2Ee330931bhHBXaug68WJcohWFs1f4LMECAE+SKgs3Gnz/ZVGv9LVEkXA+8ch3w+/PlwKGKyHWHS7q2h73CKGt0IBooXYC9U7TmgXx41OH6ZnrpmjcNLv1tRDNQrwD6M+pVKcbw5H4zGYSHV2tuunfq18t3SWS/IWepIzWDUJ+V5+BFkDfqRJc7LeFisi17psLgfwx2dDSfhkuG+lZomsLi2u6PR~3487554~3486009; ak_bmsc=7ADEB5D2835BA5646FD447CADF3C5D5C~000000000000000000000000000000~YAAQTM8tizNJFcWWAQAAprxHyxtVQz/12zUf1vfkTT9lSW125Sn5T7Ubmw2PhSAnupe3GKvhKPaqdGcwaFi2n8RQN11tALPiP9DdSXK3/PW3PQZBHjZP2WZkf2e4+Z5qWQOPHbwLPw2f3XnbQw4H0Cfw1Cx3DRr4XWJgpZqiqVa5YEp8CIfTQuA/SsKWYA2VIJi48trVXEdUBAQ639EunaF3bxfDC7vQkW+qoksUU29XwpBJUHW4f8YdxCxhd1sN/V2MKoBmIJCRq/Pm1v2nkuKZca4+Gsm/ESqXxaOMEK0KQw1ilC6MRUHihnD79JYxBJZHPzk5pDgzk+9Iz0jK3k4Fe+XLWP/hax303qqj2hLIvoFry7LW30EcclUvcWWucsZQj6kVeOElp8wR4WVv7yGzJZNYktqmix33153U5gkBdKgYSIBDIg2KiF5ilGo=; _ga_HCEXQGE0MW=GS2.1.s1747167019$o4$g1$t1747167263$j53$l0$h0; TS0122c9b6=01d57b118cde621b8cda9300ab5e4e48463ad6f37a449f4a84d5fe17f8a9c4b6401d3dc1aa5957e48385f2227e6ca3320904fa3c28; bm_sv=5C6B611207C576876A5EEE9B603FD843~YAAQTM8ti7dQFcWWAQAAENVIyxt/kIwTRB8OYhEW5V9eMz6FtUepz/5QnzahqhpfdTtV+RmvQI31eaw60IM1dnsmVS9btd/KFhN7mXTFTEkg2e+3LTv9bxklo/9hwz6BUBUkPbezpiT0rDBhJQPR/TWTOQPKRVUxTY7CIHM7Wi1auPU6cCEatnD+kLQHdGLbLI5zTxGeiLu1WiW+gh6JvfuTykJcY7NsRzEof7VTKtD0/S1keF7Oj2E4S/R8zbk=~1'}
# example()