import os
import requests
from bs4 import BeautifulSoup
import csv
from threading import Thread

UNITS_PER_PAGE = 30
OUT_FILE = 'output.csv'


class Scraper:
    def __init__(self):
        response = requests.get('https://www.lianjia.com/city/')
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.city_list a')
        self.units = []
        self.cities_queue = {link.text: link['href'] for link in links}

        if os.path.exists(OUT_FILE):
            with open(OUT_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.units.append(row)

            cities_processed = {unit['city'] for unit in self.units}
            for city_name in cities_processed:
                self.cities_queue.pop(city_name)
            print('Already processed cities: ' + ', '.join(cities_processed))

    def scrape_thread(self):
        while self.cities_queue:
            city_name, city_url = self.cities_queue.popitem()
            print(f'Scraping city {city_name}.')
            city_units = self.scrape_city(city_name, city_url)
            self.units += city_units
            self.store_units(self.units)

    def scrape_city(self, city_name, city_url):
        city_units = []
        page = 0
        while True:
            page += 1
            response = requests.get(f'{city_url}ershoufang/pg{page}rs{city_name}/')

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
            for unit in units:
                writer.writerow(unit)

    def run(self):
        thread_pool = []
        for i in range(0, 5):
            thread = Thread(target=self.scrape_thread)
            thread.start()
            thread_pool.append(thread)
        for thread in thread_pool:
            thread.join()

s = Scraper()
s.run()
