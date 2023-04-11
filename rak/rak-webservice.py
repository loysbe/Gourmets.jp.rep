# Ref.
# https://qiita.com/baraobara/items/4ded9dce0ed042703819

import requests


url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'
payload = {
    'applicationId': ,
    'hits': 30,
    'shopCode':'グルメ・ジャポン',
    'page':1,
    'postageFlag':1,
    #'genreId':101164,
    }
r = requests.get(url, params=payload)