import os
import requests
from bs4 import BeautifulSoup
import csv

UNITS_PER_PAGE = 30


class Scraper:
    thread_pool = None

    def __init__(self):
        pass

    def scrape_city(self, city_name, city_url):
        city_units = []
        page = 0
        while True:
            page += 1
            response = requests.get(f'{city_url}ershoufang/pg{page}rs{city_name}/', cookies=cookies, headers=headers)

            soup = BeautifulSoup(response.text, 'html.parser')
            lis = soup.select('ul.sellListContent > li')
            print(f'On {city_name} page {page}, found {len(lis)} units (total {len(city_units)}).')
            if len(lis) != UNITS_PER_PAGE:
                break
            for li in lis:
                unit = {
                    'city': city_name,
                }
                infos = li.select('div.info.clear > div')
                for field in infos:
                    unit[field['class'][0]] = field.text.strip()
                city_units.append(unit)
        return city_units

    def store_units(self, units):
        with open('output.csv', 'w') as f:
            keys = ['city', 'title', 'flood', 'address', 'followInfo', 'tag', 'priceInfo']
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer = csv.DictWriter(f, fieldnames=keys)
            for unit in units:
                writer.writerow(unit)

    def run(self):
        cookies = {}
        headers = {}

        response = requests.get('https://www.lianjia.com/city/')
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.city_list a')
        cities = {link.text: link['href'] for link in links}
        print(cities)

        units = []
        if os.path.exists('output.csv'):
            with open('output.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    units.append(row)

            cities_processed = {unit['city'] for unit in units}
            for city_name in cities_processed:
                cities.pop(city_name)
            print('Already processed cities: ' + ', '.join(cities_processed))

        for city_name, city_url in cities.items():
            print(f'Scraping city {city_name}.')
            city_units = scrape_city(city_name, city_url)
            units += city_units
            store_units(units)

s = Scraper()
s.run()
