import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AliExpressScraper.settings')

import django
django.setup()
from django.core.wsgi import get_wsgi_application
from adspy.models import *

import pickle

import urllib.parse
import ast
import requests
import time
import json
import datetime

application = get_wsgi_application()


def del_db():
    pickle_out = open("fbads.pickle","wb")
    pickle.dump({}, pickle_out)
    pickle_out.close()

def read_db():
    pickle_in = open("fbads.pickle","rb")
    return(pickle.load(pickle_in))


def append_to_db(k,v):
    old_val = read_db()
    old_val[k] = v
    pickle_out = open("fbads.pickle","wb")
    pickle.dump(old_val, pickle_out)
    pickle_out.close()

# del_db()
db = read_db()

def start(starting_page):
    headers = {
        'authority': 'api.adspy.com',
        'path': '/api/ad?createdBetween%5B%5D=01-Jan-2013&createdBetween%5B%5D=14-Mar-2020&orderBy=total_shares&tech%5B%5D=350&page=',
        'authorization': 'Bearer o83zoQ-p7wuq_MjWauJpx2s6ymAEH_opK_OLf1ZqUoEpkucbXmxDAfb7bsVQu4Mi0Uy_NYx_IkhVH_ef_RQEtwI-Zc-dtmfSEmGHlaQW52rUWz6GZTR5YtKUR2cWYmEXMIC_1lS3IMarBy77hw0QRxqSoGUHZxB3Ql4n_09I3dj4K5EBZ7OmvlrYO2k2ie_ZTyGp1zj4fku9AVugQ4Vqp3o3q2Xmag9BH8C0bDWhHK7-8lVw6EfZlD5x7X6EusFb5imdFhQT1NoamPLRG4lpjvJeyHrKirkpZfhzy-_K4GWSa-D2KmjvsdWDs7IOjiWfUDjbIeMbEO00JM8tBX0mRSvcAWqHlRvyJkGH_YkiS9HzmEMGnwt4lebNDPBr36r87qnIroIupecxU2uqUZOVAR_QDAKVBIU_sfOPiGkg1hTwg7I6FxB4Fq3ol8geGhjPdwOgpcsSlvVqiGhoRYdPKTZ1f3JLKIXnb84TJ8Nyqvk6iyA3-sBxi6N4Hgz58kwMT1ApbW6OqCKAhUPavtMi-ID3TAkOO5J7sleXbIj_Qvo',
        'content-md5': 'TVRVNE5ERTNOalUwT1RrM09BPT0=',
        'origin': 'https://app.adspy.com',
        'referer': 'https://app.adspy.com/ads;createdBetween=%EF%BC%BB%2201-Jan-2013%22%EF%BC%8C%2214-Mar-2020%22%EF%BC%BD;orderBy=total_shares;tech=%EF%BC%BB350%EF%BC%BD',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    for page in range(starting_page,301,1):
        url = 'https://api.adspy.com/api/ad?createdBetween%5B%5D=01-Jan-2014&createdBetween%5B%5D=13-Mar-2020&orderBy=total_shares&tech%5B%5D=350&countries%5B%5D=US&page={}'.format(page)
        t = time.time()
        response = requests.get(url, headers=headers)
        tt = round(time.time() - t, 1)
        data = json.loads(response.text)['data']
        for i in data:
            print(i['id'])
            print(i['createdOn'])
            print(i['snapshot']['likeNum'])
            print(i['snapshot']['commentsNum'])
            print(i['snapshot']['shareNum'])

            append_to_db(i['id'], i)
        
        print('--------------------------------------------------')
        print('Request compleated in {} secs'.format(tt))
        print('Remaining Pages: ', 301 - page)
        print('--------------------------------------------------')

def time_formater(val):
    d = val.split('T')[0]
    return datetime.strptime(d, '%Y-%m-%d')

def add_to_django_db(ad):
    new_ad = Ad()
    try:
        new_ad.countryStats = ad['countryStats']
    except:
        print('Err: ', str(ad['id']), 'countryStats')
    try:
        new_ad.genderStats = ad['genderStats']
    except:
        print('Err: ', str(ad['id']), 'genderStats')
    try:
        new_ad.ageStats = ad['ageStats']
    except:
        print('Err: ', str(ad['id']), 'ageStats')
    try:
        new_ad.asy_id = ad['id']
    except:
        print('Err: ', str(ad['id']), 'asy_id')
    try:
        new_ad.isIg = ad['isIg']
    except:
        print('Err: ', str(ad['id']), 'isIg')
    try:
        new_ad.text = ad['text']
    except:
        print('Err: ', str(ad['id']), 'text')
    try:
        new_ad.createdOn = ad['createdOn']
    except:
        print('Err: ', str(ad['id']), 'createdOn')
    try:
        new_ad.privacyScope = ad['privacyScope']
    except:
        print('Err: ', str(ad['id']), 'privacyScope')
    try:
        new_ad.minAge = ad['minAge']
    except:
        print('Err: ', str(ad['id']), 'minAge')
    try:
        new_ad.maxAge = ad['maxAge']
    except:
        print('Err: ', str(ad['id']), 'maxAge')
    try:
        new_ad.actor = ad['actor']
    except:
        print('Err: ', str(ad['id']), 'actor')
    try:
        new_ad.countries = ad['countries']
    except:
        print('Err: ', str(ad['id']), 'countries')
    try:
        new_ad.genders = ad['genders']
    except:
        print('Err: ', str(ad['id']), 'genders')
    try:
        new_ad.snapshot = ad['snapshot']
    except:
        print('Err: ', str(ad['id']), 'snapshot')
    try:
        new_ad.attachments = ad['attachments']
    except:
        print('Err: ', str(ad['id']), 'attachments')
    try:
        new_ad.comments = ad['comments']
    except:
        print('Err: ', str(ad['id']), 'comments')
    try:
        new_ad.adType = ad['adType']
    except:
        print('Err: ', str(ad['id']), 'adType')
    try:
        new_ad.linkToAd = ad['linkToAd']
    except:
        print('Err: ', str(ad['id']), 'linkToAd')
    try:
        new_ad.mainAttachment = ad['mainAttachment']
    except:
        print('Err: ', str(ad['id']), 'mainAttachment')
    try:
        new_ad.height = ad['height']
    except:
        print('Err: ', str(ad['id']), 'height')
    try:
        new_ad.likeNum = float(ad['snapshot']['likeNum'])
    except:
        print('Err: ', str(ad['id']), 'likeNum')
    try:
        new_ad.commentsNum = float(ad['snapshot']['commentsNum'])
    except:
        print('Err: ', str(ad['id']), 'commentsNum')
    try:
        new_ad.shareNum = float(ad['snapshot']['shareNum'])
    except:
        print('Err: ', str(ad['id']), 'shareNum')
    try:
        new_ad.imageUrl = ad['attachments'][0]['imageUrl']
    except:
        print('Err: ', str(ad['id']), 'imageUrl')
    try:
        type_ = ad['attachments'][0]['type']
        if type_ == 'Video':
            new_ad.hasVideo = True
            new_ad.videoUrl = ad['attachments'][0]['videoUrl']
    except:
        print('Err: ', str(ad['id']), 'videoUrl')

    
    new_ad.save()

db = read_db()
for i in db:
    add_to_django_db(db[i])

a = Ad.objects.all()
