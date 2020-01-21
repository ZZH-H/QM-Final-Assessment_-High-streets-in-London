from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
import time
import pymongo
from scrapy.selector import Selector

mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/tmp')
mongo_db = mongo_client['tmp']
mongo_england_map_collection = mongo_db['england_map']

driver = webdriver.Chrome("C:\software\chromedriver_win32\chromedriver")
driver.get('https://www.ordnancesurvey.co.uk/demos/high-streets/high-streets/index.html#11.3/51.5332/-0.1582')
print('rest 10 seconds')
time.sleep(10)
print('begin capture')
while True:
    time.sleep(1)
    page_source = driver.page_source
    selector = Selector(text=page_source)
    properties = selector.xpath('//div[@class="osel-feature-properties"]/div[@class="property"]')
    item = {}
    for property in properties:
        key = property.xpath('div[1]/text()').extract_first()
        value = property.xpath('div[2]/text()').extract_first()
        item[key] = value
    id = item.get('id')
    if id:
        query = {'id': item.get('id')}
        exists_item = mongo_england_map_collection.find_one(query)
        if not exists_item:
            print('insert new data:%s' % id)
            mongo_england_map_collection.insert_one(item)
        else:
            print('existed data:%s' % id)
