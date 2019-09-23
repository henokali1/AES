import requests
import time
import json


t = time.time()
url = 'https://home.aliexpress.com/dropshipper/product_analysis_ajax.htm?productId=32975528835'

headers = {
    'authority': 'home.aliexpress.com',
    'method': 'GET',
    'path': '/dropshipper/product_analysis_ajax.htm?productId=32975528835',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br,',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'ali_apache_id=11.10.10.216.1560257450113.181875.5; cna=tJGGFaaf2BkCAdmlPoaudY9K; _ga=GA1.2.2086528475.1560257495; UM_distinctid=16b46981341271-0984a2e591f604-37c153e-190140-16b46981342954; _fbp=fb.1.1560257513135.1230507670; _ym_uid=1560281048438567126; _ym_d=1560281048; aep_common_f=gkcB93n0ZEN3tVnTS53xtpn56tkiuMc5Ml1x06lqUsIL95rwBDirSw==; aeu_cid=0c098a1173944de7889e2c59a4c50659-1568314878065-03312-mun2n2V; _gid=GA1.2.1122957333.1568809427; __utma=3375712.2086528475.1560257495.1561487400.1568967599.5; __utmz=3375712.1568967599.5.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932968366680%0933013343694%0932951086764%0932975528835%0932996560430%0932975528835%0932857747008%0932846217047; acs_usuc_t=x_csrf=bzksaq4qp0cj&acs_rt=0bb30bdbd21e49cb99f0595b2e131350; intl_locale=en_US; _hvn_login=13; aep_usuc_t=ber_l=A2; ali_apache_track=mt=1|ms=|mid=ae1238700677mvdr; ali_apache_tracktmp=W_signed=Y; intl_common_forever=UoLAj9olmWiRiNRR20bbhGzOajuSswNKFZqO+dffP5fuH1wfDvTUIA==; JSESSIONID=WCYJ29YV-TF57Q5X1ZFZHR19RQYWP2-FKJ8CW0K-LBR41; _mle_tmp0=WvZKD3np02zjLR4gmq%2BUO%2BN8WUYJH%2BZW0S%2FNlmB18QH1HH7Jo%2BFEMC22arhTGf%2BK1a%2FyfNu65XxOr5c35EirT5J5%2FHl03tD2jwUlFLj2Ifzld7kLtyhNaqkZ9r0kbek5xtEGku6rnV0R7ocjq4gOJA%3D%3D; RT="sl=5&ss=1569238295552&tt=48093&obo=0&sh=1569238704472%3D5%3A0%3A48093%2C1569238668983%3D4%3A0%3A43062%2C1569238348395%3D3%3A0%3A37042%2C1569238339342%3D2%3A0%3A28060%2C1569238304992%3D1%3A0%3A9428&dm=aliexpress.com&si=cd49cf73-2f5d-4467-8396-c81f527681be&se=900&bcn=%2F%2F36fb78d7.akstat.io%2F&ld=1569238704473&r=https%3A%2F%2Fwww.aliexpress.com%2Fwholesale%3Fe70d5723135a7136c8ea609456dcd0d0&ul=1569238786619&hd=1569238786657"; _m_h5_tk=7b16230dd53101275a161471cccb6b3f_1569250504571; _m_h5_tk_enc=08a55b3fff1f1f413452c536579c005c; xman_us_f=x_l=0&x_locale=en_US&no_popup_today=n&x_user=AE|henok|ali|ifm|858029949&zero_order=n&last_popup_time=1560257481856&x_as_i=%7B%22aeuCID%22%3A%220c098a1173944de7889e2c59a4c50659-1568314878065-03312-mun2n2V%22%2C%22af%22%3A%221612068995%22%2C%22affiliateKey%22%3A%22mun2n2V%22%2C%22channel%22%3A%22AFFILIATE%22%2C%22cv%22%3A%227%22%2C%22ms%22%3A%221%22%2C%22tagtime%22%3A1568314878065%7D; aep_usuc_f=region=US&site=glo&b_locale=en_US&aep_cet=mobile&isb=y&re_sns=google&isfm=y&x_alimid=858029949&c_tp=USD; xman_us_t=x_lid=ae1238700677mvdr&sign=y&x_user=n11M9i5bX6vNEuXj2UpeWi03Uw0x+aatZAJuomGQj3o=&ctoken=w6m4y5h3vwrv&need_popup=y&l_source=aliexpress; xman_f=Z3SscTpJx3G9f9F3uWPTaSoF+1mYBu4hbyUpq3WK4wj6R3+CKtRk/5Oh1X3ijCWJGRCOVWM9SYyqdonEGcU7m5kmLJxamPmRvoeJINAZGEnl7McMv9cjzFADrGNXhBIXnzh9RSCiDgLEzB4/TrbZJWKT+wJlxoIE2o4LlmF5hLC03hSkDZHhQrkjjkYvZyBQssXYUPf7yvhw2XyeojrUXy371XSNCSDjkyHxaDBe9irzafdjGQjEVTvEhu5IMxAGOFy3fgrKv+Rk5cie1006Zsvs/TqyOX2LQOIr1nyBhYhFXv5c6LN3PaL6QGj4v32WN7dz9sZbxLGYmyQ4KGutZtotejuT1Vv5RKoTySZvFcMfaLxBjgoxRpJ0qfOQq5JgjNIWv1oLZAe2ikQ3BCBOrQFE8NTAsA5bOfSyXHIG/zee+TCW5+EafQ==; isg=BLKy6mwYO0XNBQYOD0HXjdi2A_iewlsVyyPvjXyLoGVQD1AJZdPx7Xsu__MWRC51; l=cBPkM9XPvQfD1PyGBOCZourza77OHIR4juPzaNbMi_5aU6L1ap_Ok1eI-Fp6cAWFMZLp4JuaUM2t6en7JyMaBQVpF7av-L1..; xman_t=6Flq9cZLpYeEvlyHndiRfgSlNW0e9BFPN5RXT4+HA3IdaOOXzQq/Bv0YhcjmWP9eNpmIVN/4/CBjEvtIyvKXMgXV5CG96MpXKc+60E9QSCWGgfFpiKR1ELg5etml8GQM3otrpCZijoAVYjlaciGPXGPH02T49hiJ1bdfqQt/LYmZ6WTTP5aJ0EaLlYjzTtSpImprdGXfW/Ibw7MiTtce91tmdlYGitz/MmRqKhv2Z8306cO7RM0bZ58hBm/iQr8Z0C6QPCADMP6PQaNFzfjfTMlJWbg1F1QHuoYXZLGElb6DlogkKnGGWiefl3ibUpK5QlWc6zeUqc0AKaw7UjqRLvLmkkRIQuOE7JTDvonp4kgolJTxVc/4OlZ6+dD1OebZm4SccflfxJMgJ7vXuqfxZS8VFrTqU/gpb+LuvgBFT0tmMqGV36yrd/HxhghX6vaTYAhGBkdnrVF369MwvljQzq54oEZn/Sr7XR2jU/i67V0g/21TeZrfkQteeRHNCQV9I33E9C0CNDU8jJBpFXv9N9ywWyMuEWQT4qRIPcnaODwsk/q1KL/yojGNr0vUGrXTAHvUUMmN0hcSM8Tbx24O9RlIkkmj49euZi6eJ0CtUTNkNzxrUdTd0nucDdfk2HLgn/jHFSI5/daF2Em4FAXRtg==',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

response = requests.get(url, headers=headers)

print(time.time() - t)

data = json.loads(response.text)['data']
print(data['id'])
