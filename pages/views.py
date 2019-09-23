from django.views.generic import TemplateView
from django.shortcuts import render
from .models import *
import urllib.parse
import ast

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