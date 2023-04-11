from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement
import re

import sys
sys.path.append(".")
from orderlib import file_utils

# https://chromedriver.chromium.org/downloads
options = webdriver.ChromeOptions() 
options.add_argument('user-data-dir=C:\\Users\\blgl\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #Path to your chrome profile
driver = webdriver.Chrome(executable_path="C:\\Loys\\Google drive - ltd-japon\\Dev\\web\\Chrome\\chromedriver.exe", chrome_options=options)

address = []

def update_adresses():
    driver.get("https://cmypage.kuronekoyamato.co.jp/portal/entrance")
    # driver.get("https://ship-book.kuronekoyamato.co.jp/ship_book/index.jsp?_A=OTODOKE")
    try:

        try:
            a = driver.find_element_by_xpath('//a/p[contains(text(), "アドレス帳")]')
        except:
            a = driver.find_element_by_xpath('//h1[contains(text(), "アドレス帳")]')
        a.click()

        # get list of addresses
        for add in address:
            adresse = add.split(',')

            n = '//a[@id="button_regist"]'
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
            except:
                print("plus de place ?")
            a = driver.find_element_by_xpath(n)
            driver.execute_script("arguments[0].scrollIntoView(true);", a)
            a.click()

            n = '//input[@id="lastNmCenter"]'
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,n)))
            e = driver.find_element_by_xpath('//input[@id="lastNmCenter"]')
            # driver.execute_script("arguments[0].scrollIntoView(true);", e)
            # probleme avec send_keys
            while (True):
                e.send_keys(adresse[1])
                try:
                    WebDriverWait(driver, 1).until(EC.text_to_be_present_in_element_value((By.XPATH,n),adresse[1]))
                    break
                except:
                    pass

            e = driver.find_element_by_xpath('//input[@id="firstNmCenter"]')
            e.send_keys(adresse[2])
            e = driver.find_element_by_xpath('//input[@id="telCenter"]')
            tel = adresse[3]
            if (tel[0:2] == '81'):
                tel = tel[2:len(tel)]
            elif (tel[0:3] == '+81'):
                tel = tel[3:len(tel)]
            e.send_keys(tel)
            
            e = driver.find_element_by_xpath('//input[@id="zipCd"]')
            e.send_keys(adresse[4])
            # e = driver.find_element_by_xpath('//input[@id="address1"]')
            # e.send_keys(adresse[5])
            # e = driver.find_element_by_xpath('//input[@id="address2"]')
            # e.send_keys(adresse[6])
            # e = driver.find_element_by_xpath('//input[@id="address3"]')

            for i in range(5,len(adresse)-2):
                j = i-4
                n = '//input[@id="address' + str(j) + 'Center"]'
                try:
                    e = driver.find_element_by_xpath(n)
                except:
                    continue
                n_i = adresse[i]
                nn=n_i.replace('　','')
                nn.replace(' ','')
                nn.replace('\n','')
                # move 番号 to next field necessary
                if j == 2:
                    m = re.search(r"\d", nn)
                    if m:
                        k = m.start()
                        adresse[i+1] += nn[k:]
                        e.send_keys(nn[:k])
                        continue
                #     else:
                #         e.send_keys(nn)
                # else:    
                e.send_keys(nn)
          
            b = driver.find_element_by_xpath('//button[@name="_BTN_REGISTER"]')
            b.click()

    except NoSuchElementException:
        print('error')

    a = driver.find_element_by_xpath('//a[contains(text(), "ログアウト")]').click()
    return

kuroneko_id = 'BK4XU755'
kuroneko_id = 'RAV7B3G9'
kuroneko_pwd = 'xxxxx'

def connectToYMT():
    driver.get("https://cmypage.kuronekoyamato.co.jp/portal/entrance")
    try:
        # enter mot de passe
        try:
            k_id = driver.find_element_by_xpath('//input[@id="kuroneko_id"]')
        except:
            k_id = driver.find_element_by_xpath('//input[@id="login-form-id"]')
        k_id.clear()
        k_id.send_keys(kuroneko_id)

        # enter mot de passe        
        try:
            pwd = driver.find_element_by_xpath('//input[@type="password"]')
        except:
            pwd = driver.find_element_by_xpath('//input[@type="login-form-password"]')
        pwd.send_keys(kuroneko_pwd)

        try:
            o = driver.find_element_by_xpath('//button[@type="submit"]')
        except:
            o = driver.find_element_by_xpath('//button[@id="login-form-submit"]')
        o.click()

        driver.get("https://ship-book.kuronekoyamato.co.jp/ship_book/index.jsp?_A=OTODOKE")
        # "https://ship-book.kuronekoyamato.co.jp/ship_book/index.jsp?_A=OTODOKE&_R=menu_personal_portal&utm_source=NRCWBMM0120"
        a = driver.find_element_by_xpath('//a/p[contains(text(), "アドレス帳")]')
        a.click()

    except NoSuchElementException:
        print('erreur connexion YMT')

    return

def cleanUpYMTaddresses() -> int :

    driver.get("https://cmypage.kuronekoyamato.co.jp/portal/entrance")
    try:

        try:
            a = driver.find_element_by_xpath('//a/p[contains(text(), "アドレス帳")]')
        except:
            a = driver.find_element_by_xpath('//h1[contains(text(), "アドレス帳")]')
        a.click()

        encore = True
        i = 0
        while(encore):
            # get list of entries
            try:
                liste_addresses = driver.find_elements_by_xpath('//div[@class="box-send-head"]')
                encore = False if len(liste_addresses) == 0 else True
                if not encore:
                    print("No address to erase")
                    break
            except NoSuchElementException:
                print("No address to erase")
                break

            # print('encore ', encore)
                    
            add = liste_addresses[0]
            print(add.text)
            name = add.find_element_by_xpath('//div/div[@class="box-send-head-title"]/p')
            print(name.text)

            b = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//button[@name="_BTN_UPDATE"]')))
            # b = add.find_element_by_xpath('//button[@name="_BTN_UPDATE"]')
            b.click()

            a = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//a[@href="#modal-delete"]')))
            # a = driver.find_element_by_xpath('//a[@href="#modal-delete"]')
            a.click()
                
            # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            # new_win = driver.window_handles
            # print(len(new_win))
            # print(new_win[0],new_win[1])
            # driver.switch_to.window(new_win[1])

            try:
                b = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//button[@name="_BTN_DELETE"]')))
                # b = driver.find_element_by_xpath('//button[@name="_BTN_DELETE"]')
                b.click()      
            except NoSuchElementException:
                s = 'erreur efface adresse Yamato'
                print(s)

            # driver.close()   
            # driver.switch_to.window(new_win[0])
            i += 1
            # if i == 5:
            #     break
        
        a = driver.find_element_by_xpath('//a/span[contains(text(), "前の画面に戻る")]')
        a.click()

    except:
        print("erreur...")
    
    return i

cleanUp = False
if __name__ == '__main__':

    file_name = './orders_list_YMT.txt'
    # file_name = './orders_list_YMT.csv'
    # file_name = './orders_list_YMT-restant.csv'
    address = file_utils.getAddresses(file_name)

    connectToYMT()
    if ( cleanUp ):
        i = cleanUpYMTaddresses()
        print('effacé : ', i,' adresses !')
        
    update_adresses()