from django.views.generic import TemplateView
from django.shortcuts import render
from .models import *
import urllib.parse
import ast
import requests
import time
import json
import datetime
from statistics import variance, mean
import concurrent.futures
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def vv_product_all(request):
    args={}
    all_products = VvProduct.objects.all().order_by('-likes')

    page = request.GET.get('page', 1)

    paginator = Paginator(all_products, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # products = products[0:12]
    args['products'] = products

    args['len'] = len(products)
    args['products'] = products
    return render(request, 'vv_products/vv_product_all.html', args)

def vv_product(request, pk):
    product = VvProduct.objects.all().filter(pk=pk)[0]
    args = {'product': product}
    return render(request, 'vv_products/vv_product.html', args)