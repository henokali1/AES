from django.views.generic import TemplateView
from django.shortcuts import render
from .models import *
import urllib.parse
import ast
import requests
import time
import json
import datetime

# Helper Functions
# ---------------------------------------------------------------------------
def parsePrice(p):
    if '-' in p:
        pl = p.replace(',', '').split(' - ')
        price = {'min': float(pl[0]), 'max': float(pl[1])}
        return price
    else:
        pf = float(p.replace(',', '').strip())
        price = {'min': pf, 'max': pf}
        return price
# ---------------------------------------------------------------------------

def pages(request):
	return render(request, 'pages/dashboard.html')


def all_categories(request):
	categories = CategorieUrl.objects.all()
	args={'categories': categories}
	return render(request, 'pages/all-categories.html', args)


def cat_urls(request, cat_urls):
	urls = str(request.get_full_path())
	urls = urls[22:]
	sp = urls.split(',')
	
	for url in sp:
		url, created = CategorieUrl.objects.get_or_create(url=url)

		if created:
		   print("{} added".format(url))
		else:
		   print("{} already exists".format(url))

	args={'cats':cat_urls}
	return render(request, 'pages/cats.html', args)

def save_products(request, products):
	raw_products = urllib.parse.unquote(request.get_full_path())[38:]
	products_dict = ast.literal_eval(raw_products)
	
	for product in products_dict:
		prod = products_dict[product]
		productId = prod['productId']
		new_product, created = Product.objects.get_or_create(
				productId = productId,
				rating = prod['rating'],
				productTitle = prod['productTitle'],
				minPrice = parsePrice(prod['currentPrice'])['min'],
				maxPrice = parsePrice(prod['currentPrice'])['max'],
				storeName = prod['storeName'],
				totSalesCount = prod['totSalesCount'],
			)

		if created:
			print('Product Saved.')
		else:
			print('Product Already Exists')

	args={'products':'Saved'}
	return render(request, 'pages/save_products.html', args)

def products_srtd_order(request):
	min_order_count = 1000
	products = Product.objects.filter(totSalesCount__gte=min_order_count).order_by('-totSalesCount')
	args={
		'products': products,
		'min_order_count': min_order_count,
	}
	return render(request, 'pages/products_srtd_order.html', args)

def update_cookie(request, cookie):
	new_cookie = urllib.parse.unquote(request.get_full_path())[29:]
	Cookie.objects.filter(pk=1).update(cookie=new_cookie)
	args = {}
	return render(request, 'pages/update-cookie.html', args)

def update_daily_sales_record(request):
	t = time.time()
	c = Cookie.objects.all()[0].cookie

	min_order_count = 1000
	products = Product.objects.filter(totSalesCount__gte=min_order_count).order_by('-totSalesCount')

	for i in products:
		tt = time.time()
		productId = i.productId
		print(productId)
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
			print('tt Time:', time.time()-tt)
			print('Tot Time:', time.time()-t)
		except:
			print('Error: ', productId)
	args = {}
	return render(request, 'pages/update-daily-sales-record.html', args)
