# Ref.
# https://qiita.com/biblioteka/items/8d48087ab5e57ffa0ce5


import base64
import json
import urllib.request
import datetime
from pytz import timezone
import requests

def get_product_info():

    # ■■■■■■■■　認証情報　■■■■■■■■■■
    serviceSecret = b"SP375953_Q4Xq7PwS9Gkq16Ld"
    licenseKey = b"SL375953_iI4yIxnzLhctmex5"
    headers = {
        'Authorization' : b"ESA " + base64.b64encode( serviceSecret + b':' + licenseKey ),
        'Content-Type': 'application/json; charset=utf-8',
    }

    # ■■■■■■■■　post　■■■■■■■■■■
    # 現在時から何時間前を設定（63日以内制限あり）
    int_st=-24 #24H前を想定

    # 開始日時:jst_st 終了日時:jst_ed を生成
    # たぶんもっとスマートな生成方法があるはず
    jst_st = datetime.datetime.now(timezone('Asia/Tokyo'))+ datetime.timedelta(hours=int_st)
    jst_st ="{0:%Y-%m-%dT%H:%M:%S}".format(jst_st)
    jst_st = str(jst_st)+"+0900"

    jst_ed = datetime.datetime.now(timezone('Asia/Tokyo'))
    jst_ed ="{0:%Y-%m-%dT%H:%M:%S}".format(jst_ed)
    jst_ed = str(jst_ed)+"+0900"

    # post文字列生成
    url = 'https://api.rms.rakuten.co.jp/es/2.0/order/searchOrder/'
    data = {
        "dateType":1,
        "startDatetime":jst_st,
        "endDatetime":jst_ed
    }

    url = 'https://api.rms.rakuten.co.jp/es/1.0/item/get' #?itemUrl="espn-foie-gras-extra"'
    data = {
        "itemUrl":'espn-foie-gras-extra'
    }

    # url = 'https://api.rms.rakuten.co.jp/es/1.0/categoryapi/shop/category/get'
    # data = {
    #     "categoryId":134
    # }
    
    url = 'https://api.rms.rakuten.co.jp/es/1.0/item/get' # marche pas 有料
    url = 'https://api.rms.rakuten.co.jp/es/1.0/categoryapi/shop/category/get'
    url = 'https://api.rms.rakuten.co.jp/es/1.0/categoryapi/shop/categories/get'
    response = requests.get(
        url,
        # params = {'itemUrl': 'espn-foie-gras-extra'},
        # params = {'categorySetManageNumber':0},
        headers = headers
    )
    print('response.status',response.text)
    # print(response.itemGetResult)
    return

    # post
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()

    try:
            # APIの戻り値を格納
        json_load = json.loads(body)
    except:
        print('erreur')

    return

if __name__ == '__main__':
    get_product_info()
