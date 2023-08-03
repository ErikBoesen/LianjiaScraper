import requests
from bs4 import BeautifulSoup
import csv

cookies = {
    'select_city': '430100',
    'lianjia_ssid': '1afc204f-d9d1-46f2-8441-290cad9d400b',
    'lianjia_uuid': 'ab9a81ad-b4b7-4c81-8def-7784c4a16bc7',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22189b94d144f620-018f2ae06446e88-41292c3d-1296000-189b94d14514c%22%2C%22%24device_id%22%3A%22189b94d144f620-018f2ae06446e88-41292c3d-1296000-189b94d14514c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
    'sajssdk_2015_cross_new_user': '1',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://cs.lianjia.com/',
    # 'Cookie': 'select_city=430100; lianjia_ssid=1afc204f-d9d1-46f2-8441-290cad9d400b; lianjia_uuid=ab9a81ad-b4b7-4c81-8def-7784c4a16bc7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22189b94d144f620-018f2ae06446e88-41292c3d-1296000-189b94d14514c%22%2C%22%24device_id%22%3A%22189b94d144f620-018f2ae06446e88-41292c3d-1296000-189b94d14514c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; sajssdk_2015_cross_new_user=1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}
#search_term = input('Write your search here: ')
search_term = '长沙'
response = requests.get('https://cs.lianjia.com/ershoufang/rs' + search_term + '/', cookies=cookies, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
lis = soup.select('ul.sellListContent > li')
houses = []
for li in lis:
    house = {}
    infos = li.select('div.info.clear > div')
    for field in infos:
        print(field)
        house[field['class'][0]] = field.text.strip()
    houses.append(house)
print(houses)

with open('test.csv', 'w') as testfile:

    # store the desired header row as a list
    # and store it in a variable
    fieldnames = ['first_field', 'second_field', 'third_field']

    # pass the created csv file and the header
    # rows to the Dictwriter function
    writer = csv.DictWriter(testfile, fieldnames=fieldnames)

    # Now call the writeheader function,
    # this will write the specified rows as
    # headers of the csv file
    writer.writeheader()
