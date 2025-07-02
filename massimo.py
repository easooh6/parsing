import cloudscraper
import requests
import browser_cookie3
from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
import json
import re

# scraper = cloudscraper.create_scraper()

# headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}
# cookies = {'cookies': 'ITXSESSIONID=dc7de3e03ba6adbc1e1e83fe00fa4750; MDSESSION=27d9826b0ca1291e82673898ea12b259; bm_mi=C644D7C5E4FCD31E3EA3E5FD9B28AE83~YAAQVs8ti9mqBM6WAQAAQNjW1BvwjNJg3Cg2+8EBh+uCi3uURKNtP4wkGY31gu+YOoH751w4tD+2gCr6xjgExbhgDhDZa2Qn0rFuLAUvWR78iubkt0dYWdAap5Qv2ftC2R+IeS7GZxsTsqzXcUq755RyfeKEptnv65JYbGeyDcPHfQoy8ymEF1Weh7bJm/79IF8f2KQOeVDnawrdwhbUhdFBt188J0CBMbhCBWpGfq5qj3svN/8eOWuy4CQNa1YJmwzEX1FnIOf4w2ORR3OrVo1Y7cVo7Pj6y/gNINei4mjEFmLzN+krreECJ4Hp84KgJ9Ox~1; _itxo11y_ses.4e20=*; ak_bmsc=0E7B4FBA6BA6A7E556E9E40E18ACFE03~000000000000000000000000000000~YAAQVs8ti+aqBM6WAQAAJt7W1BuhKoeo46IN3h1L1ALkGQmH7i6xmexOlPS9dswups8L4mK4oI+ADSmVsCu7dgxEIdjQghcFGNKUFw4EZIyLcAkAS3U28lsiu2TdvEuY+iweiTYCvnYTt/551T3RwLVX/6HI9NVVJgoJGFBph40APa4brxW3/7HFojEOuuhsj5ZcSd2M6nlCEZTWYPvTzCWots+ZXYhTuv8tc3rvGTcz+8OclJzohEWKJgZY4Si+Pz+pCbfULoZLVuxOfK+7LNds+5deh0GLtlRy/K/LyxDATmdcmPFfRYTgslIJzenT4/Bf3XcDrUHDfRMNEUSkqt7mBfP/R63odU7aiyjd34dW0Lwk4BV9jAwyJHdznq0ylvRnd714AzpX8nQrBQKS+GsgTGiHsKlXFKDBkOnuD9H8/HkaDZWQgEWhzlDjP6g9VkU/eSuee+ifBnfr0KwO5FK+g/Bwefw37kH7qshw7ue4kNWxIXIPrakdFJNx2odwtg5nUfg4kZAC1iXh6N/EymUQAtvGDB5jxKVxQcUjPgdXgV+IJ8HM3rNh4nWpZCihM4CyJHPN; IDROSTA=80a6387c2a81:1dab710fc8892d7255bcc6cda; UAITXID=6073c47d6c4421632b153cebd0daee5722d667519d52231c5350baf9b46c2506; JSESSIONID=0000AapgCZM1ZeBUA-eFUUnr_7l:1aa1aj2e2; _gcl_au=1.1.1928507911.1747327577; _ga=GA1.1.1706449877.1747327577; _pin_unauth=dWlkPU56UTVNR0V5TmpFdFpUZG1aaTAwWVRObExXSmhORE10TnpNM1pEZGlNREpoTXpjMg; _hjSession_5269530=eyJpZCI6IjU1ZDEwMzg5LTI3MmUtNDNjZC04MThkLTc0MTVjMDI0YWQ2NSIsImMiOjE3NDczMjc1Nzc3MzUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _tt_enable_cookie=1; _ttp=01JVADDVP3W0APZHPCCCD36J6T_.tt.1; ORA_FPC=id=1c53c7f1-9556-41ba-8b0a-a58f7d8b3403; LAST_STORE_JSON=%7B%22id%22%3A35009503%2C%22countryCode%22%3A%22kz%22%2C%22countryName%22%3A%22Kazakhstan%22%2C%22storeDefaultLanguageId%22%3A-20%2C%22supportedLanguages%22%3A%5B%7B%22id%22%3A-20%2C%22code%22%3A%22ru%22%2C%22name%22%3A%22%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9%22%7D%5D%7D; _abck=74D66BCA6D8E8E37741B272880821B21~0~YAAQVs8tiyqrBM6WAQAARQjX1A0wBWamRzfXtDOEcRiaeydqzSz4ZVwgZ8dhRN/hdWwblapo9fHoArbn5QXSOycsLWF2JDPNL1c21OVG3DnZ4x4CugIJv7I1unzaIUX1+B2lwod6AyIAuZ0FYivbBSBHPEoOaDspzIPI2k6QkyvCpcqJYV57al68tAg2vm8BzSsSuOanjsLevpgW3xtdaCF2ujlEJw5BcGc53PcxlnvVrR6DfyDEr5y16TkcHcERRjD9tGAzc6izCFAsyYxgbG25n1xvFWeekxQH0pCupTO6Yd5zaEeKUxmN82WHpyymQKvbYMwaOyZ9vbQ2LR0Z9pbalVv7gsfujnOAXTxVa7Msepy1tvoBbAnQl2pG6J4RDhn7QptjTJrfDOPK1v8JFQ+tleiDSZfT7sEpEEtx5PSX/NPGSn7jYyYEv82LIPBPN7nCCZo0ZG+sFWohIacG4Hbk6ETapwwhn84qrXcFz9TXbxstGuME73HMogDpIhqNM59N5Syw5VaDIbj4IQRyum4B5K+jlgfmYSY01AN9ng7E187gUvr2Fx0z1TlMwnwiVovAiwuZ/BJ7wwN97p0AiLG69BLaCuyaJZL5LmCFHy6ubJZtTyuoI1xpJ5w=~-1~-1~1747331172; _hjSession_1259099=eyJpZCI6ImFlNjFlOTdlLWYzNDYtNGEyYy1iMmU4LTk2ZGVjNjJjNjJiNyIsImMiOjE3NDczMjc1ODc2MzcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; optimizelyEndUserId=oeu1747327587782r0.694139973997973; _hjSessionUser_1259099=eyJpZCI6IjBjNDRjNjU5LTQ4MzEtNTc0YS1iOWY2LWY2N2ZlZGViMTNjMCIsImNyZWF0ZWQiOjE3NDczMjc1ODc2MzUsImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionUser_5269530=eyJpZCI6ImI0ZWZkNDcyLWJiMjYtNWQxZi1hY2RkLWI4YTliNGJmZjNmZCIsImNyZWF0ZWQiOjE3NDczMjc1Nzc3MzMsImV4aXN0aW5nIjp0cnVlfQ==; WTPERSIST=; optimizelySession=1747327666377; OptanonConsent=isGpcEnabled=0&datestamp=Thu+May+15+2025+21%3A58%3A15+GMT%2B0500+(GMT%2B05%3A00)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=1275f2eb-697d-49b2-bfb3-67f10421f0d4&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0005%3A1&geolocation=KZ%3B75&AwaitingReconsent=false; OptanonAlertBoxClosed=2025-05-15T16:58:15.761Z; _itxo11y_id.4e20=84c96bc7-55b6-4802-91e9-31ba3e09b203.1747327573.1.1747328297..9e08cca4-1bca-49e1-9646-9bc393a4c371....0; _ga_NOTFORGA4TRACKING=GS2.1.s1747327577$o1$g1$t1747328297$j0$l0$h1387788127; ttcsid=1747327577801::K7CGa4NPnCqjJrF_eibs.1.1747328298751; ttcsid_CAOP60BC77U56BB6AMUG=1747327577800::6fegHr0xk_4Kn9ZWDvpA.1.1747328299057; _ga_F6ZL9NT6KE=GS2.1.s1747327577$o1$g1$t1747328933$j60$l0$h0; TS01d6af0d=01b752f41e2362e11c19aecfe13729aa15d55876c93e29a6bcc72ca125c38965bcc2e3719883bf79f89a512573fd3bc234bb98ed6c; bm_sv=9FADD0F3A1ADF7ABDD652190E11AC04B~YAAQVIVlX2PTDaiWAQAAwBPu1BvMR9J+spTuajE9Uk1b24j+7Jbclg216476FgSsjX7N9IlpcWXHLXx5fxpCL33Xi5h9Xlf9s5LJ/fYUaf8UqSIHh180UneFfltbz97x80hl0Epby9GjjIP+Padhzv5IZdUT6K7ZtygVoAj44Yb1vuTAjyjt8HLZOJKW/CN7m2zPrz6qBTQaSMT4iKZYwJX0gMFaz1auIfDiDPVihqabw+NIZ5itUCZzrbMSBbs6r4CiIRXZb6I=~1; bm_sz=1DC6804B9D34DB179F60C53DF58C2582~YAAQVIVlX2TTDaiWAQAAwBPu1BvaVDeCmidyJqxJ3oCYRTRMhkX60KsjGqOeFs4p7ZyNUpXS0IczNjjd7BB9tlmvw0VhIOOOcs/ffxxrpsbwlgeGQZi3JPzqXjo0CZzcqOTaLst2hf0MXTWumgHu7b8mdMifxC9vczzLs5hcp0xUldP1XNFRbezeyralNMMlnb5mx0UWvBmfSbiBIuFj8XdV6b8DmRZ+Du9tK5EnasjqX2hG/ZRKSaQ1/yLX0mUxzgXg8a581aleczvoN50WseJ4YlxcYIS2VBqs7uSDb8mJ8Vn61Zsrk8B8XC0n2IZ2HKRKzsvRupEdjne7kOEV6CUU719ZEEosKoAAGUBCR8BEMipxfqHTW555a+2N+DCjFrRdc8VVZf+AoAbEpGwESHkCjLbqW2BKOk10ud8/UkGjCfyRaN/7DatNSzv7OaXm8aD2VA7xM7ngxaUjgnELLRXMXkoqyPzW0HCTCo/2inZIO9dxAhqQbvJZwMgg5W+wIVsC6bIcm8QWbGFao1l9DXL/hewcF3bM5xFqlZ3DJt3pjQ==~4272196~3160375'}

# response = requests.get(url=url,cookies=cookies, headers=headers)
# print(response.text)
# # ex = [52574809, 48645421, 50816101, 50816100, 49490009, 50367648, 47652602, 47652603, 48704266, 47650374, 47650373, 49490012, 48704267, 46395474, 46079554, 46079553, 45479677, 46916905, 46470408, 46394807, 45479676, 46763671, 45782944, 45782946, 45782945, 46394808, 45782951, 45941283, 45782937, 45484085, 46623501, 45484084, 45484083, 45484079, 45484193, 45004136, 46279242, 45479678, 46274764]

@browser(create_error_logs=None,
         output=None,
         output_formats=None,
         headless=False)
def scraping_json(driver: Driver, data: dict):

    end_data = []

    id_url = 'https://www.massimodutti.com/itxrest/3/catalog/store/35009503/30359534/category/1835017/product?languageId=-20&appId=1&showProducts=false&ts=1747327759141'
    driver.get(id_url)
    
    page_url = 'https://www.massimodutti.com/kz/straight-midrise-jeans-l05050750?pelement={page}'

    text_for_id = json.loads(driver.page_text)
    ids = text_for_id['filters']["sizeGroupFilter"][1]['productIds']
    print(f'total pages: {len(ids)}')
    for url in ids:
        try:
            driver.get(page_url.format(page=url))
            
            driver.wait_for_element('.text-nowrap.title-l')

            soup = soupify(driver.page_html)
            description = soup.select_one('p.text-l').text.strip()
            price = soup.select_one('formatted-price-detail div[aria-label]').text.strip()
            name = soup.select_one('h1[class*="product-name"]').text.strip()
            colors_select = soup.select('.is-flex.list-clear.content-center.flex-wrap button')
            colors = [color.attrs.get('title') for color in colors_select]
            cleaned_colors = [re.sub(r',?\s*Ref\..*', '', color) for color in colors]

            driver.click('[aria-label = "СОСТАВ / УХОД"]')
            driver.wait_for_element('[class*="ma-product-compo-zone-list"] span')
            
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
            print(jeans)
            end_data.append(jeans)
            print(f'page {url} was parsed')
        except Exception as e:
            print(e)
            print('problem url:', url)
            continue

    with open('massimoduty.json','w',encoding='utf-8') as file:
        json.dump(end_data,file,ensure_ascii=False,indent=4)
    print('massimoduty was successfully parsed')

    # text = json.loads(driver.page_text)
    # ids = text['filters']["sizeGroupFilter"][1]['productIds']
    
    # cur_id = ids[0]
    # new_url = f'https://www.massimodutti.com/kz/midrise-straightleg-jeans-l05093793?pelement={cur_id}'
    # driver.get(new_url)
    # driver.wait_for_element('script')
    
    # soup = soupify(driver.page_html)
    # script_tag = soup.select_one('#mdfrontw-state')
    
    # if script_tag and script_tag.string:
    #     # Extract the text content from the script tag
    #     json_text = script_tag.string
        
    #     try:
    #         # Parse the text content as JSON
    #         json_data = json.loads(json_text)
            
    #         # Now you can save the parsed JSON data
    #         with open('mass_try.json', 'w', encoding='utf-8') as file:
    #             json.dump(json_data, file, ensure_ascii=False, indent=4)
                
    #         print("Data successfully extracted and saved to mass_try.json")
            
    #     except json.JSONDecodeError as e:
    #         print(f"Error parsing JSON: {e}")
    #         # Save raw content for debugging
    #         with open('script_content.txt', 'w', encoding='utf-8') as file:
    #             file.write(str(json_text))
    # else:
    #     print("Script tag not found or empty")
    
scraping_json()
