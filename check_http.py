from datetime import datetime
import time

d = datetime.today()
print(d)
filename = r'.\log_gourmets_status_' + d.strftime("%m_%d_%Y") + '.txt'
print('write log in file ', filename)

login_pages = ['https://www.gourmets.jp/','https://blog.gourmets.jp/','https://hongo2chome.gourmets.jp/']

def save_http_status(s):
    f = open(filename,'a+',encoding='utf-8')
    f.write("%s\n" % s)
    f.close()
    return

import urllib.request
import urllib.request
import urllib.error

def start_http_monitoring(url):
    i = 0
    while 1:

        try:
            with urllib.request.urlopen(url) as f:
                # print(f.read())
                print(f.status)
                # print(f.getheader("content-length"))
                d = datetime.now()
                print(d)
                s = 'OK ' + url + ' | ' + d.strftime("%m/%d/%Y, %H:%M:%S")
                # save_http_status(s)
                time.sleep(60)
        except urllib.error.URLError as e:
            print('error', e.reason)
            d = datetime.now()
            print(d)
            s = 'ERROR ' + url + ' | ' + d.strftime("%m/%d/%Y, %H:%M:%S")
            save_http_status(s)
            if (i > 2): 
                break
            i += 1
            time.sleep(10)
    print('i = ', i)

def check_url(url):
    pass

import threading
if __name__ == '__main__':

    url = login_pages[0]
    print('connect to :', url)
    thread1 = threading.Thread(target=start_http_monitoring, args=[url])
    thread1.start()

    url = login_pages[1]
    print('connect to :', url)
    thread2 = threading.Thread(target=start_http_monitoring, args=[url])
    thread2.start()

    print('wait for the end of thread')