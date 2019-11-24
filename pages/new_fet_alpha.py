import requests
import time
import ast
import concurrent.futures
from pages.models import *

st = time.time()
start = time.perf_counter()

with open('cookie.txt', 'r') as file:
	cookie = file.read().replace('', '')


def slicer(d, s, e):
	return d[d.index(s)+len(s):d.index(e)]

def get_tot_sales_count(d):
	return int(slicer(d=d, s='","tradeCount":', e=',"tradeCountUnit":"orders"'))

def get_stock_available(d):
	return int(slicer(d=d, s=',"totalAvailQuantity":', e='},"buyerProtectionModule":{'))

def get_store_rating(d):
	s=',"positiveRate":"'
	si=d.index(s)+len(s)
	ns=d[si:si+10]
	return float(ns[:ns.index('%')])

def get_product_rating(d):
	return float(slicer(d=d, s=',"evarageStar":"', e='","evarageStarRage":"'))

def get_shipping_country(d):
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

def test(productId):
	print(productId, 'Processing.............')
	headers = {
		'authority': 'www.aliexpress.com',
		'method': 'GET',
		'path': '/item/{}.html'.format(productId),
		'scheme': 'https',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
		'cache-control': 'max-age=0',
		'cookie': cookie,
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'none,',
		'sec-fetch-user': '?1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
	}



	t=time.time()
	# Collect and parse first page
	page = requests.get('https://www.aliexpress.com/item/{}.html'.format(productId))
	tt=time.time()
	ttt = round((tt - t), 1)

	print('Request compleated in {} seconds'.format(ttt))

	d = page.text

	if '","tradeCount":' in d:
		Product.objects.filter(productId=productId).update(
			storeRating = get_store_rating(d),
			rating = get_product_rating(d),
			stockAvailable = get_stock_available(d),
			shippingCountries = get_shipping_country(d),
			totSalesCountv = get_tot_sales_count(d),
			productListingHasVideo = 'videoId' in d,
			minPrice = get_price_range(d)['min'],
			maxPrice = get_price_range(d)['max'],
			)
		return '{} updated'.format(productId)
	else:
		return {'Status': 'Product Listing Removed or Other Error', 'Product ID': productId}

cntr = 0
products = Product.objects.all()

tot_prds = len(products)

def calc_nums(product):
	global cntr
	cntr += 1
	n = (product.maxPrice+product.shippingPrice)*product.avgDailySale
	Product.objects.filter(productId=product.productId).update(nums=n)
	print(productId, n)
	print('Total Processed: ', cntr)
	r = tot_prds - cntr
	print('Remaining: ', r)
	return {product.productId:n}

with concurrent.futures.ThreadPoolExecutor() as executor:
	results = executor.map(calc_nums, products)


et = time.time()
nt = round(et-st,2)
print('\nMine Process Compleated in {} second(s).'.format(nt))


finish = time.perf_counter()

# for i in results:
#	 print('------------------------------------------------------------------------------------------')
#	 for j in i.keys():
#		 print(j, i[j])

print('Finished in {} second(s)'.format(round(finish-start, 2)))

