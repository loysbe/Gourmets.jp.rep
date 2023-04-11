import requests
from bs4 import BeautifulSoup

# url = 'https://www.google.com'
url = 'https://www.amazon.co.jp/'
url_param = 's?k=鴨+フォアグラ'

session = requests.Session()

my_headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' + 
' (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

session.headers.update(my_headers)

# req = session.get(url+url_param, headers=my_headers)
req = session.get(url+url_param)

print(req.text)
# print(r.request.headers)

bs = BeautifulSoup(req.text,'html.parser')
products = bs.find('div', {'data-asin': True})

for p in products:
    print(p)