from selenium import webdriver
# from selenium.webdriver.chrome.options import Options as SeleniumOptions
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime as dt
from selenium.webdriver.remote.webelement import WebElement
import re

import sys
sys.path.append(".")
from orderlib import file_utils

firefox = False

if firefox: 
    # fp = webdriver.FirefoxProfile('C:/Users/Loys/AppData/Roaming/Mozilla/Firefox/Profiles/ax8azgih.default')
    # driver = webdriver.Firefox(firefox_profile=fp)
    driver = webdriver.Firefox(executable_path="E:\\Google drive - ltd-japon\\Dev\\web\\Gekco\\geckodriver.exe")
else:
    options = webdriver.ChromeOptions() 
    # options.add_argument('user-data-dir=C:\\Users\\Loys\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #Path to your chrome profile
    options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1")
    driver = webdriver.Chrome(executable_path="C:\\Loys\\Google drive - ltd-japon\\Dev\\web\\Chrome\\chromedriver.exe", chrome_options=options)


kuroneko_id = 'BK4XU755'
kuroneko_id = 'RAV7B3G9'
kuroneko_pwd = 'xxxxx'

regions = ['三重県',	'京都府',	'兵庫県',	'千葉県',	'和歌山県',	'埼玉県',	'大阪府',	'奈良県',\
    	'宮城県',	'富山県',	'山形県',	'山梨県',	'岐阜県',	'愛知県',	'新潟県',	'東京都',	'栃木県',	'滋賀県',\
    	'石川県',	'神奈川県',	'福井県',	'福島県',	'群馬県',	'茨城県',	'長野県',	'静岡県',]

def connectToYMT():

    URL = ' https://sp-send.kuronekoyamato.co.jp/smpTaqWeb/Viwb1010Action_doInit.action'
    driver.get(URL)
    try:
        o = driver.find_element_by_xpath('//*')
        # print(o.get_attribute('outerHTML'))
        # print(o.get_attribute('innerHTML'))
    except NoSuchElementException:
        print('error')
        return False

    # seems ok
    a = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//a[@id="portalEntrance"]')))
    a.click()

    try:
        # enter mot de passe         
        try:
            k_id = driver.find_element_by_xpath('//input[@id="kuroneko_id"]')
        except:
            k_id = driver.find_element_by_xpath('//input[@id="login-form-id"]')
        k_id.clear()
        k_id.send_keys(kuroneko_id)

        # enter mot de passe        
        pwd = driver.find_element_by_xpath('//input[@type="password"]')
        pwd.send_keys(kuroneko_pwd)

        try:
            o = driver.find_element_by_xpath('//button[@type="submit"]')
        except:
            o = driver.find_element_by_xpath('//button[@id="login-form-submit"]')
        o.click()
    except NoSuchElementException:
        print('erreur connexion YMT')
        return False

    return True

def update_adresses():

    try:
        # a = driver.find_element_by_xpath('//a/p[contains(text(), "アドレス帳")]')
        # a.click()
        # get list of addresses
        for add in address:
            adresse = add.split(',')

            YMT_category = adresse[-4]
            # print('compact')
            if YMT_category == 'YMT_compact':
                n = '//a/span[contains(text(),"通常の荷物を送る")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                a = driver.find_element_by_xpath(n)
                a.click()
            elif YMT_category == 'YMT_frozen':
                n = '//a/span[contains(text(),"冷凍の荷物を送る")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                a = driver.find_element_by_xpath(n)
                a.click()

            elif YMT_category == 'YMT_60':
                n = '//a/span[contains(text(),"通常の荷物を送る")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                a = driver.find_element_by_xpath(n)
                a.click()
            
            n = '//a/span[contains(text(),"発払いで荷物を送る")]'
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
            a = driver.find_element_by_xpath(n)
            a.click()

            if YMT_category == 'YMT_compact':

                n = '//div[@class="btn-box"]/p/a'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                a = driver.find_element_by_xpath(n)
                a.click()

                n = '//div[@class="btn-type-size "]/label/span[contains(text(),"コンパクト")]'
                n = '//div[@class="btn-type-size "]/label/span[@class="size-btn size-btn-compact js-compactBtn"]'
                n = '//div[@class="btn-type-size "]/label/span[@class="size-btn size-btn-compact js-compactBtn size-btn-initial"]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                a = driver.find_element_by_xpath(n)
                a.click()

                n = '//div[@id="modal"]'
                n = '//div[@class="btn-type-02 modal-close"]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                p = driver.find_elements_by_xpath(n)
                if len(p) > 1:
                    print('pb')

                n = './/a[contains(text(),"OK")]'
                # WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                a = p[0].find_element_by_xpath(n)
                a.click()

            elif YMT_category == 'YMT_60':

                n = '//div[@class="btn-type-size btn-type-size-single"]/label/span[contains(text(),"S")]'
                n = '//a[@id="one"]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                a = driver.find_element_by_xpath(n)
                a.click()

                n = '//div[@class="btn-type-size "]/label/span[contains(text(),"S")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                a = driver.find_element_by_xpath(n)
                a.click()                
                
                # n = '//a/span/p[contains(text(),"それ以外の荷物")]'
                # WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                # a = driver.find_element_by_xpath(n)
                # a.click()
            
            elif YMT_category == 'YMT_frozen':
                # less than 80 size
                # n = '//a/span/p[contains(text(),"Ｓサイズの荷物")]'
                n = '//div[@class="btn-type-size btn-type-size-single"]/label/span[contains(text(),"S")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                a = driver.find_element_by_xpath(n)
                a.click()

            # same for all ?
            try:
                # win = driver.window_handles
                # print(len(win))

                n = '//label/input[contains(@class,"form-text-01")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                e = driver.find_element_by_xpath(n)
                e.clear()
                e.send_keys('食品')

                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                n = '//form[@id="form"]/div[@class="content-inner"]/div[@align="center"]'
                # o = WebDriverWait(driver, 5).until(EC.element_to_be_clickable ((By.XPATH,n)))

                n = './/input[@id="notProhibitedItem"]'
                n = '//div/p[@class="input-chk-01 mt50"]/label'
                # WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable ((By.XPATH,n)))
                e = driver.find_element_by_xpath(n)
                e.click()

                n = '//div/p[@class="btn-type-02 btn-submit "]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                e = driver.find_element_by_xpath(n)
                e.click()

                # n = '//a[@id="next"]'
                # WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                # e = driver.find_element_by_xpath(n)
                # e.click()

                n = '//a[@id="nextAddressBook"]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                e = driver.find_element_by_xpath(n)
                e.click()    

                # choose which address to create 

                n = '//h1/span[contains(text(),"アドレス帳")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                n = '//div[@class="box-container"]'
                o = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                n = './/div[@class="box-qr-03"]'
                e = o.find_elements_by_xpath(n)

                for c in e:
                    nom = adresse[0]
                    n = './/label/div/h3'
                    namae = c.find_element_by_xpath(n)
                    # print(namae.text)
                    if nom == namae.text:
                        print('nom ', nom)
                        n = './/label/p[@class="input-radio-01"]'
                        c.find_element_by_xpath(n).click()
                        break
                
                n = '//div[@id="div-up"]'
                try:
                    o = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                    o.click()
                except:
                    print('pas de div-up, pas d\'adresse correspondante ?')
                    
                n = '//div[@class="btn-box mt80"]/p/a[@id="next"]'
                o = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                if '次へ' in o.get_attribute('value'):
                    o.click()
                
                # enter now my address
                # 	
                n = '//h1/span[contains(text(),"ご依頼主設定")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                n = '//a[@id="nextAddressBook"]'
                e = driver.find_element_by_xpath(n)
                e.click()    

                n = '//h1/span[contains(text(),"ご依頼主アドレス帳から選択")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                n = '//div[@class="box-container"]'
                o = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                n = './/div[@class="box-qr-03"]'
                e = o.find_elements_by_xpath(n)

                for c in e:
                    nom = 'グルメ ジャポン'
                    # print('nom ', nom)
                    n = './/div/h3'
                    namae = c.find_element_by_xpath(n)
                    if nom in namae.text:
                        n = './/p[@class="input-radio-01"]'
                        c.find_element_by_xpath(n).click()
                        break

                try:
                    n = '//p[@id="btn-down"]/a[@id="next-down"]'
                    o = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,n)))
                except:
                    n = '//div[@id="div-up"]/p[contains(@class,"btn-type-02")]/a[@id="next-up"]'
                    o = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,n)))
                o.click()

                n = '//div[@class="btn-box mt80"]/p/a[@id="next"]'
                o = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                if '次へ' in o.get_attribute('value'):
                    o.click()

                n = '//a[@id="next"]'
                # e = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                # e.click()
                next_button(driver,n)
                # next_button(driver,n)

                n = '//h1/span[contains(text(),"発送場所を選択する")]'
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))

                yamto_basho = ['水戸東原センター']
                n = '//div[@class="box-map"]'
                e = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                n = './/form[@class="form-type-search"]/p/input[@type="search"]'
                f =  e.find_element_by_xpath(n)
                f.clear()
                f.send_keys(yamto_basho[0])
                f.send_keys(Keys.ENTER)
                
                n = '//div[@class="content-inner"]/div/div/div[@class="box-qr-01"]'
                # driver.implicitly_wait(3)
                e =  driver.find_elements_by_xpath(n)
                # print(len(e))
                for f in e:
                    n = '//div[@class="content-inner"]/div/div/div[@class="box-qr-01"]/a'
                    g = driver.find_element_by_xpath(n)
                    if yamto_basho[0] in g.find_element_by_xpath('.//h2').text:
                        g.click()
                        break
                n = '//div[@class="btn-box mt30"]/p/a'
                e = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,n)))
                e.click()

                # enter the timings !!
                n = '//div[@class="content-inner mt20"]'
                e = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                n = './/p[@class="input-01 required"]'
                f =  e.find_elements_by_xpath(n)
                
                g = f[0]
                n = './/select[@name="viwb4100ActionBean.dateToShip"]'
                select = Select(f[0].find_element_by_id('dateToShip'))
                fromDate = dt.datetime.today()
                select.select_by_value(fromDate.strftime('%Y%m%d'))

                #   <option value="0" selected="selected">希望なし</option>
                #     <option value="1">午前中</option>
                #     <option value="3">14時～16時</option>
                #     <option value="4">16時～18時</option>
                #     <option value="5">18時～20時</option>
                #     <option value="7">19時～21時</option>
                # g = f[1]
                try:
                    select = Select(driver.find_element_by_id('dateToReceive'))
                    if adresse[5] not in regions:
                        dateToReceive = fromDate + dt.timedelta(days=2)
                    else:
                        dateToReceive = fromDate + dt.timedelta(days=1)
                    select.select_by_value(dateToReceive.strftime('%Y%m%d'))
                    driver.implicitly_wait(1)

                    if YMT_category == 'YMT_compact' :
                        select = Select(driver.find_element_by_id('timeToReceiveByTZone'))
                    elif YMT_category == 'YMT_frozen' :
                        select = Select(driver.find_element_by_id('timeToReceiveByTZone'))
                    else:
                        select = Select(driver.find_element_by_id('timeToReceiveByTZone'))
                    if '14-16時' in adresse[10]:
                        timeToReceive = "3"
                    elif '16-18時' in adresse[10]:
                        timeToReceive = '4'
                    elif '18-20時' in adresse[10]:
                        timeToReceive = '5'
                    elif '19-21時' in adresse[10]:
                        timeToReceive = '7'
                    elif '午前' in adresse[10]:
                        timeToReceive = '1'
                    else:
                        timeToReceive = '0'
                    select.select_by_value(timeToReceive)
                except NoSuchElementException:
                    print('error')
                

                n = '//div[@class="btn-box mt40"]/p/a[@id="next"]'
                o = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                if '次へ' in o.text:
                    o.click()

                n = '//div[@class="btn-box mt100"]/p/a[@id="doPaymentForward"]'
                o = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                if '支払いへ進む' in o.text:
                    o.click()

                n = '//div[@class="btn-box"]/p/a[@id="directPay"]'
                o = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                if 'キャッシュレス決済' in o.text:
                    o.click()

                # should be ok here...

                n = '//a[@id="returnTop"]'                
                o = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,n)))
                o.click()
            except:
                print('error')

    except NoSuchElementException:
        print('error')
        
    n = '//p[@id="btn-modal-logout"]'
    o = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,n)))
    o.click()
    return

def next_button(d, n):
    e = WebDriverWait(d, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
    e.click()
    return 

if __name__ == '__main__':

    file_name = './orders_list_YMT.csv'
    file_name = './orders_list_YMT.txt'
    address = file_utils.getAddresses(file_name)

    if connectToYMT():
    # connect ok 
        print('traitement des commandes...')
        update_adresses()

    print('fin')