import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AliExpressScraper.settings')

import django
django.setup()
from django.core.wsgi import get_wsgi_application
from sp_products.models import *

import pickle

import urllib.parse
import ast
import requests
import time
import json
import datetime
from django.utils import timezone
import pytz
application = get_wsgi_application()

t = time.time()
prod_id = '32975528835'

def update_sp_daily_inv():
    headers = {
        'accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJpZCI6ImUwNTE2ZDU5LTA2N2QtNGY3Yi05OGFlLWYxYWRjZDhjMjJjMCIsInN0b3JlX2lkIjoiM2UxOTk1NjEtZTI2MC00MzcyLTgxZTUtZTBiNzBkMGZlODdiIiwiZHJvcHNoaXBwZXJfaWQiOiJmMDFiMjdlYi0wZTMxLTRkZWYtOWUxZS02NDU2ZTlmOTg0ZDQifQ.EtElIHeNbdsAldbmqy3OBtL_5T7--lw3qWYSL4oALQM',
        'Connection': 'keep-alive',
        'content-type': 'application/json',
        'Host': 'newapi.spocket.co',
        'Origin': 'https://app.spocket.co',
        'Referer': 'https://app.spocket.co/search',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,'
    }


    suc = 0
    err = 0
    nw = []
    for p in range(1,700,1):
        page = p
        url = 'https://newapi.spocket.co/dropshippers/listings?keywords=&category=&category_id=&min_price=&max_price=&ships_from=&ships_to=&supplier_name=&sort_by=&premium=&ethically_sourced=&origin_usa=&high_inventory=&under_5_dollar=&free_usa_shipping=&minimum_inventory=&collection_id=&page={}&seed=1588890078180'.format(page)

        response = requests.get(url, headers=headers)

        print(time.time() - t)

        d = json.loads(response.text)

        for i in d:
            print(i['id'], i['total_inventory'])
            
            try:
                new_d_sale, created = SpDailyInv.objects.get_or_create(
                    sp_id = i['id'],
                    total_inventory = i['total_inventory'],
                )

                if created:
                    print('SP Product Sales Data Saved.')
                    nw.append(i['id'])
                else:
                    print('SP Product Sales Data Already Exists')
                suc += 1
            except:
                print(i['id'])
                err += 1
        print('Page: ', page)

    print('Suc', suc)
    print('Err', err)


def one_pg_req():
    headers = {
        'accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJpZCI6ImUwNTE2ZDU5LTA2N2QtNGY3Yi05OGFlLWYxYWRjZDhjMjJjMCIsInN0b3JlX2lkIjoiM2UxOTk1NjEtZTI2MC00MzcyLTgxZTUtZTBiNzBkMGZlODdiIiwiZHJvcHNoaXBwZXJfaWQiOiJmMDFiMjdlYi0wZTMxLTRkZWYtOWUxZS02NDU2ZTlmOTg0ZDQifQ.EtElIHeNbdsAldbmqy3OBtL_5T7--lw3qWYSL4oALQM',
        'Connection': 'keep-alive',
        'content-type': 'application/json',
        'Host': 'newapi.spocket.co',
        'Origin': 'https://app.spocket.co',
        'Referer': 'https://app.spocket.co/search',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,'
    }


    suc = 0
    err = 0
    nw = []
    page = 1
    url = 'https://newapi.spocket.co/dropshippers/listings?keywords=&category=&category_id=&min_price=&max_price=&ships_from=&ships_to=&supplier_name=&sort_by=&premium=&ethically_sourced=&origin_usa=&high_inventory=&under_5_dollar=&free_usa_shipping=&minimum_inventory=&collection_id=&page={}&seed=1588890078180'.format(page)

    response = requests.get(url, headers=headers)

    print(time.time() - t)

    d = json.loads(response.text)
    return d
# update_sp_daily_sale()

def update_sp_daily_sale(sp):
    headers = {
        'accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJpZCI6ImUwNTE2ZDU5LTA2N2QtNGY3Yi05OGFlLWYxYWRjZDhjMjJjMCIsInN0b3JlX2lkIjoiM2UxOTk1NjEtZTI2MC00MzcyLTgxZTUtZTBiNzBkMGZlODdiIiwiZHJvcHNoaXBwZXJfaWQiOiJmMDFiMjdlYi0wZTMxLTRkZWYtOWUxZS02NDU2ZTlmOTg0ZDQifQ.EtElIHeNbdsAldbmqy3OBtL_5T7--lw3qWYSL4oALQM',
        'Connection': 'keep-alive',
        'content-type': 'application/json',
        'Host': 'newapi.spocket.co',
        'Origin': 'https://app.spocket.co',
        'Referer': 'https://app.spocket.co/search',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,'
    }


    suc = 0
    err = 0
    nw = []
    for p in range(sp,700,1):
        page = p
        url = 'https://newapi.spocket.co/dropshippers/listings?keywords=&category=&category_id=&min_price=&max_price=&ships_from=&ships_to=&supplier_name=&sort_by=&premium=&ethically_sourced=&origin_usa=&high_inventory=&under_5_dollar=&free_usa_shipping=&minimum_inventory=&collection_id=&page={}&seed=1588890078180'.format(page)

        response = requests.get(url, headers=headers)

        print(time.time() - t)

        d = json.loads(response.text)

        for i in d:
            try:
                print(i['id'], i['total_inventory'])
                sp_id = i['id']
                prev_inv = SpDailyInv.objects.filter(sp_id=sp_id)[0].total_inventory
                cur_inv = i['total_inventory']
                if(prev_inv > cur_inv):
                    quantitySold = prev_inv - cur_inv
                else:
                    quantitySold = 0
                
                if quantitySold > 0:
                    new_d_sale, created = SpPrDailySale.objects.get_or_create(
                        sp_id = sp_id,
                        quantitySold = quantitySold,
                    )

                    if created:
                        print('SP Product Sales Data Saved.', quantitySold, sp_id)
                        nw.append(i['id'])
                print("Sales", sp_id, quantitySold)
                suc += 1
            except:
                print('Err: ', i['id'])
                err += 1
            try:
                SpDailyInv.objects.filter(sp_id=sp_id).update(
                    total_inventory = cur_inv,
                    date = timezone.now()
                )
                print('Inv Ref Updated', sp_id)
            except:
                print('Couldn\'t Update Inv Ref')
        print('Page: ', page)

    print('Suc', suc)
    print('Err', err)

# update_sp_daily_sale()

def anaSales():
    d=SpPrDailySale.objects.filter(quantitySold__gte=50, date=datetime.date.today()).order_by('-quantitySold')
    for i in d:
        print(i.quantitySold)
        print("https://app.spocket.co/search?listing_id={}".format(i.sp_id))

anaSales()
# update_sp_daily_sale(497)