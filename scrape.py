import requests
from bs4 import BeautifulSoup
import csv

UNITS_PER_PAGE = 30

cookies = {}
headers = {}

response = requests.get('https://www.lianjia.com/city/')
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.select('.city_list a')
cities = {link.text: link['href'] for link in links}
print(cities)

units = []
for city_name, city_url in cities.items():
    print(f'Scraping city {city_name}.')
    page = 0
    while True:
        page += 1
        response = requests.get(f'{city_url}ershoufang/pg{page}rs{city_name}/', cookies=cookies, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        lis = soup.select('ul.sellListContent > li')
        print(f'On {city_name} page {page}, found {len(lis)} units (total {len(units)}).')
        if len(lis) != UNITS_PER_PAGE:
            break
        for li in lis:
            unit = {
                'city': city_name,
            }
            infos = li.select('div.info.clear > div')
            for field in infos:
                unit[field['class'][0]] = field.text.strip()
            units.append(unit)

with open('output.csv', 'w') as f:
    keys = ['city', 'title', 'flood', 'address', 'followInfo', 'tag', 'priceInfo']
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    for unit in units:
        writer.writerow(unit)
