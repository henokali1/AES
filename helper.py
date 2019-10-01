import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AliExpressScraper.settings')

import django
django.setup()
from django.core.wsgi import get_wsgi_application
from pages.models import *

import requests
import json
import time
import ast
import traceback
import sys

application = get_wsgi_application()


def getShippingCountryList(d):
	sfi = d.index('Ships From')
	s=d[sfi:].index('[')
	e=d[sfi:].index(']')+1
	scls = d[sfi:][s:e]
	res = []
	di=ast.literal_eval(scls)
	for i in di:
		res.append(i['propertyValueDisplayName'])
	return res

def key_extractor(obj_str, s, e):
    return obj_str[obj_str.index(s)+len(s):obj_str.index(e)]


def product_page_extract(productId):
	headers = {
		'authority': 'www.aliexpress.com',
		'method': 'GET',
		'path': '/item/{}.html'.format(productId),
		'scheme': 'https',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
		'cache-control': 'max-age=0',
		'cookie': str(Cookie.objects.filter(pk=1)[0].cookie),
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'none,',
		'sec-fetch-user': '?1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
	}

	t=time.time()
	page = requests.get('https://www.aliexpress.com/item/{}.html'.format(productId))
	tt=time.time()
	ttt = round((tt - t), 1)

	print('Request compleated in {} seconds'.format(ttt))

	d = page.text

	total_orders = d[d.index('"tradeCount"')+13:d.index('"tradeCountUnit"')-1]
	print('total_orders',total_orders)
	product_rating = key_extractor(d, ',"positiveRate":"', '%","productId":')
	print('product_rating',product_rating)
	price_range = key_extractor(d, '"formatedActivityPrice":"', '","formatedPrice":')
	print('price_range',price_range)
	shipping_countries = getShippingCountryList(d)
	print('shipping_countries', shipping_countries)
	stock_available = key_extractor(d, ',"totalAvailQuantity":', '},"buyerProtectionModule":{"')
	print('stock_available', stock_available)
	store_rating = key_extractor(d, ',"positiveRate":"', '%","productId":')
	print('store_rating', store_rating)
	product_has_video = 'video' in d	
	print('product_has_video',product_has_video)


a = Product.objects.all()

for i in range(5):
	productId = a[i].productId
	print('--------------------------------------------------------------------------------------------------')
	print('productId=', productId)
	try:
		product_page_extract(productId)
	except Exception:
		err = str(traceback.format_exc())
		# print('err == None', err == 'None')
		# print(err == None)
		# print(type(err))
		# if err != 'None':
		e, created = Err.objects.get_or_create(
				productId = productId,
				file_name = 'helper.py',
				func_name = 'product_page_extract',
				err = err
			)
	print('-------------------------------------------------------------------------------------------------')

# product_page_extract('32916713289')