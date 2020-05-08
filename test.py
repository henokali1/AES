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

application = get_wsgi_application()

t = time.time()
prod_id = '32975528835'

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
for p in range(667,10000,1):
    page = p
    url = 'https://newapi.spocket.co/dropshippers/listings?keywords=&category=&category_id=&min_price=&max_price=&ships_from=&ships_to=&supplier_name=&sort_by=&premium=&ethically_sourced=&origin_usa=&high_inventory=&under_5_dollar=&free_usa_shipping=&minimum_inventory=&collection_id=&page={}&seed=1588890078180'.format(page)

    response = requests.get(url, headers=headers)

    print(time.time() - t)

    d = json.loads(response.text)

    for i in d:
        print(i['id'], i['total_inventory'])
        
        try:
            new_d_sale, created = SpDailySale.objects.get_or_create(
                sp_id = i['id'],
                total_inventory = i['total_inventory'],
            )

            if created:
                print('SP Product Sales Data Saved.')
            else:
                print('SP Product Sales Data Already Exists')
            suc += 1
        except:
            print(i['id'])
            err += 1
    print('Page: ', page)

print('Suc', suc)
print('Err', err)
