import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AliExpressScraper.settings')

import django
django.setup()
from django.core.wsgi import get_wsgi_application
from vv_products.models import *

import pickle

import urllib.parse
import ast
import requests
import time
import json
import datetime

application = get_wsgi_application()


def del_db():
    pickle_out = open("vv_products.pickle","wb")
    pickle.dump({}, pickle_out)
    pickle_out.close()

def read_db():
    pickle_in = open("vv_products.pickle","rb")
    return(pickle.load(pickle_in))


def append_to_db(k,v):
    old_val = read_db()
    old_val[k] = v
    pickle_out = open("vv_products.pickle","wb")
    pickle.dump(old_val, pickle_out)
    pickle_out.close()


def get_from_db():
    all_raw_data = RawData.objects.all()

    for raw_data in all_raw_data:
        raw_data_dict = ast.literal_eval(raw_data.data)

        for product in raw_data_dict['results']:
            k = product['pk']
            v = {}
            
            v['vvpk'] = product['pk']
            v['title'] = product['title']
            v['category'] = product['category']
            v['timestamp'] = product['timestamp']
            v['description'] = product['description']
            v['fb_targeting'] = product['fb_targeting']
            v['cogs'] = product['cogs']
            v['price'] = product['price']
            v['profit'] = product['profit']
            v['favorite'] = product['favorite']
            try:
                v['fb_url'] = product['facebook']['url']
                v['likes'] = product['facebook']['likes']
                v['comments'] = product['facebook']['comments']
                v['redirects'] = product['facebook']['redirects']
            except:
                print(k)
                v['fb_url'] = ''
                v['likes'] = 0.0
                v['comments'] = 0.0
                v['redirects'] = 0.0
            v['aliexpress1'] = product['aliexpress1']
            v['aliexpress2'] = product['aliexpress2']
            v['amazon1'] = product['amazon1']
            v['amazon2'] = product['amazon2']
            v['competitor_store'] = product['competitor_store']
            v['aliexpress_data'] = product['aliexpress_data']
            v['images'] = product['images']
            v['ad_creative'] = product['ad_creative']

            append_to_db(k, v)


# del_db()
# db = read_db()

def add_vv_product_to_django_db():
    for p in db:
        new_vv_p = VvProduct()

        new_vv_p.vvpk = 0 if db[p]['vvpk'] == None else db[p]['vvpk']
        new_vv_p.title = '' if db[p]['title'] == None else db[p]['title']
        new_vv_p.category = '' if db[p]['category'] == None else db[p]['category']
        new_vv_p.timestamp = '' if db[p]['timestamp'] == None else db[p]['timestamp']
        new_vv_p.description = '' if db[p]['description'] == None else db[p]['description']
        new_vv_p.fb_targeting = '' if db[p]['fb_targeting'] == None else db[p]['fb_targeting']
        new_vv_p.cogs = 0.0 if db[p]['cogs'] == None else float(db[p]['cogs'])
        new_vv_p.price = 0.0 if db[p]['price'] == None else float(db[p]['price'])
        new_vv_p.profit = 0.0 if db[p]['profit'] == None else float(db[p]['profit'])
        new_vv_p.favorite = '' if db[p]['favorite'] == None else db[p]['favorite']
        new_vv_p.fb_url = '' if db[p]['fb_url'] == None else db[p]['fb_url']
        new_vv_p.likes = 0.0 if db[p]['likes'] == None else float(db[p]['likes'])
        new_vv_p.comments = 0.0 if db[p]['comments'] == None else float(db[p]['comments'])
        new_vv_p.redirects = 0.0 if db[p]['redirects'] == None else float(db[p]['redirects'])
        new_vv_p.aliexpress1 = '' if db[p]['aliexpress1'] == None else db[p]['aliexpress1']
        new_vv_p.aliexpress2 = '' if db[p]['aliexpress2'] == None else db[p]['aliexpress2']
        new_vv_p.amazon1 = '' if db[p]['amazon1'] == None else db[p]['amazon1']
        new_vv_p.amazon2 = '' if db[p]['amazon2'] == None else db[p]['amazon2']
        new_vv_p.competitor_store = '' if db[p]['competitor_store'] == None else db[p]['competitor_store']
        new_vv_p.aliexpress_data = '[]' if db[p]['aliexpress_data'] == None else db[p]['aliexpress_data']
        new_vv_p.images = '' if db[p]['images'] == None else db[p]['images']
        new_vv_p.ad_creative = '' if db[p]['ad_creative'] == None else db[p]['ad_creative']

        new_vv_p.save()
        
        print(p)

def update_urls():
    all_vv_ps = VvProduct.objects.all()
    for p in all_vv_ps:
        print(p.pk)
        l=[1068, 1069, 1070, 1071, 1380, 1509, 1520, 1610]

        if p.pk in l:
            category_ext = '' if ((p.category == None) or (p.category == '')) else ast.literal_eval(p.category)['title']
            aliexpress1_url = p.aliexpress1
            aliexpress2_url = p.aliexpress2
            amazon1_url = p.amazon1
            amazon2_url = p.amazon2

            VvProduct.objects.filter(pk=p.pk).update(
                category_ext = category_ext,
                aliexpress1_url = aliexpress1_url,
                aliexpress2_url = aliexpress2_url,
                amazon1_url = amazon1_url,
                amazon2_url = amazon2_url,
            )
        else:
            category_ext = '' if ((p.category == None) or (p.category == '')) else ast.literal_eval(p.category)['title']
            aliexpress1_url = '' if ((p.aliexpress1 == None) or (p.aliexpress1 == '')) else ast.literal_eval(p.aliexpress1)['url']
            aliexpress2_url = '' if ((p.aliexpress2 == None) or (p.aliexpress2 == '')) else ast.literal_eval(p.aliexpress2)['url']
            amazon1_url = '' if ((p.amazon1 == None) or (p.amazon1 == '')) else ast.literal_eval(p.amazon1)['url']
            amazon2_url = '' if ((p.amazon2 == None) or (p.amazon2 == '')) else ast.literal_eval(p.amazon2)['url']
            

            video = '' if ((p.ad_creative == None) or (p.ad_creative == '') or (ast.literal_eval(p.ad_creative)['product_video'] == None)) else 'https://app.tryviralvault.com/' + ast.literal_eval(p.ad_creative)['product_video']
            video_thumbnail = '' if ((p.ad_creative == None) or (p.ad_creative == '') or (ast.literal_eval(p.ad_creative)['thumbnail'] == None)) else 'https://app.tryviralvault.com/' + ast.literal_eval(p.ad_creative)['thumbnail']
            ad_copy1 = '' if ((p.ad_creative == None) or (p.ad_creative == '') or (ast.literal_eval(p.ad_creative)['option1'] == None)) else ast.literal_eval(p.ad_creative)['option1']
            ad_copy2 = '' if ((p.ad_creative == None) or (p.ad_creative == '') or (ast.literal_eval(p.ad_creative)['option2'] == None)) else ast.literal_eval(p.ad_creative)['option2']
        
            VvProduct.objects.filter(pk=p.pk).update(
                category_ext = category_ext,
                aliexpress1_url = aliexpress1_url,
                aliexpress2_url = aliexpress2_url,
                amazon1_url = amazon1_url,
                amazon2_url = amazon2_url,
                video = video,
                video_thumbnail = video_thumbnail,
                ad_copy1 = ad_copy1,
                ad_copy2 = ad_copy2
            )

update_urls()