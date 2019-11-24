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
import concurrent.futures
import sys
from pages.models import *

application = get_wsgi_application()


st = time.time()
start = time.perf_counter()

def slicer(d, s, e):
	return d[d.index(s)+len(s):d.index(e)]

def get_tot_sales_count(d):
	try:
		return int(slicer(d=d, s='","tradeCount":', e=',"tradeCountUnit":"orders"'))
	except:
		return -1

def get_stock_available(d):
	try:
		return int(slicer(d=d, s=',"totalAvailQuantity":', e='},"buyerProtectionModule":{'))
	except:
		return -1

def get_store_rating(d):
	try:
		s=',"positiveRate":"'
		si=d.index(s)+len(s)
		ns=d[si:si+10]
		return float(ns[:ns.index('%')])
	except:
		return -0.01

def get_product_rating(d):
	try:
		return float(slicer(d=d, s=',"evarageStar":"', e='","evarageStarRage":"'))
	except:
		return -0.01

def get_shipping_country(d):
	try:
		s = '"Ships From","skuPropertyValues":'
		si = d.index(s)+len(s)
		ns = d[si:si+3000]
		ei = ns.index(']')+1
		st = ns[:ei]
		res = []
		di=ast.literal_eval(st)
		for i in di:
			res.append(i['propertyValueDisplayName'])
		return str(res)
	except:
		return []

def req_mkr(productId):
	t=time.time()
	# Collect and parse first page
	page = requests.get('https://www.aliexpress.com/item/{}.html'.format(productId))
	tt=time.time()
	ttt = round((tt - t), 1)

	print('Request compleated in {} seconds'.format(ttt))

	d = page.text
	return d

def get_price_range(d):
	try:
		s='"formatedActivityPrice":"'
		e='","formatedPrice":'
		si = d.index(s)+len(s)
		ei = d.index(e)
		prs = d[si:ei]
		prs = prs.replace('US $','')
		pr = prs.replace(' ', '')
		if '-' in pr:
			pl = pr.split('-')
			pr = {'min': float(pl[0]), 'max': float(pl[1])}
		else:
			pr = {'min': float(pr), 'max': float(pr)}
		return pr
	except:
		return {'min': -0.1, 'max': -0.1}

def test(productId):
	time.sleep(0.35)
	print(productId, 'Processing.............')
	headers = {
		'authority': 'www.aliexpress.com',
		'method': 'GET',
		'path': '/item/{}.html'.format(productId),
		'scheme': 'https',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'none,',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
	}



	t=time.time()
	# Collect and parse first page
	page = requests.get('https://www.aliexpress.com/item/{}.html'.format(productId))
	tt=time.time()
	ttt = round((tt - t), 1)

	# print('Request compleated in {} seconds'.format(ttt))

	d = page.text

	if '","tradeCount":' in d:
		Product.objects.filter(productId=productId).update(
			storeRating = get_store_rating(d),
			rating = get_product_rating(d),
			stockAvailable = get_stock_available(d),
			shippingCountries = get_shipping_country(d),
			totSalesCount = get_tot_sales_count(d),
			productListingHasVideo = 'videoId' in d,
			minPrice = get_price_range(d)['min'],
			maxPrice = get_price_range(d)['max'],
			)
		print('{} updated'.format(productId))
		print('Total Sales Count: {}'.format(get_tot_sales_count(d)))
		global processed_products
		processed_products += 1
		global updated_suc
		updated_suc += 1
		print('Products Remaining: {}'.format(tot_products - processed_products))
		print('Total Elapsed Time: {} min(s).'.format(round(((time.time()-st)/60),2)))
		return '{} updated'.format(productId)
	else:
		print('Status'+ 'Product Listing Removed or Other Error', 'Product ID: {}'.format(productId))
		global processed_products
		processed_products += 1
		global err
		err += 1
		print('Products Remaining: {}'.format(tot_products - processed_products))
		print('Total Elapsed Time: {} min(s).'.format(round(((time.time()-st)/60),2)))
		return {'Status': 'Product Listing Removed or Other Error', 'Product ID': productId}


# po = Product.objects.all().values_list('productId')
po = Product.objects.filter(totSalesCount=0.0).values_list('productId')
productIds = [i[0] for i in po]
tot_products = len(productIds)
processed_products = 0
updated_suc = 0
err = 0

# with concurrent.futures.ThreadPoolExecutor() as executor:
# 	results = executor.map(test, productIds)
for i in productIds:
	test(i)
	print("{} products processed in {} min(s).".format(processed_products, round((time.time()-st)/60.0,2)))
	print("Remaining Products: {}".format(tot_products - processed_products))
et = time.time()
nt = round(et-st,2)
print('\nMine Process Compleated in {} second(s).'.format(nt))



finish = time.perf_counter()
tn = (finish-start)/60.0
print('Finished in {} min(s)'.format(round(tn, 2)))

print('Success {}: '.format(updated_suc))
print('Err {}: '.format(err))
print("Verification: {}".format(tot_products - (err+updated_suc)))
