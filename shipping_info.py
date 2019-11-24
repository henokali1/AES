import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AliExpressScraper.settings')

import django
django.setup()
from django.core.wsgi import get_wsgi_application
from pages.models import *

import requests
import time
import json
import concurrent.futures
from pages.models import *


def get_shipping_info(productId):
    headers = {
        'Origin': 'https://hz.aliexpress.com',
        'Referer': 'https://hz.aliexpress.com/',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    minPrice=0
    maxPrice=0

    url = 'https://www.aliexpress.com/aeglodetailweb/api/logistics/freight?productId={}&count=1&minPrice={}&maxPrice={}&sendGoodsCountry=US&country=US&provinceCode=&cityCode=&tradeCurrency=USD&userScene=PC_DETAIL'.format(productId, minPrice, maxPrice)
    t = time.time()
    response = requests.get(url, headers=headers)
    tt = round(time.time() - t, 1)
    print('Request compleated in {} secs'.format(tt))

    data = json.loads(response.text)['body']["freightResult"][0]

    res = {
        'shippingPrice': data['freightAmount']['value'],
        'shippingCompany': data['company'],
        'commitDay': data['commitDay'],
        'estimatedDelivery': data['time'],
        'trackingAvailable': data['tracking'],
        'estimatedDeliveryDayMax': int(data['time'].split('-')[1]),
        'estimatedDeliveryDayMin':int(data['time'].split('-')[0]),
    }
    print(res)
    Product.objects.filter(productId=productId).update(
        shippingPrice = data['freightAmount']['value'],
        shippingCompany = data['company'],
        commitDay = data['commitDay'],
        estimatedDeliveryDayMax = int(data['time'].split('-')[1]),
        estimatedDeliveryDayMin = int(data['time'].split('-')[0]),
        trackingAvailable = data['tracking'],
        )
    return res

# si = get_shipping_info("33037874102")
# for i in si.keys():
#     print(i, si[i])

with concurrent.futures.ThreadPoolExecutor() as executor:
    po = Product.objects.all().values_list('productId')
    productIds = [i[0] for i in po]

    results = executor.map(get_shipping_info, productIds)
