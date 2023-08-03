import requests
from bs4 import BeautifulSoup
import csv

cookies = {}
headers = {}

search_terms = ['长沙', '北京', '上海', '杭州', '武汉', '福州', '广州', '深圳']
units = []
for search_term in search_terms:
    for page in range(1, 1 + 1):
        print(f'On page {page}, now have found {len(units)} units.')
        response = requests.get(f'https://cs.lianjia.com/ershoufang/pg{page}rs{search_term}/', cookies=cookies, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        lis = soup.select('ul.sellListContent > li')
        for li in lis:
            unit = {}
            infos = li.select('div.info.clear > div')
            for field in infos:
                unit[field['class'][0]] = field.text.strip()
            units.append(unit)

with open('output.csv', 'w') as f:
    keys = ['title', 'flood', 'address', 'followInfo', 'tag', 'priceInfo']
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    for unit in units:
        writer.writerow(unit)
