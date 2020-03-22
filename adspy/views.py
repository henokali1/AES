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

def time_formater(val):
    d = val.split('T')[0]
    return datetime.strptime(d, '%Y-%m-%d')

def fbads(request):
	return render(request, 'fbads/dashboard.html')

def all_ads(request):
    args = {}
    if request.method == 'POST':
        filter_opt = request.POST['filter_opt']
        args['filter']=filter_opt
        if filter_opt == 'no_filter':
            all_ads = Ad.objects.all().order_by('-likeNum')
        else:
            all_ads = Ad.objects.all().order_by('-' + filter_opt)
        print('filter_opt:',filter_opt)
    else:
        all_ads = Ad.objects.all().order_by('-likeNum')
    
    # all_ads = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(all_ads, 12)
    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)

    # ads = all_ads[0:12]
    args['ads'] = ads
    return render(request, 'fbads/all-ads.html', args)
