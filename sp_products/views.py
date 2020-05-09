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
from django.http import JsonResponse


def tst(request):
	return JsonResponse({'one':'1', 'two':'2', 'three':'3'})

def sp_products_all(request):
	srt_by = 'pushed_count'
	args={}
	if request.method == 'POST':
		srt_by = request.POST['srt_by']
		print(srt_by)
	if request.method == 'GET':
		try:
			srt_by = request.GET['srt_by']
		except:
			pass
	all_products = SpProduct.objects.all().order_by('-'+srt_by)

	page = request.GET.get('page', 1)

	paginator = Paginator(all_products, 12)
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)

	args['srt_by'] = srt_by
	args['len'] = len(products)
	args['products'] = products
	return render(request, 'sp_products/sp_products_all.html', args)