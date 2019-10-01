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

def parsePrice(p):
	p=p.replace('US $','')
	if '-' in p:
		pl = p.replace(',', '').split(' - ')
		price = {'min': float(pl[0]), 'max': float(pl[1])}
		return price
	else:
		pf = float(p.replace(',', '').strip())
		price = {'min': pf, 'max': pf}
		return price

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
	
	page = requests.get('https://www.aliexpress.com/item/{}.html'.format(productId))
	d = page.text

	total_orders = d[d.index('"tradeCount"')+13:d.index('"tradeCountUnit"')-1]
	product_rating = key_extractor(d, ',"positiveRate":"', '%","productId":')
	price_range = key_extractor(d, '"formatedActivityPrice":"', '","formatedPrice":')
	np = parsePrice(price_range)
	shipping_countries = getShippingCountryList(d)
	stock_available = key_extractor(d, ',"totalAvailQuantity":', '},"buyerProtectionModule":{"')
	store_rating = key_extractor(d, ',"positiveRate":"', '%","productId":')
	product_has_video = 'video' in d	
	c = Cookie.objects.all()[0].cookie
	try:
		headers = {
			'authority': 'home.aliexpress.com',
			'method': 'GET',
			'path': '/dropshipper/product_analysis_ajax.htm?productId=' + productId,
			'scheme': 'https',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
			'accept-encoding': 'gzip, deflate, br,',
			'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
			'cache-control': 'max-age=0',
			'cookie': str(Cookie.objects.filter(pk=1)[0].cookie),
			'sec-fetch-mode': 'navigate',
			'sec-fetch-site': 'none',
			'sec-fetch-user': '?1',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
		}

		url = 'https://home.aliexpress.com/dropshipper/product_analysis_ajax.htm?productId=' + productId

		response = requests.get(url, headers=headers)
		data = json.loads(response.text)['data']

	except Exception:
		err = str(traceback.format_exc())
		e, created = Err.objects.get_or_create(
				productId = productId,
				file_name = 'helper.py',
				func_name = 'product_page_extract',
				err = err
			)


	new_product, created = Product.objects.get_or_create(
			productId = productId,
			rating = float(product_rating),
			productTitle = data["subject"],
			minPrice = parsePrice(price_range)['min'],
			maxPrice = parsePrice(price_range)['max'],
			storeName = data["storeName"],
			totSalesCount = int(total_orders),
			shippingCountries = str(shipping_countries),
			stockAvailable = int(stock_available),
			storeRating = float(store_rating),
			productListingHasVideo = product_has_video,
			imageUrl = data["imageUrl"],
			logisticsReliability = data['logisticsReliability'],
			sellerDsSupplier = data['sellerDsSupplier'],
			storeUrl = data['storeUrl']
		)

	if created:
		print('Product Saved.')
	else:
		print('Product Already Exists')


a = Product.objects.all()
all_products = Product.objects.all()

apl = len(all_products)
cntr = 0
for i in range(5):
	t = time.time()
	productId = a[i].productId
	print('productId=', productId)

	try:
		product_page_extract(productId)
	except Exception:
		err = str(traceback.format_exc())
		e, created = Err.objects.get_or_create(
				productId = productId,
				file_name = 'helper.py',
				func_name = 'product_page_extract',
				err = err
			)
	tt = time.time()
	ttt = round(tt-t,2)
	print('CPPT: {} secs'.format(ttt))
	cntr += 1
	print('Products Remaining: {}'.format(apl-cntr))
	print('-------------------------------------------------------------------------------------------------')
