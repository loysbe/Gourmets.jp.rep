from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement
import re

firefox = True

if firefox: 
    # fp = webdriver.FirefoxProfile('C:/Users/Loys/AppData/Roaming/Mozilla/Firefox/Profiles/ax8azgih.default')
    # driver = webdriver.Firefox(firefox_profile=fp)
    driver = webdriver.Firefox(executable_path="C:\\Loys\\Google drive - ltd-japon\\Dev\\web\\Gekco\\geckodriver.exe")
else:
    options = webdriver.ChromeOptions() 
    options.add_argument('user-data-dir=C:\\Users\\Loys\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #Path to your chrome profile
    driver = webdriver.Chrome(executable_path="C:\\Loys\\Google drive - ltd-japon\\Dev\\web\\Chrome\\chromedriver.exe", chrome_options=options)

adresses = []
produits = []
user_glogin = 'GourmetsJP'
mdp = ''
user_yahoo = 'xxxxxxxxxxxxxxx@yahoo.co.jp'
mdp2 = ""

def connect_to_rms() -> bool:

    driver.get("https://glogin.rms.rakuten.co.jp/")
    try:
        # entrer le mot de passe
        user = driver.find_element_by_xpath('//input[@id="rlogin-username-ja"]')
        user.send_keys(user_glogin)    
        pwd = driver.find_element_by_xpath('//input[@id="rlogin-password-ja"]')
        pwd.send_keys(mdp)
        o = driver.find_element_by_xpath('//button[@name="submit"]')
        o.click()

        # must check if element is visible etc..
        user = driver.find_element_by_xpath('//input[@id="rlogin-username-2-ja"]')
        user.send_keys(user_yahoo)
        pwd = driver.find_element_by_xpath('//input[@id="rlogin-password-2-ja"]') 
        pwd.send_keys(mdp2)

        # check if exist and yahoo id/pwd are set
        n = '//button[@name="submit"]'
        o = driver.find_element_by_xpath(n)
        # o = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
        o.click()

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//h2[contains(text(), "お気をつけください")]')))
        o = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//button[@name="submit"]')))
        o.click()

        try:
            # driver.find_element_by_xpath('//h1[contains(text(), "R-Login管理")]')
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//h1[contains(text(), "R-Login管理")]')))
            a = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//h1[contains(text(), "利用者管理")]')))
            # '//a[contains(@href,"glogin.rms.rakuten.co.jp")]')))
            # 
            # 
            # for h in o:
            #     # h.find_element_by_xpath('./h1[contains(text(), "R-Login管理")]')
            #     if '利用者管理' in h.get_attribute('innerHTML'):
            #         a = h
            #         break
            a.click()
            
            o = driver.find_elements_by_xpath('//a[contains(@href,"mainmenu.rms.rakuten.co.jp")]')
            
            # pb ici comment differencier les 2 elts ?
            # for h in o:
            #     if 'ＲＭＳ' in h.get_attribute('innerHTML'):
            #         a = h
            #         print(a.get_attribute('outerHTML'))
            #         break
            a = o[1]
            # print(a.get_attribute('outerHTML'))
            a.click()

            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[contains(text(), "共通の送料込みライン")]')))
            # o = driver.find_element_by_xpath('//button[@type="submit"]')
            o = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//button[contains(text(),"上記を遵守していることを確認の上")]')))
            o.click()

            # we should be in... 
            # check if fucking pop-up appears :
            # div class="eccMessagePopTitle"
        except NoSuchElementException:
            print('pas de R-Login管理')
            return False
    except NoSuchElementException:
        print('Erreur de connexion')
        return False

    return True

def get_rak_orders():

    try:

        # check if there are orders
        b = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, '//div/h2[contains(text(),"注文確認待ち")]')))
       
        nb = b.find_elements_by_xpath('../p/strong')[0].text
        print(nb)

        if (nb == "0"):
            print("pas de commandes")
            return

        a = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "order-rb/order-list")]')))
        a.click()

        # get list of orders
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div/span[contains(text(), "受注番号")]')))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "order-rb/individual-order-detail-sc")]')))
        o = driver.find_elements_by_xpath('//a[contains(@href, "order-rb/individual-order-detail-sc")]')
        print('\n we have : ', len(o), ' orders')

        i = 0
        for add in o:
            s = get_rak_order_address(add)
            adresses.append(s)

    except NoSuchElementException:
        print('error')

    saveAddresses()

    return

def get_rak_order_address(add) -> str :

    add.click()

    WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
    new_win = driver.window_handles
    print(len(new_win))
    print(new_win[0],new_win[1])
    # https://stackoverflow.com/questions/53690243/selenium-switch-tabs
    driver.switch_to.window(new_win[1])
    # WebDriverWait(driver, 20).until(EC.title_contains("Amazon"))

    s = ''    
    try:

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[contains(@class,"rms-content-order-details-contact-info")]'))) 
        o = driver.find_elements_by_xpath('//div[contains(@class,"rms-content-order-details-contact-info")]')
        print(len(o))
        
        n = '//div[contains(@class,"rms-content-order-details-summary-table-row-wrapper") and contains(.//span,"お届け日時")]'
        # n = '//span[contains(text(),"お届け日時")]/ancestor::div[contains(@class, "rms-content-order-details-summary-table-row-wrapper")]'

        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
            jikan = driver.find_element_by_xpath(n)
            # print(jikan.get_attribute('innerHTML'))
            # print(jikan.get_attribute('outerHTML'))
            d = jikan.find_elements_by_xpath('.//div/p')
            j = d[0].text
            print('時間',j)

        except:
            pass

        for d in o:
            if '送付先情報' in d.get_attribute('innerHTML'):
                print(d.get_attribute('innerHTML'))
                name = d.find_element_by_xpath('.//div/span[@class="fullname"]').text
               
                if ( ' ' in name ):
                    n = name.split(' ')
                    nom = n[0]
                    prenom = n[1]  
                elif ( '　' in name ):
                    n = name.split('　')
                    nom = n[0]
                    prenom = n[1]
                    name = name.replace('　', ' ')
                else:
                    nom = name[0:2]
                    prenom = name[2:len(name)]

                s += name + ',' + nom + "," + prenom + "," 

                phone = d.find_element_by_xpath('.//div/span[@class="phone"]').text

                if (phone.find('-') != -1 ):
                    phone = phone.replace('-','')

                s += phone + ','
                
                address = d.find_element_by_xpath('.//div/span[@class="address"]').text

                zip_code = address[1:9]
                zip_code = zip_code.replace('-','')

                jusho = address[10:len(address)]
                # trouve les 1er numeros
                m = re.search(r"\d", jusho)
                i = m.start()
                jusho1 = jusho[0:i]
                j = jusho1.find("県")
                if (j != -1):
                    jusho0 = jusho1[0:j+1]
                    jusho1 = jusho1[j+1:len(jusho1)]
                else:    
                    # 大阪府　東京都　京都府
                    jusho0 = jusho1[0:3]
                    jusho1 = jusho1[3:len(jusho1)]
                    
                jusho2 = jusho[i:len(jusho)]
               
                s += zip_code + ',' + jusho0 + ',' + jusho1 + ',' + jusho2 + ','
                
                furigana = d.find_element_by_xpath('.//div/span[@class="furigana"]').text
                s +=  ',' + furigana
                break

    except NoSuchElementException:
        s = 'erreur get_rak_order_address'
        print(s)

    driver.close()   
    driver.switch_to.window(new_win[0])

    return s

def saveAddresses():
    global adresses
    if shohin_kanri :
        f = open(r'.\amz\rakuten_products.csv','w',encoding='utf-8')
    else:
        f = open(r'.\amz\orders_list_YMT.txt','w',encoding='utf-8')

    for s in adresses:
        f.write("%s\n" % s)
    f.close()
    return

def rak_update_products():
    # get list of products
    getProducts()

    go_to_product_page()

    products_num_page()

    list_products = get_list_products_in_page()

    for prod in produits:
        product = prod.split(',')
        # print(product[0], product[7])
        if product[7] == '1':
            product_name =  product[0]
            print("edit : ", product_name)
            e = list_products[product_name]
            edit_product(product)
        # a = driver.find_element_by_xpath('//a[@id="button_regist"]')
        # a.click()
    return

def edit_product(product):

    url = 'https://item.rms.rakuten.co.jp/rms/mall/rsf/item/vc?__event=RI03_001_002&shop_bid=375953&mng_number=' + product[0]
    try:
        driver.get(url)

        # start editing page
        # s = 'shohin_kanri,title,catch_copy,price,image,nombre,zaiko'

        # 在庫

        # price
        n = '//input[@name="price"]'
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,n)))
        o = driver.find_element_by_xpath(n)
        # print(o.get_attribute('innerHTML'))
        # print(o.get_attribute('outerHTML'))
        # print(o.get_attribute("value"))
        
        price = product[3]
        o.clear()
        o.send_keys(price)
        print(o.get_attribute("value"))

        # 
        catalog_caption = product[8]


        # finally submit changes
        n = '//input[@id="submitButton"][contains(@value,"商品情報を変更する")]'
        o = driver.find_element_by_xpath(n)
        o.click()
    except:
        print('erreur')

    return

def get_list_products_in_page() -> {}:
    # liste des produits 
    n = '//div[@class = "fixed-table-container fixed-main-table-padding"]'
    WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
    o = driver.find_element_by_xpath(n)

    n = './/table[@id="tableBootstrap"]'
    tab = o.find_element_by_xpath(n)

    n = './/tbody/tr'
    e = tab.find_elements_by_xpath(n)
    print('nbre de produits ', len(e))

    list_products = {}

    for p in e:
        n = './/td'
        try:
            q = p.find_elements_by_xpath(n)
            print(q[5].text)
            shohinKanri = q[5].text
            list_products[shohinKanri] = e
        except:
            print("erreur dans p")

    return list_products

def products_num_page():
    n = '//section[@class="itemlist-container"]'
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
        section = driver.find_element_by_xpath(n)
        print("itemlist-container")            
        # nombre de pages
        n = './/ul[@class="pagination"]/li'
        page = section.find_elements_by_xpath(n)
        print('nbre de pages ', len(page))
        # poi = page[2]
        # qwe = poi.find_element_by_xpath('.//a')
        for poi in page:
            print(poi.get_attribute('innerHTML'))
            print(poi.get_attribute('outerHTML'))
            print(poi.text)
    except:
        print('pb2')
        return
    return

def go_to_product_page():
    try:
        driver.get('https://item.rms.rakuten.co.jp/rms/mall/rsf/item/vc?__event=RI00_001_101')
        
        t = '商品個別編集(一覧表示)'
        # n = '//a[contains(text(),"' + t + '")]'
        n = '//a/font[contains(text(),"商品個別編集(一覧表示)")]'
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n))) 
            print("page des produits")
            o = driver.find_element_by_xpath(n)
            o.click()
        except:
            print("pas de page de produits")
            pass
    except:
        print('erreur go_to_product_page')
    return

def getProducts():
    global produits
    f = open(r'.\amz\rakuten_products.csv', 'r',encoding='utf-8')
    produits = f.readlines()
    for i in range(0,len(produits)):
        prod = produits[i]
        # print(len(prod))
        # print(prod)
        if prod[len(prod)-1] == '\n':
            produits[i] = prod[:-1]
    f.close()
    return

def getProducts_from_csv():
    global produits
    f = open(r'.\amz\rakuten_products.csv', 'r',encoding='utf-8')
    produits = f.readlines()
    for i in range(0,len(produits)):
        prod = produits[i]
        # print(len(prod))
        # print(prod)
        if prod[len(prod)-1] == '\n':
            produits[i] = prod[:-1]
    f.close()
    return

def download_prod():
    try:
        driver.get('https://item.rms.rakuten.co.jp/rms/mall/rsf/item/vc?__event=RI00_001_101')
        
        t = '商品個別編集(一覧表示)'
        # n = '//a[contains(text(),"' + t + '")]'
        n = '//a/font[contains(text(),"商品個別編集(一覧表示)")]'
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
            o = driver.find_element_by_xpath(n)
            o.click()

            n = '//h1[contains(text(),"商品個別編集(一覧表示)")]'
            try:
                WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
                print("page des produits")
            except:
                print('pb1')
                return

            n = '//section[@class="itemlist-container"]'
            try:
                WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
                section = driver.find_element_by_xpath(n)
                print("itemlist-container")            
                # nombre de pages
                n = './/ul[@class="pagination"]/li'
                page = section.find_elements_by_xpath(n)
                print('nbre de pages ', len(page))
                # poi = page[2]
                # qwe = poi.find_element_by_xpath('.//a')
                for poi in page:
                    print(poi.get_attribute('innerHTML'))
                    print(poi.get_attribute('outerHTML'))
                    print(poi.text)
            except:
                print('pb2')
                return

            # liste des produits 
            n = '//div[@class = "fixed-table-container fixed-main-table-padding"]'
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
            o = driver.find_element_by_xpath(n)

            n = './/table[@id="tableBootstrap"]'
            tab = o.find_element_by_xpath(n)

            n = './/tbody/tr'
            e = tab.find_elements_by_xpath(n)
            print('nbre de produits ', len(e))
            
            s = 'shohin_kanri,title,catch_copy,price,image,nombre,zaiko'
            adresses.append(s)

            for p in e:

                s = ''
                n = './/a[contains(text(),"変更")]'
                n = './/td'
                try:
                    # WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
                    # q = p.find_element_by_xpath(n)
                    # print(q.get_attribute('innerHTML'))
                    # print(q.get_attribute('outerHTML'))
                    q = p.find_elements_by_xpath(n)

                    src = q[2].find_element_by_xpath('.//img').get_attribute("src")
                    img = src.split('?')
                    print(img[0].rsplit('/', 1)[-1])
                    image = img[0].rsplit('/', 1)[-1]

                    print(q[5].text)
                    shohinKanri = q[5].text

                    t = q[3].find_elements_by_xpath('.//div')
                    title = t[0].get_attribute("title")
                    catch_copy = t[1].text

                    price = q[4].find_element_by_xpath('.//input').get_attribute("value")
                    price = price.replace(',','')

                    nombre = q[6].find_element_by_xpath('.//input').get_attribute("value")
                    zaiko = q[8].text
                    
                    s = shohinKanri + ',' + title + ',' + catch_copy + ',' + price + ',' + image + ',' + nombre + ',' + zaiko
                    adresses.append(s)

                except:
                    print("erreur dans p")

            saveAddresses()
            
        except:
            print("erreur totale")
            pass

    except:
        print('erreur')
    return

def download_report(reportYear):

    try:
        driver.get('https://csvdl-rp.rms.rakuten.co.jp/rms/mall/csvdl/CD02_01_001?dataType=opp_order#result')

        n = '//label[contains(text(),"注文確定日")]'
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
            o = driver.find_element_by_xpath(n)
            o.click()

            # for m in range(1,13):
            #     get_monthly_data(reportYear,m)

            # consolidation des fichiers
            outFile = dirPath + 'rak-' + reportYear + '-total.csv'
            f = open(outFile,'w',encoding='shift-jis')

            for m in range(1,13):
                fromDate =  reportYear + '-' + str(m).zfill(2) + '-01'
                days = monthrange(int(reportYear),int(m))
                toDate = reportYear + '-' + str(m).zfill(2) +  '-' + str(days[1]).zfill(2)
                fileName = dirPath + 'rak-' + fromDate + '-' + toDate + '.csv'
                g = open(fileName, 'r',encoding='shift-jis')
                contenu = g.readlines()
                g.close()
                for s in contenu:
                    f.write("%s\n" % s)

        except:
            print('erreur')
    except:
        print('erreur')
    return

dirPath = 'C:\\Users\\blgl\\Downloads\\'
from calendar import monthrange
from datetime import datetime
import os
def get_monthly_data(reportYear, month):

    n = '//select[@name="fromYmd"]'
    select = Select(driver.find_element_by_name('fromYmd'))
    fromDate =  reportYear + '-' + str(month).zfill(2) + '-01'
    select.select_by_value(fromDate)

    select = Select(driver.find_element_by_name('toYmd'))
    days = monthrange(int(reportYear),int(month))
    toDate = reportYear + '-' + str(month).zfill(2) +  '-' + str(days[1]).zfill(2)
    select.select_by_value(toDate)

    select = Select(driver.find_element_by_name('templateId'))    
    select.select_by_value('-1')

    n = '//input[@id="dataCreateBtn"]'
    o = driver.find_element_by_xpath(n)
    o.click()

    try:
        n = '//input[@id="downloadBtn"]'
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH,n))) 

        user = driver.find_element_by_xpath('//input[@id="user"]')
        user.send_keys('loys')   
        pwd = driver.find_element_by_xpath('//input[@id="passwd"]')
        pwd.send_keys('Yelpb94q')   

        o = driver.find_element_by_xpath(n)
        o.click()

        # download done, do some clean up
        fileName = datetime.today().strftime('%Y-%m-%d') + '.csv'
        # dirPath = 'E:\\Google drive - ltd-japon\\LTD-Japon\\Kaisha\\業績\\2020\\'
        oldName = dirPath + fileName.replace('-', '')
        newName = dirPath + 'rak-' + fromDate + '-' + toDate + '.csv'
        # move file to 
        os.rename(oldName,newName)

    except:
        print('erreur downloadBtn')
        return

    return


mail_subject = '【楽天市場・特別 感謝クーポン】'
mail_subject = '【楽天市場・フランス産（冷凍）フォアグラ 割引 キャンペーン！】'
# set text 
# mail_texte = ' この度はグルメ・ジャポンでのご注文、誠にありがとうございます。<br>\
#     <p>お客様へ、お礼の割引クーポンを配布中ですので、<br>\
#         是非ご確認下さい：<br> \
#         <a href="https://coupon.rakuten.co.jp/getCoupon?getkey=TTNaWS1YMUc3LVY2TVktVDVEVQ--&rt=" target="_blank"> ＊＊＊　獲得URL　＊＊＊　<br>  \
#        クーポンコード：X1G7-M3ZY-V6MY-T5DU <br>\
#     どうぞよろしくお願い致します。</p>' 
# mail_texte = ' この度はグルメ・ジャポンでのご注文、誠にありがとうございます。\n\
#     お客様へ、お礼の割引クーポンを配布中ですので、\n\
#         是非ご確認下さい：\n \
#         獲得URL：https://coupon.rakuten.co.jp/getCoupon?getkey=TTNaWS1YMUc3LVY2TVktVDVEVQ--&rt= \n \
#     クーポンコード：X1G7-M3ZY-V6MY-T5DU \n \
#     どうぞよろしくお願い致します。'
mail_texte = ' 今年グルメ・ジャポンでフォアグラをご注文のお客様へ、\n\
        在庫調整のため、特別の割引クーポンを配布致します！\n\
            商品：\n\
                https://item.rakuten.co.jp/gourmets-japon/espn-escalope-foie-gras-4pc \n\
            (生・冷凍) フランス産 フォアグラ ド カナール （鴨）エスカロップ （スライス4個）１５０ｇ 以上（4０〜6０ｇｘ４個）「IGP」 Maison Espinet </a>\n\
        通常価格（１パックｘ４個）：２９００円\n \
        キャンペーン価格： ２パックｘ８個 ４０００円 【送料無料】（１８００円ＯＦＦ！) \n \
   有効期間　：　2021/11/12 14:00 ～ 2021/11/30 23:59\n \
   利用条件　：　先着100個まで 2個以上の購入で使える PC・スマホでの購入 併用NG \n \
   説明　：　在庫切れまで。\n \
    お早めにね！ \n \
        クーポン獲得URL：  	https://coupon.rakuten.co.jp/getCoupon?getkey=MlhXMS1HQURFLUpRVzktSllKVQ--&rt=\n \
    クーポンコード：GADE-2XW1-JQW9-JYJU　\n \
    どうぞよろしくお願い致します。'

def mailing_list():
    try:
        driver.get('https://cs.rms.rakuten.co.jp/')
        
        n = '//button[@class="rms-btn btn-blue btn-width-md" and contains(text(),"検索")]'
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n))) 
            print("page des clients")
            o = driver.find_element_by_xpath(n)
            o.click()

            clients = []
            # 1ere paage
            # n = '//div[@class="rms-pagination"]'
            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="rms-pagination"]'))) 
            # n = '//table[@class="rms-table"]/tbody/tr'
            # tr = driver.find_elements_by_xpath(n)
            # print(len(tr))
            # clients.append(tr)

            # select product
            product = 'espn-escalope-foie-gras-4pc'
            product = 'espn-escalope-foie-gras-2pc'

            n = '//div[@class="rms-col-xs-21"]'
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
            n = '//div[@class="rms-col-xs-21"]/div/label/input'
            # WebDriverWait(q, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
            o = driver.find_elements_by_xpath(n)
            for p in o:
                v = p.get_attribute('value')
                if v == 'mng_number':
                    p.click()

            n = '//div[@class="rms-input-control"]/input'
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
            o = driver.find_element_by_xpath(n)
            o.clear()
            o.send_keys(product)

            n = '//button[@class="rms-btn btn-blue btn-width-md"]'
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
            o = driver.find_element_by_xpath(n)
            o.click()

            # nbre de commandes
            n = '//div[@class="rms-content-fixed"]/div/div'
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
            o = driver.find_elements_by_xpath(n)
            nbre = o[3].text
            nbre = int(nbre.split('件')[1][-1])
            print("nbre ", nbre)

            if nbre > 10:
                # nombre de pages
                n = '//div[@class="rms-pagination"]'
                WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
                
                n = '//div[@class="rms-pagination"]/ul/li'
                t = driver.find_elements_by_xpath(n)
                pages = int(t[-2].text)
            else:
                pages = 1
            print("nombre de pages : ", pages)

            # charger les autres pages
            # for p in range(1,4):

            #     # n = '//div[@class="rms-pagination"]/ul/li/a[@href="#pagination' + str(p) + '"]'
            #     n = '//div[@class="rms-pagination"]/ul/li/a[@href="#next"]'
            #     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n))) 
            #     o = driver.find_element_by_xpath(n)
            #     o.click()
            #     print('p', p)

            for p in range(0,pages):

                n = '//table[@class="rms-table"]/tbody/tr'
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="rms-pagination"]'))) 
                tr = driver.find_elements_by_xpath(n)
                print(len(tr))
                #     clients.append(tr)
                # print(len(clients))

                # for i in range(4,len(clients)-1):
                #     tr = clients[i]
                for a in tr:
                    n = './/span[@data-ratid="link-search_order"]/a'
                    # n = './/*/a'
                    o = a.find_elements_by_xpath(n)
                    client_id = o[0].get_attribute('href')
                    print(client_id)
                    o[0].click()

                    WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
                    new_win = driver.window_handles
                    driver.switch_to.window(new_win[1])

                    n = '//a[@class="email"]'
                    try:
                        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
                        o = driver.find_element_by_xpath(n)
                        o.click()

                        WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(3))
                        new_win = driver.window_handles
                        driver.switch_to.window(new_win[2])

                        # n = '//a[contains(text(),"注文お礼メール")]'
                        n = '//input[@class="submitControlButton"]'
                        try:
                            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
                            o = driver.find_element_by_xpath(n)
                            o.click()

                            n = '//input[@id="subject"]'
                            o = driver.find_element_by_xpath(n)
                            o.clear()
                            o.send_keys(mail_subject)

                            n = '//textarea[@id="body1"]'
                            o = driver.find_element_by_xpath(n)
                            o.clear()

                            o.send_keys(mail_texte)

                            n = '//input[@value="テスト送信"]'
                            n = '//input[@value=" 本送信 "]'
                            o = driver.find_element_by_xpath(n)
                            o.click()

                        except:
                            print('erreur send mail')

                        driver.close()
                        driver.switch_to.window(new_win[1])

                    except:
                        print('erreur send mail')

                    driver.close()   
                    driver.switch_to.window(new_win[0])
                
                if p < pages-1 :
                    # page suivante
                    n = '//div[@class="rms-pagination"]/ul/li/a[@href="#next"]'
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n))) 
                    o = driver.find_element_by_xpath(n)
                    o.click()
                else:
                    break

        except:
            print("pas de page de produits")
            pass
    except:
        print('erreur go_to_product_page')
    return

def envoi_mail():
    n = '//a[@class="email"]'
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
        o = driver.find_element_by_xpath(n)
        o.click()

        WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(3))
        new_win = driver.window_handles
        driver.switch_to.window(new_win[2])

        # n = '//a[contains(text(),"注文お礼メール")]'
        n = '//input[@class="submitControlButton"]'
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
            o = driver.find_element_by_xpath(n)
            o.click()

            n = '//input[@id="subject"]'
            o = driver.find_element_by_xpath(n)
            o.clear()
            o.send_keys('【楽天市場・特別 感謝クーポン】')

            n = '//textarea[@id="body1"]'
            o = driver.find_element_by_xpath(n)
            o.clear()

            # set text 
            # texte = ' この度はグルメ・ジャポンでのご注文、誠にありがとうございます。<br>\
            #     <p>お客様へ、お礼の割引クーポンを配布中ですので、<br>\
            #         是非ご確認下さい：<br> \
            #         <a href="https://coupon.rakuten.co.jp/getCoupon?getkey=TTNaWS1YMUc3LVY2TVktVDVEVQ--&rt=" target="_blank"> ＊＊＊　獲得URL　＊＊＊　<br>  \
            #        クーポンコード：X1G7-M3ZY-V6MY-T5DU <br>\
            #     どうぞよろしくお願い致します。</p>' 
            texte = ' この度はグルメ・ジャポンでのご注文、誠にありがとうございます。\n\
                お客様へ、お礼の割引クーポンを配布中ですので、\n\
                    是非ご確認下さい：\n \
                    獲得URL：https://coupon.rakuten.co.jp/getCoupon?getkey=TTNaWS1YMUc3LVY2TVktVDVEVQ--&rt= \n \
                クーポンコード：X1G7-M3ZY-V6MY-T5DU \n \
                どうぞよろしくお願い致します。'
            texte = ''
            o.send_keys(texte)

            n = '//input[@value="1．テスト送信"]'
            # n = '//input[@value="2．本送信"]'
            o = driver.find_element_by_xpath(n)
            o.click()

        except:
            print('erreur send mail')

        driver.close()
        driver.switch_to.window(new_win[1])

    except:
        print('erreur send mail')

    return

shohin_kanri = False
downloadReport = False
updateProducts = False
mailingList = True

if __name__ == '__main__':
    if ( connect_to_rms() ):

        if ( shohin_kanri ):
            download_prod()
        elif (downloadReport):
            reportYear = '2021'
            download_report(reportYear)
        elif (mailingList):
            reportYear = '2021'
            mailing_list()
        elif (updateProducts):
            rak_update_products()
