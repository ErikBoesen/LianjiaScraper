import os
import requests
from bs4 import BeautifulSoup
import csv
from threading import Thread

UNITS_PER_PAGE = 30
OUT_FILE = 'output.csv'


class Scraper:
    # Executed when you initialize the scraper
    def __init__(self):
        # Fetch the city list page
        response = requests.get('https://www.lianjia.com/city/')
        # Turn it into BeautifulSoup object so we can read the content
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.city_list a')
        self.units = []
        # Make a list of cities to scrape with city name : URL pairs
        self.cities_queue = {link.text: link['href'] for link in links}

        # If the output spreadsheet already exists, open it and read all the units into self.units
        if os.path.exists(OUT_FILE):
            with open(OUT_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.units.append(row)

            # Get a set of all cities that are already listed in the spreadsheet,
            cities_processed = {unit['city'] for unit in self.units}
            # And iterate through each to remove them from teh queue of cities to scrape
            for city_name in cities_processed:
                self.cities_queue.pop(city_name)
            print('Skipping already processed cities: ' + ', '.join(cities_processed))

    # A function to run on a thread that repeatedly scrapes a city until there are none left
    def scrape_thread(self):
        while self.cities_queue:
            # Remove a city from the queue to scrape
            city_name, city_url = self.cities_queue.popitem()
            print(f'Scraping city {city_name}.')
            # Run the scraping
            city_units = self.scrape_city(city_name, city_url)
            self.units += city_units
            # Save all the units, including the new ones we just scraped, into the spreadsheet
            self.store_units(self.units)

    def scrape_city(self, city_name, city_url):
        city_units = []
        page = 0
        while True:
            page += 1
            # Download the page and prepare it to scrape content
            response = requests.get(f'{city_url}ershoufang/pg{page}rs{city_name}/')
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get all the items that match this CSS selector, i.e. get a list of all the housing unit results listed on the page
            lis = soup.select('ul.sellListContent > li')
            print(f'On {city_name} page {page}, found {len(lis)} units (total {len(city_units)}).')

            # If we don't see 30 units listed (i.e. this is the last page or past the end of the list) then we stop going to the next page
            if len(lis) != UNITS_PER_PAGE:
                break

            # Loop through each item iin the list
            for li in lis:
                unit = {
                    'city': city_name,
                }
                # Get all the div elements with pieces of information we want
                infos = li.select('div.info.clear > div')
                # Iterate through each one, extracting the text content and storing it into the "unit" dictionary
                for field in infos:
                    unit[field['class'][0]] = field.text.strip()
                # Add unit to the units list
                city_units.append(unit)
        return city_units

    def store_units(self, units):
        # Store all the units in the spreadsheet
        with open(OUT_FILE, 'w') as f:
            keys = ['city', 'title', 'flood', 'address', 'followInfo', 'tag', 'priceInfo']
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for unit in units:
                writer.writerow(unit)

    def run(self):
        thread_pool = []
        # Create 5 different simultaneous threads that all scrape cities
        for i in range(0, 5):
            # Create the thread
            thread = Thread(target=self.scrape_thread)
            # Start the thread running
            thread.start()
            # Store the thread into the thread_pool list so we can come back and check on it
            thread_pool.append(thread)
        # Wait for every thread to finish
        for thread in thread_pool:
            thread.join()

s = Scraper()
s.run()
