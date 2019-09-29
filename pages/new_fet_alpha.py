# ---------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------- Extracts Product info from product page --------------------------------------------------------------------------------
# import requests
# import json
# import time
# import ast

# with open('cookie.txt', 'r') as file:
#     cookie = file.read().replace('\n', '')


# productId = '33012206693'


# headers = {
#     'authority': 'www.aliexpress.com',
#     'method': 'GET',
#     'path': '/item/{}.html'.format(productId),
#     'scheme': 'https',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
#     'cache-control': 'max-age=0',
#     'cookie': cookie,
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'none,',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
# }


# def getShippingCountry(st):
#     res = []
#     di=ast.literal_eval(st)
#     for i in di:
#         res.append(i['propertyValueDisplayName'])
#     return res

# def key_extractor(obj_str, s, e):
#     return obj_str[obj_str.index(s)+len(s):obj_str.index(e)]

# t=time.time()
# # Collect and parse first page
# page = requests.get('https://www.aliexpress.com/item/{}.html'.format(productId))
# tt=time.time()
# ttt = round((tt - t), 1)

# print('Request compleated in {} seconds'.format(ttt))

# d = page.text
# total_orders = d[d.index('"tradeCount"')+13:d.index('"tradeCountUnit"')-1]

# product_rating = key_extractor(d, '{"averageStar":"', '","averageStarRage":"')
# price_range = key_extractor(d, '"formatedActivityPrice":"', '","formatedPrice":')
# shipping_countries = getShippingCountry(key_extractor(d, '"Ships From","skuPropertyValues":[', ']}],"skuPriceList":[{'))
# stock_available = key_extractor(d, ',"totalAvailQuantity":', '},"buyerProtectionModule":{"')
# store_rating = key_extractor(d, ',"positiveRate":"', '%","productId":')
# product_has_video = 'video' in d

# print('total_orders',total_orders)
# print('product_rating',product_rating)
# print('price_range',price_range)
# print('shipping_countries', shipping_countries)
# print('stock_available', stock_available)
# print('store_rating', store_rating)
# print('product_has_video',product_has_video)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
