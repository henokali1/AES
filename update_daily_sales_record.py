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


def daily_sales_helper(productId):
	# for i in products:
	# cntr += 1
	# tt = time.time()
	# productId = i.productId
	print('{} Processing........'.format(productId))
	try:
		c = Cookie.objects.all()[0].cookie
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

		Product.objects.filter(productId=productId).update(
			imageUrl = data['imageUrl'],
			logisticsReliability = data['logisticsReliability'],
			sellerDsSupplier = data['sellerDsSupplier'],
			storeUrl = data['storeUrl'],
			)

		for i in data['saleVolume']:
			date_list = i.split('-')
			date = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
			units_sold = data['saleVolume'][i]

			new_d_sale, created = DailySale.objects.get_or_create(
				quantitySold = units_sold,
				date = date,
				product = Product.objects.filter(productId=productId)[0],
			)

			if created:
				print('Product Sales Data Saved.')
			else:
				print('Product Sales Data Already Exists')

		
		try:
			mv = calcMeanVar(productId)
			Product.objects.filter(productId=productId).update(
					avgDailySale=mv['mean'],
					dailySaleVariance=mv['variance']
				)
			print('M&V Updated: ', mv)
		except:
			print('Couldn\'t update M&V 	', productId)
		# tElapsed = round((time.time()-t)/60.0, 2)
		# singTime = round(time.time()-tt, 2)
		# remProducts = totProds - cntr
		# print('Products remaining: {},	Elapsed Time: {} mins,	CPPT: {} sec'.format(remProducts, tElapsed, singTime))
	
	except:
		print('Error: ', productId)

def update_daily_sales_record():
	t = time.time()
	min_order_count = 50
	products = Product.objects.filter(totSalesCount__gte=min_order_count).values_list('productId')
	product_ids = [i[0] for i in products]
	totProds = len(product_ids)
	cntr = 0
	with concurrent.futures.ThreadPoolExecutor() as executor:
		results = executor.map(daily_sales_helper, product_ids)
	tt = time.time()
	ttt = round(tt-t,2)/60.0
	print('Daily Sales of {} products compleated in {} min(s).'.format(totProds, ttt))
	args = {}

update_daily_sales_record()