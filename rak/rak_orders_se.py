import sys
sys.path.append(".")
from orderlib import file_utils
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
    # driver = webdriver.Firefox(firefox_profile=fp)  C:\Loys\Google drive - ltd-japon\Dev\web\Gekco
    driver = webdriver.Firefox(executable_path="C:\\Loys\\Google drive - ltd-japon\\Dev\\web\\Gekco\\geckodriver.exe")
else:
    options = webdriver.ChromeOptions() 
    options.add_argument('user-data-dir=C:\\Users\\Loys\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #Path to your chrome profile
    driver = webdriver.Chrome(executable_path="E:\\Google drive - ltd-japon\\Dev\\web\\Chrome\\chromedriver.exe", chrome_options=options)

adresses = []
produits = []
user_glogin = file_utils.user_glogin
mdp = file_utils.mdp
user_yahoo = file_utils.user_yahoo
mdp2 = file_utils.mdp2

regions = ['三重県',	'京都府',	'兵庫県',	'千葉県',	'和歌山県',	'埼玉県',	'大阪府',	'奈良県',\
    	'宮城県',	'富山県',	'山形県',	'山梨県',	'岐阜県',	'愛知県',	'新潟県',	'東京都',	'栃木県',	'滋賀県',\
    	'石川県',	'神奈川県',	'福井県',	'福島県',	'群馬県',	'茨城県',	'長野県',	'静岡県',]

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
        o = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//button[@name="submit"]')))
        # o = driver.find_element_by_xpath('//button[@name="submit"]')
        # o.click()
        driver.execute_script("arguments[0].click();", o)

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

# first i_max addresses 
i_min = 1
i_max = 1000

def get_rak_orders():

    try:

        # check if there are orders
        b = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, '//div/h2[contains(text(),"注文確認待ち")]')))
       
        # nb = b.find_elements_by_xpath('../p/strong')[0].text
        # print(nb)

        # if (nb == "0"):
        #     print("pas de commandes")
        #     return

        a = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "order-rb/order-list")]')))
        a.click()

        # select data-order-list-filter-tab="発送待ち"
        a = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//li[@data-order-list-filter-tab="発送待ち"]')))
        o = a.find_element_by_xpath('.//h5/span')
        print(o.text)
        a.click()

        # name="displayAmount"
        n = '//select[@name="displayAmount"]'
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n)))
        select = Select(driver.find_element_by_name('displayAmount'))
        select.select_by_value('500')


        # get list of orders
        # class="rms-content-order-list-item-order-nr"
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div/span[contains(text(), "受注番号")]')))
        n = '//table[@id="orderListTable"]'
        t = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n)))
        # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "order-rb/individual-order-detail-sc")]')))
        # o = driver.find_elements_by_xpath('//a[contains(@href, "order-rb/individual-order-detail-sc")]')
        n = './/tbody[@class="rms-content-order-list-item rms-list-item rms-item-order-inprogress"]'
        n = '//tbody[contains(@class,"rms-content-order-list-item")]'
        n = './/a[@class="rms-content-order-list-item-order-nr"]'
        WebDriverWait(t, 20).until(EC.visibility_of_element_located((By.XPATH,n)))
        o = t.find_elements_by_xpath(n)
        print('\n we have : ', len(o), ' orders')
        # driver.execute_script("arguments[0].scrollIntoView(true);", e)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # add = driver.find_elements_by_xpath(n)
        # url.replace('https:\/\/','')
        # url = 'https://order-rp.rms.rakuten.co.jp' + url

        url = []
        obj = []
        i = 0
        for k in range(0,len(o)):
            # bizarre, l'objet n'est pas accessible 
            url.append(o[k].get_attribute('href'))
        for k in range(0,len(o)):
            driver.execute_script("window.open('');")
            WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
            new_win = driver.window_handles
            driver.switch_to.window(new_win[1])
            # obj[k].click()
            driver.get(url[k])
            s = get_rak_order_address()
            driver.close()
            driver.switch_to.window(new_win[0])
            adresses.append(s)
            i += 1

        # i = 1
        # j = 0
        # for k in range(0,len(o)):
        #     if i_min <= i <= i_max:
        #           j += 1
        #     i += 1
            
        print('il y a ', i, ' adresses')

    except NoSuchElementException:
        print('error')

    if not update_Yamato:
        saveAddresses()

    return

def get_rak_order_address() -> str :

    # get destination address
    s = ''
    try:

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[contains(@class,"rms-content-order-details-contact-info")]'))) 
        o = driver.find_elements_by_xpath('//div[contains(@class,"rms-content-order-details-contact-info")]')
        # print(len(o))
        
        n = '//div[contains(@class,"rms-content-order-details-summary-table-row-wrapper") and contains(.//span,"お届け日時")]'
        # n = '//span[contains(text(),"お届け日時")]/ancestor::div[contains(@class, "rms-content-order-details-summary-table-row-wrapper")]'

        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n))) 
            jikan = driver.find_element_by_xpath(n)
            # print(jikan.get_attribute('innerHTML'))
            # print(jikan.get_attribute('outerHTML'))
            d = jikan.find_elements_by_xpath('.//div/p')
            jikan = d[1].text.replace('時間指定：','')
            # print('時間',jikan)

        except:
            pass

        for d in o:
            if '送付先情報' in d.get_attribute('innerHTML'):
                # print(d.get_attribute('innerHTML'))
                name = d.find_element_by_xpath('.//div/span[@class="fullname"]').text

                if update_Yamato:
                    if '伊熊 みか子' in name:
                        break
                    n = '//input[@name="parcelNumber"]'
                    print("update ", name)
                    parcel_number = d.find_element_by_xpath(n)
                    parcel_number.clear()
                    # break
                    numero_YMT = '7641-8532-'
                    parcel_number.send_keys(numero_YMT)
                    n = '//input[@name="shipmentDate"]'
                    s = d.find_element_by_xpath(n)
                    s.clear()
                    s.send_keys('2021-06-21')
                    select = Select(driver.find_element_by_name('deliveryClass'))
                    deliveryClass = '1'
                    select.select_by_value(deliveryClass)
                    n = '//input[@name="deliveryDate"]'
                    s = d.find_element_by_xpath(n)
                    s.clear()
                    # get region ?
                    address = d.find_element_by_xpath('.//div/span[@class="address"]').text
                    ken = get_jusho(address)
                    if ken in regions:
                        dateToReceive = '20210622'
                    else:
                        dateToReceive = '20210623'
                    s.send_keys(dateToReceive)

                    # n = '//button[@id="btnSave"]'
                    # o = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,n)))
                    # o.click()

                else:
                                   
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
                    chiffres = ['０','１','２','３','４','５','６','７','８','９','ー','丁目','-']
                    # re.search(r'^chiffres', jusho2).start()
                    iNum = 0
                    for i, c in enumerate(jusho2):
                        if c.isnumeric():
                            continue
                        if c not in chiffres:
                            iNum = i
                            break
                    
                    if iNum != 0:
                        s += zip_code + ',' + jusho0 + ',' + jusho1 + ',' + jusho2[0:iNum] + ',' + jusho2[iNum:] 
                    else:
                        s += zip_code + ',' + jusho0 + ',' + jusho1 + ',' + jusho2 + ',' 
                    
                    furigana = d.find_element_by_xpath('.//div/span[@class="furigana"]').text
                    s +=  ',' + furigana + ',' + jikan
                break

    except NoSuchElementException:
        s = 'erreur get_rak_order_address'
        print(s)


    if not update_Yamato:
        # get order details
        # class="rms-content-order-details-block-destination-overview-table-title"
        try:
            n = '//div[@class="rms-content-order-details-block-destination-overview-table"]'
            o = driver.find_elements_by_xpath(n)
            if len(o) != 1:
                print('pb')
            m = './/div/table/tbody/tr'
            p = o[0].find_elements_by_xpath(m)
            i = 0
            for e in p:
                if e.get_attribute('class'):
                    print('trouvé ',i,'commandes')
                    break
                f = e.find_elements_by_xpath('.//td')
                g = f[0].find_element_by_xpath('.//div/a')
                produit = g.get_attribute('href').split('/')
                prod = produit[-2]
                print("Commande : ", prod )
                if prod in file_utils.charcuteries_fine_conserves:
                    package = 'YMT_compact'
                elif prod in file_utils.surgeles:
                    package = 'YMT_frozen'
                elif prod in file_utils.YMT_60:
                    package = 'YMT_60'
                else:               
                    print('pb package')
                i += 1
                prix = f[5].find_element_by_xpath('.//div/div/div').text
                prix = prix.replace(',','')
                prix = prix.replace('円','')
                print(prix)
                nbre = f[7].find_element_by_xpath('.//div/div').text
                print(nbre)

                s +=  ',' + prod + ',' + package + ',' + prix + ',' + nbre + ','

        except NoSuchElementException:
            s = 'erreur get_rak_order_address'
            print(s)

    # driver.close()   
    # driver.switch_to.window(new_win[0])

    return s

def get_jusho(address):
    
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

    return jusho0

def saveAddresses():
    global adresses
    if shohin_kanri :
        f = open(r'.\rak\rakuten_products.csv','w',encoding='utf-8')
    else:
        f = open(r'.\orders_list_YMT.txt','w',encoding='utf-8')

    for s in adresses:
        f.write("%s\n" % s)
    f.close()
    return

def rak_new_products():
    # get list of products
    for prod in produits:
        product = prod.split(',')
        print(product)
        # a = driver.find_element_by_xpath('//a[@id="button_regist"]')
        # a.click()
    return

def getProducts():
    global produits
    f = open(r'..\rak\rak_produits.txt', 'r',encoding='utf-8')
    produits = f.readlines()
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

            for m in range(1,13):
                get_monthly_data(reportYear,m)

        except:
            print('erreur')
    except:
        print('erreur')
    return

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
        dirPath = 'C:\\Users\\Loys\\Downloads\\'
        oldName = dirPath + fileName.replace('-', '')
        newName = dirPath + 'rak-' + fromDate + '-' + toDate + '.csv'
        # move file to 
        os.rename(oldName,newName)

    except:
        print('erreur downloadBtn')
        return

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

    return

shohin_kanri = False
downloadReport = False
update_Yamato = False

if __name__ == '__main__':
    if ( connect_to_rms() ):

        if ( shohin_kanri ):
            download_prod()
        elif (downloadReport):
            reportYear = '2021'
            download_report(reportYear)
        else:
            # file_name = './orders_list_YMT-ref-51-99.csv'
            # address = file_utils.getAddresses(file_name)
            get_rak_orders()
            # rak_new_products()
