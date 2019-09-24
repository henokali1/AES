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

def update_daily_sales_record(request):
	t = time.time()
	c = Cookie.objects.all()[0].cookie

	min_order_count = 1000
	products = Product.objects.filter(totSalesCount__gte=min_order_count, imageUrl="").order_by('-totSalesCount')

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
				'cookie': 'ali_apache_id=11.10.10.216.1560257450113.181875.5; cna=tJGGFaaf2BkCAdmlPoaudY9K; _ga=GA1.2.2086528475.1560257495; UM_distinctid=16b46981341271-0984a2e591f604-37c153e-190140-16b46981342954; _fbp=fb.1.1560257513135.1230507670; _ym_uid=1560281048438567126; _ym_d=1560281048; aep_common_f=gkcB93n0ZEN3tVnTS53xtpn56tkiuMc5Ml1x06lqUsIL95rwBDirSw==; aeu_cid=0c098a1173944de7889e2c59a4c50659-1568314878065-03312-mun2n2V; _gid=GA1.2.1122957333.1568809427; __utma=3375712.2086528475.1560257495.1561487400.1568967599.5; __utmz=3375712.1568967599.5.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0933013343694%0932951086764%0932975528835%0932996560430%0932975528835%0932857747008%0932846217047%0932975528835; acs_usuc_t=x_csrf=epdpv3310yhg&acs_rt=8020f74ac63643918b9e31226cc4ab12; intl_locale=en_US; AKA_A2=A; _m_h5_tk=9906f7e896342360eed54b20d506bf21_1569271662675; _m_h5_tk_enc=a11b21143436fa2c7ffac5d8a4e298c3; _hvn_login=13; xman_us_t=x_lid=ae1238700677mvdr&sign=y&x_user=4fmeybhA7LaLchjBcIaw996SwSkI/IYzAN2GvtVnpLw=&ctoken=160ckl3q3llk4&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A2; xman_f=1Kw1AGw1RF/JYEKY+ahRn9pyYCKxxSZ7cX8uIv1it6/YXAhggE3qZi2QRcmybrNrM/Cbwen4BBkKswThQSXc1b2AMNPk1eZ3P5+f8D3QAoXDgTfnH/EyIluWFvCJUK1+PYUVp37knc6zVTm7Oyu51/YOfDeBV9CBdcEkSvDi8U/XpMr+WKRD8LIMUK9DCwayAAQ13XRZekMJfhuBJuaWFjzOfNGdidU7h/CSBe9XgbTfVtFLYZwXVwOAaf6pwiC19cEqLmrxjql5CK6dcFJxNMutDpyf3CocKft5/Ycip5CJzGCPdpfpL3YlWDjRSvA2PVFw3AQI/jnSUrN8FCNtw2PrhNhu79flVwAe0lEx3SRHvdtr16V9yxiaYFZSxTyXZPf8rwv14oDa0xP0PUi5PX5q9P4Fnu3ZuBgy71A0dZ915MxtnIDqrw==; xman_us_f=zero_order=n&x_locale=en_US&x_l=0&last_popup_time=1560257481856&x_user=AE|henok|ali|ifm|858029949&no_popup_today=n&x_as_i=%7B%22aeuCID%22%3A%220c098a1173944de7889e2c59a4c50659-1568314878065-03312-mun2n2V%22%2C%22af%22%3A%221612068995%22%2C%22affiliateKey%22%3A%22mun2n2V%22%2C%22channel%22%3A%22AFFILIATE%22%2C%22cv%22%3A%227%22%2C%22ms%22%3A%221%22%2C%22tagtime%22%3A1568314878065%7D; aep_usuc_f=isfm=y&site=glo&aep_cet=mobile&c_tp=USD&x_alimid=858029949&re_sns=google&isb=y&region=US&b_locale=en_US; ali_apache_tracktmp=W_signed=Y; intl_common_forever=7ZcBY/FLPF9ek6lmpesF7XPAjrrskFU9O2HMdwtYdZ+KggWqVsDnng==; ali_apache_track=mt=1|ms=|mid=ae1238700677mvdr; xman_t=n4XnZ0tZWuGbfHEgQYB4v1l+BBO3aJs/TxzYsAqU5QAgtKr3gKKanp2oeRNZHvIalymX2YrpItDB8LBZ7fw6I/A1GViDNt8E/iSEwP1/EFlHKKbAs7n28aio6Hikv3P9PpkArCaPwSx/v5lRB0stdXHL7KNs025J1Hpdm8D56RpKyZI3xvP52E2SASuxPguArQbj/Eq04ucp4irjAzoE9w/05c8ecXl8T3sss+QSRPsWZbiJB7+BkjDjbSEFrmHItyfi4iOK03pvycNY3pOjbG/why7iqPL7onSDZ9IKdmJM2+NqzPreELrh+HfcQGztjZithYF40LhPRH037Bo2BTVvVhNQ8ftfqnPYEWssiwhBUO1i5EM8scEnPu0m1WQCqZBe82QRMya63L+JwJIq/QRcQ0LlGOfgs0y2sn+A3Ux9cVkHrVk/IpT7DNeiFDzetT4W0sXA7xmhtNdrM+Xt4xaXs7J07zjuqQGqndsLTYnRdiROc9ztuOYbz/k5qjDuQjDJNTj0L1pI1IWHUTI5E0R7dY/YYUFqTT/zn0wSN6gS25NOmBWEWQWTDvbF2UubTRYit8eLylwDEzXftkiUO/NWI+tKo1sn1XuCM9BnqiBJi+weGtMNYSJWxgqljcPkWDraDphMCb5ROnZ/AHVXKw==; RT="sl=2&ss=1569269418232&tt=26781&obo=0&sh=1569269467291%3D2%3A0%3A26781%2C1569269436138%3D1%3A0%3A17856&dm=aliexpress.com&si=cd49cf73-2f5d-4467-8396-c81f527681be&se=900&bcn=%2F%2F686eb51a.akstat.io%2F&ld=1569269467292&r=https%3A%2F%2Fwww.aliexpress.com%2F&ul=1569269509555&hd=1569269511930"; l=cBPkM9XPvQfD1fq1BOCaourza7798IRYiuPzaNbMi_5iz9T1gFbOk1sF_h96DAWdtYYB4JuaUM29-etkwX2Gv268ieSF.; isg=BJmZpF81IIHAzf1jiERcqPe7qIV5p2AQVH704LtOQUA_wrlUA3TzqAHTxd4RxSUQ',
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
