from requests_html import HTMLSession
import pandas as pd
import logging
import sqlite3


# Set User-Agent header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

session = HTMLSession()
session.headers.update(headers)

# Error Handling and Logging
logging.basicConfig(filename='laptops_scraping.log', level=logging.INFO)
counter = 0
try:
    url = 'https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/laptops/?limit=200&page=1'
    r = session.get(url, timeout=10)

    r.html.arender(sleep=10, scrolldown='20')
    page_title = r.html.find('title', first=True).text
    available_laptops = r.html.find('div.sc-7d1ac0ec-4.cHooCx', first=True).text.split()[0]
    num_pages = int(r.html.find('.pageLink')[-1].text)
    print(page_title)
    print(f'Number of available laptops is: {available_laptops}\nPages: {num_pages}')

    laptops_list = []

    for i in range(1, num_pages + 1):
        print(f"Scraping page {i} of {num_pages}")
        url = f'https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/laptops/?limit=200&page={i}'
        r = session.get(url, timeout=10)
        r.html.arender(sleep=10, scrolldown='20')

        laptops = r.html.find('#__next > div > section > div > div > div > div.sc-926ab76d-5.MBA-Dr > div.sc-926ab76d-7.eCDCTP.grid > span')

        for laptop in laptops:
            try:
                laptop_link = list(laptop.absolute_links)[0]
                r_laptop = session.get(laptop_link)
                brand = r_laptop.html.find(
                    '#__next > div > section > div > div.sc-e6ac681c-4.kBJtlp.noGap > div:nth-child(2) > div > div.sc-e6ac681c-8.dlyHKy > div.sc-e6ac681c-9.gYcwMr > div > a > div > div', first=True).text
                model = r_laptop.html.find('.modelNumber', first=True).text.split(':')[-1]
                laptop_name = r_laptop.html.find(
                    '#__next > div > section > div > div.sc-e6ac681c-4.kBJtlp.noGap > div:nth-child(2) > div > div.sc-e6ac681c-8.dlyHKy > div.sc-e6ac681c-9.gYcwMr > div > h1', first=True).text.split(' - ')[0]
                laptop_price = r_laptop.html.find('.priceNow', first=True).text
                laptop_rating = r_laptop.html.find('.sc-363ddf4f-2.jdbOPo', first=True).text if r_laptop.html.find(
                    '.sc-363ddf4f-2.jdbOPo', first=True) else "N/A"
                stock = r_laptop.html.find('.sc-9b5c7a61-5.fTSPxQ', first=True).text if r_laptop.html.find(
                    '.sc-9b5c7a61-5.fTSPxQ', first=True) else "N/A"
                laptop_dict = {
                    'name': laptop_name,
                    'brand': brand,
                    'model': model,
                    'price': laptop_price,
                    'stock': stock
                }
                specifications = r_laptop.html.find(
                    '#__next > div > section > div > div:nth-child(2) > div:nth-child(1) > section > div > div > div.sc-966c8510-0.jLcJyt > div > div > table > tbody > tr')
                for tr in specifications:
                    key, value = [td.text for td in tr.find('td')]
                    laptop_dict[key] = value
                # print(laptop_dict)
                laptop_dict['link'] = laptop_link
                laptops_list.append(laptop_dict)
                counter += 1
                print(f'we have scrapped {counter}')
            except Exception as laptop_error:
                print(f"Error scraping laptop details: {str(laptop_error)}")
                logging.error(f"Error scraping laptop details: {str(laptop_error)}")

    # Save to CSV
    laptops = pd.DataFrame(laptops_list)
    laptops.to_csv('noon-phones.csv', index=False)

    # Save to SQLite Database
    conn = sqlite3.connect('noon-phones.db')
    laptops.to_sql('noon_phones', conn, index=False, if_exists='replace')
    conn.close()

except Exception as main_error:
    print(f"An error occurred: {str(main_error)}")
    logging.error(f"An error occurred: {str(main_error)}")
    