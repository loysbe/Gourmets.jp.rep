from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement
import re
import csv

# from facebook import GraphAPI

# graph = GraphAPI(version=8.0)
# graph.access_token = graph.get_app_access_token(APP_ID, APP_SECRET)

# https://chromedriver.chromium.org/downloads
options = webdriver.ChromeOptions() 
options.add_argument('user-data-dir=C:\\Users\\Loys\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #Path to your chrome profile
driver = webdriver.Chrome(executable_path="E:\\Google drive - ltd-japon\\Dev\\web\\Chrome\\chromedriver.exe", chrome_options=options)

new_win = []
nb_email = 0
nb_noms = 0

def get_lead(file_name,web_name):
    if ( web_name == 'tabelog' ):
        category = ['french']
        base_url = 'https://tabelog.com/rstLst/french/'
        # param = '?genre_name=french&LstCatD=RC0211&LstCat=RC02&Cat=RC'
        # paramètres
        # budget min = LstCos ; budget max = LstCosT 1~6,8,10,15,20
        # lunch RdoCosTp = 1 ; diner : 2
        param = '?LstCatD=RC0211&LstCat=RC02&Cat=RC'
        param += '&RdoCosTp=1&LstCos=6'
        base_url = 'https://tabelog.com/rstLst/' + category[0] + '/'

        # param = '?LstReserve=0&LstSmoking=0&svd=20210317&svt=1900&svps=2&vac_net=0&LstCos=4&RdoCosTp=2'
        tabelog(file_name,base_url,param)
       
    elif ( web_name == 'gurunavi' ):
        url = 'https://r.gnavi.co.jp/food/french/rs/' 
        param = '?prl=10000'
        # param += '&resc=1&fwc=フレンチ（フランス料理）'
        gurunavi(file_name,url+param)    

    elif ( web_name == 'retty' ):
        url = 'https://retty.me/restaurant-search/search-result/'
        free_word_category = 'フランス料理'
        param = '?budget_meal_type=2&min_budget=8&free_word_category=' + free_word_category + '&category_type=170' 
        retty(file_name,url+param)
    
    elif ( web_name == 'michelin'):
        url = 'https://clubmichelin.jp'
        url = 'https://my.gnavi.co.jp/authority/login/?cType=clubmichelin02'
        michelin(file_name,url)

def michelin(file_name,url):
    driver.get(url)
    restau = {}

    # login
    # 
    n = '//input[@name="memberloginid"]'
    o = driver.find_element_by_xpath(n)
    o.send_keys('loys_belleguie@yahoo.co.jp')
    n = '//input[@name="memberpassword"]'
    o = driver.find_element_by_xpath(n)
    o.send_keys('asdasd00')
    n = '//input[@class="button-login4" and @value="LOGIN"]'
    o = driver.find_element_by_xpath(n)
    o.click()

    # select category
    #
    # url_search = 'https://clubmichelin.jp/search/restaurant/'
    url_search = 'https://clubmichelin.jp/search/restaurant/?st[]=3&amp;rt[]=11&amp;sc_lid=cm_keywords_210121'
    # driver.get(url)
    js_command = "document.getElementsByName('keyword2')[0].click();"
    js_class = 'mvInput__input mvInput__input__search  js-search-submit'
    js_command = 'document.getElementsByClass(\"' + js_class + '\")[0].click();'
    # driver.execute_script(js_command)

    n = '//a[@class="mvInput__input js-select-val"]'
    o = driver.find_element_by_xpath(n)
    driver.execute_script("arguments[0].click();", o)

    n = '//a[@class="popup__submit js-select-submit"]'
    # o = driver.find_element_by_xpath(n)
    o = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n)))
    o.click()

    n = '//a[@class="mvInput__input js-select-val" and contains(text(),"料理カテゴリー")]'
    # o = driver.find_element_by_xpath(n)
    o = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n)))
    o.click()

    n = '//div[@class="popup-body__inner"]/ul/li/label/input'
    n = '//div[@class="popup-body__inner"]/ul/li/label/span[contains(text(),"フランス料理")]'
    o = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n)))
    o.click()
    
    # e = driver.find_elements_by_xpath(n)
    # li_l = len(e)
    # for i in e:
    #     # l = i.get_attribute('data-val')
    #     l = i.get_attribute('innerHTML')
    #     if l == 'フランス料理':
    #     # if l == '日本料理':
    #         i.click()
    #         break

    # 料理のカテゴリー
    #
    n = '//a[@class="popup__submit js-select-submit"]'
    o = driver.find_elements_by_xpath(n)
    # o = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n)))
    # o = WebDriverWait(driver, 20).until(EC.presence_of_elements_located((By.XPATH,n)))
    print(len(o))
    for i in range(len(o)):
        try:
            o[i].click()
            break
        except:
            pass

    n = '//a[@class="mvInput__input mvInput__input__search  js-search-submit"]'
    o = driver.find_element_by_xpath(n)
    driver.execute_script("arguments[0].click();", o)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    n = '//div[@class="count-current"]'
    o = driver.find_element_by_xpath(n)
    # print(o.text)
    # print(o.get_attribute('innerHTML'))
    # print(o.get_attribute('outerHTML'))

    total_entries = int(o.get_attribute('innerHTML').replace('件','').replace(',',''))
    print(total_entries,' entrées..')

    nb_check = 0
    while( True ):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        n = '//div[@class="entry-content"]'
        e = driver.find_elements_by_xpath(n)
        nb_entries = len(e)
        if nb_entries == nb_check :
            print(nb_entries, nb_check)
        #     n = '//a[@class="button-pagetop"]'
        #     # o = driver.find_element_by_xpath(n)
        #     o = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,n)))
        #     o.click()
            
        nb_check = nb_entries
        if ( nb_entries >= total_entries ):
        # if nb_entries == nb_check :
            for r in e:
            # for i in range(1):
                # r = e[i]
                n = './/a[@class="entry-info-texts"]'
                o = r.find_element_by_xpath(n)
                # url = 'https://clubmichelin.jp' + o.get_attribute('href')
                url = o.get_attribute('href')
                # print(url)

                n = './/h2[@class="name"]'
                o = r.find_element_by_xpath(n)
                nom = o.get_attribute('innerHTML')
                # print(nom, o.text)

                # get rating
                n = './/a[@class="entry-icons-main"]/*/div[@class="rating"]/div'
                o = r.find_element_by_xpath(n)
                # url = 'https://clubmichelin.jp' + o.get_attribute('href')
                classe = o.get_attribute('class')

                restau[nom] = [url,classe]

            break

    michelin_url = get_michelin_info(restau)

    with open(file_name, 'w', newline='',encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerows(michelin_url)  
    
    return

def get_michelin_info(restau) -> []:

    # current_win = driver.window_handles
    
        # driver.switch_to.window(current_win[0])
    adr = []
    adr.append(['Restaurant','url','classement Michelin'])
    for nom in restau:
        # new window 
        print(nom)
        u = restau[nom][0]
        c = restau[nom][1]
        driver.execute_script('''window.open('',"_blank");''')
        WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
        new_win = driver.window_handles
        driver.switch_to.window(new_win[1])
        driver.get(u)
        
        url = ''
        n = '//div[@class="mod-infolist mi-data"]/dl/dd/a'
        try:
            o = driver.find_element_by_xpath(n)
            url = o.get_attribute('href')
            print(url)
        except:
            print("pas de site web..")
        adr.append([nom,url,c])
        driver.close()   
        driver.switch_to.window(new_win[0])

    return adr

def retty(file_name,url):
    driver.get(url)
    adresses:str = []
    # get number of pages
    # 
    o = driver.find_element_by_xpath('//span[contains(@class,"search-result__hit-count")]')
    nb = o.text
    nb = nb[:len(nb)-1]
    print(nb)
    page_max = int(nb)//20
    # page_max = 20
    print(page_max)
    page_num = 32
    adresses.append('nom,nom2,adresse,retty,url,fb,mail')
    saveAddresses(file_name,adresses)
    while(page_num<page_max):
        adresses.clear()
        page_num += 1
        adresses = process_page_retty(page_num)
        saveAddresses(file_name,adresses)
    return

def process_page_retty(page_num) -> [str]:
    global nb_noms
    adresses:str = []

    url = 'https://retty.me/restaurant-search/search-result/?page=' + str(page_num)
    free_word_category = 'フランス料理'
    param = '&free_word_category=' + free_word_category + '&category_type=170&budget_meal_type=2&min_budget=8' 
    driver.get(url+param)

    print('\n *************** \n page : ', page_num)
    print(url)

    try:
        # list all restaurants
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//ul[contains(@class,"pager")]')))
        # should be displayed
        o = driver.find_elements_by_xpath('//a[contains(@class,"restaurant__block-link")]')
        # print(len(o))

        for m in o:
            nom = m.find_element_by_xpath('.//h3[@class="restaurant__name"]').text
            nom = nom.strip(free_word_category + ' ')
            retty = m.get_attribute('href')
            # # debug print(m.get_attribute('outerHTML'),tabelog)
            # m.get_attribute('innerHTML'),
            # n = '//a[contains(text(),"' + nom + '")]'
            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n))) 
            m.click()

            WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
            new_win = driver.window_handles
            driver.switch_to.window(new_win[1])
        
            nb_noms += 1
            print(nb_noms, nom)

            # 場所
            n = '//div[@class="restaurant-info-table__map"]/a[@class="restaurant-info-table__link"]'
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,n)))
                add = driver.find_element_by_xpath(n)
                region = get_region(add.text)
                print(region)
                s = '"' + nom + '",,"' + region + '","' + retty + '",'
            except:
                print('problem')
                return

            try:
                # check if home page
                n = '//a[contains(@class,"js-log-action restaurant-info-table__link")]'
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,n)))
                    hp = driver.find_element_by_xpath(n)
                    l = hp.get_attribute("href")
                    print(l)
                    s += '"' + l + '",'
                except:
                    print('pas de site web')
                    s += ','
                
                # check if FB
                n = '//a[contains(@href,"facebook")]'
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,n)))
                    fb = driver.find_elements_by_xpath(n)
                    done = False
                    for f in fb:
                        l = f.get_attribute("href")
                        if ('sharer' not in l and 'com/retty.me' not in l):
                            s +=  '"' + l + '",'
                            done = True
                            break
                    if not done:
                        s +=  ','
                           
                except:
                    print('pas de fb',add[1].get_attribute("href"))
                    s += ','

                # check if mail
                n = '//a[contains(@href,"mailto")]'
                try:
                    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,n)))
                    o = driver.find_element_by_xpath(n)
                    email = o.get_attribute('href').split(':')
                    print(email[1])
                    s += '"' + email[1] + '",'
                except:
                    print('pas de mail')
                    s += ','

                # try others
                n = '//*[contains(text(),"mail")]'
                try:
                    o = driver.find_element_by_xpath(n)
                    if 'script' not in o.tag_name :
                        print(o.text)
                except:
                    pass
                n = '//*[contains(text(),"メール")]'
                try:
                    o = driver.find_element_by_xpath(n)
                    print(o.text)
                except:
                    pass
                n = '//*[contains(text(),"@")]'
                try:
                    o = driver.find_element_by_xpath(n)
                    if 'style' not in o.tag_name :
                        print(o.text)
                except:
                    pass

            except NoSuchElementException:
                print('erreur')
                pass

            adresses.append(s)

            driver.close()   
            driver.switch_to.window(new_win[0])

    except NoSuchElementException:
        print('error')
        pass
        
    return adresses

def gurunavi(file_name,url):
    driver.get(url)
    adresses:str = []
    # get number of pages
    # 
    o = driver.find_element_by_xpath('//span[contains(@class,"result-stats__total")]')
    nb = o.text.strip('全')
    nb = nb[:len(nb)-1]
    print(nb)
    page_max = int(nb)//20
    # page_max = 1
    print(page_max)
    page_num = 0
    adresses.append('nom,nom2,adresse,gurunavi,url,fb,mail')
    saveAddresses(file_name,adresses)

    while(page_num<page_max):
        adresses.clear()
        page_num += 1
        adresses = process_page_gurunavi(page_num)
        saveAddresses(file_name,adresses)
    return

def process_page_gurunavi(page_num) -> [str]:
    global nb_noms
    adresses:str = []

    url = 'https://r.gnavi.co.jp/food/french/rs/?prl=10000&p=' + str(page_num)
    driver.get(url)

    print('\n *************** \n page : ', page_num)
    print(url)

    try:
        # list all restaurants
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//span[contains(@class,"result-stats__total")]'))) 
        o = driver.find_elements_by_xpath('//a[contains(@class,"result-cassette__box-title js-measure")]')

        for m in o:
            nom = m.text
            gurunavi = m.get_attribute('href')
            # # debug print(m.get_attribute('outerHTML'),tabelog)
            # m.get_attribute('innerHTML'),
            n = '//a[contains(text(),"' + nom + '")]'
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n))) 
            m.click()

            WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
            new_win = driver.window_handles
            driver.switch_to.window(new_win[1])
        
            nb_noms += 1
            print(nb_noms, nom)

            # 場所
            n = '//span[@class="region"]'
            add = driver.find_elements_by_xpath(n)
            region = get_region(add[0].text)
            print(region)

            s = nom + ',,"' + region + '","' + gurunavi + '",'
            try:
                # check if home page
                n = '//a[contains(text(),"お店のホームページ")]'
                try:
                    WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,n)))
                    hp = driver.find_element_by_xpath(n)
                    l = hp.get_attribute("href")
                    print(l)
                    s += '"' + l + '",'
                except:
                    # print('pas de site web')
                    s += ','
                
                # check if FB
                n = '//a[contains(@href,"facebook")]'
                try:
                    WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,n)))
                    fb = driver.find_element_by_xpath(n)
                    l = fb.get_attribute("href")
                    s +=  '"' + l + '",' 
                except:
                    # debug print('pas de fb')
                    s += ','

                # check if mail
                n = '//a[contains(@href,"mailto")]'
                try:
                    WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,n)))
                    o = driver.find_element_by_xpath(n)
                    email = o.get_attribute('href').split(':')
                    print(email[1])
                    s += '"' + email[1] + '",'
                except:
                    # print('pas de mail')
                    s += ','

            except NoSuchElementException:
                print('erreur')
                pass

            adresses.append(s)

            driver.close()   
            driver.switch_to.window(new_win[0])

    except NoSuchElementException:
        print('error')
        pass
        
    return adresses

def get_region(jusho1):
    j = jusho1.find("県")
    if (j != -1):
        jusho0 = jusho1[0:j+1]
        jusho1 = jusho1[j+1:len(jusho1)]
    else:    
        # 大阪府　東京都　京都府
        jusho0 = jusho1[0:3]
        jusho1 = jusho1[3:len(jusho1)]
    return jusho0

def tabelog(file_name,base_url,param):
    driver.get(base_url+param)
    adresses:str = []

    # get number of pages
    # 
    o = driver.find_elements_by_xpath('//span[contains(@class,"c-page-count__num")]/strong')
 
    page_max = int(o[2].text)//20
    # page_max = 2
    print('Nombre de restaurants : ', o[2].text)
    print(page_max)
    page_num = 0
    adresses.append('nom,adresse,tabelog,url,fb,mails,tel,budget,keyword')
    saveAddresses(file_name, adresses)
    while(page_num<page_max):
        adresses.clear()
        page_num += 1
        adresses = process_page_tabelog(page_num, base_url, param)
        saveAddresses(file_name, adresses)
    return

def process_page_tabelog(page_num, base_url, param) -> [str]:
    global nb_noms
    adresses:str = []

    url = base_url + str(page_num) + '/' + param
    driver.get(url)

    print('\n *************** \n page : ', page_num)
    print(url)

    try:
        # list all restaurants
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//h4[contains(@class,"list-rst__rst-name")]'))) 
        o = driver.find_elements_by_xpath('//a[contains(@class,"list-rst__rst-name-target cpy-rst-name")]')

        for m in o:
            nom = m.text
            tabelog = m.get_attribute('href')
            # # debug print(m.get_attribute('outerHTML'),tabelog)
            # m.get_attribute('innerHTML'),
            n = '//a[contains(text(),"' + nom + '")]'
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,n))) 
            m.click()

            WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
            new_win = driver.window_handles
            # # debug print(len(new_win))
            # # debug print(new_win[0],new_win[1])
            # https://stackoverflow.com/questions/53690243/selenium-switch-tabs
            driver.switch_to.window(new_win[1])

            # n = '//div[@class,"rdheader-rstname"]'
            n = '//div[contains(@class,"rdheader-rstname")]/span[contains(@class,"alias")]'
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                o = driver.find_element_by_xpath(n)
                nom += ' ' + o.text
            except:
                pass

            nb_noms += 1
            print(nb_noms, nom)

            # 場所
            n = '//p[contains(@class,"rstinfo-table__address")]/span'
            add = driver.find_elements_by_xpath(n)

            s = nom + ',"' + add[0].text + '","' + tabelog + '",'
            try:

                # check if home page
                n = '//p[contains(@class,"homepage")]'
                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                    hp = driver.find_element_by_xpath('//p[contains(@class,"homepage")]/a')
                    l = hp.get_attribute("href")
                    # debug print(l)
                    s += '"' + l + '",'
                except:
                    # debug print('pas de site web')
                    s += ','
                
                # check if FB
                n = '//a[contains(@class,"rstinfo-sns-link rstinfo-sns-facebook")]'
                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                    fb = driver.find_element_by_xpath(n)
                    l = fb.get_attribute("href")
                    # debug print("facebook link ", l)
                    mails = get_fb_info(fb,l)
                    # # debug print(*new_win)
                    s +=  '"' + l + '",' + '"' + mails + '",'
                except:
                    # debug print('pas de fb')
                    s += ',' + '"0",'

                n = '//p[contains(@class,"rstinfo-table__tel-num-wrap")]'
                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                    tel = driver.find_element_by_xpath(n).text
                    # debug print("tel ", tel)
                    s += '"' + tel + '",'
                except:
                    # debug print('pas de tel')
                    s += ','
                
                bud = driver.find_elements_by_xpath('//em[contains(@class,"gly-b-lunch")]')
                sb = ''
                for b in bud:
                    sb += b.text + " | "
                # debug print(sb)
                s += '"' + sb + '",'

            except NoSuchElementException:
                # debug print('erreur')
                pass

            # check if page has keyword
            key_word = 'フォアグラ'
            key_word2 = 'フォワグラ'
            key_words = [key_word,key_word2]

            n = '//p[contains(text(),"' + key_word + '" or "' + key_word2+ '")]'
            try:
                o = driver.find_elements_by_xpath(n)
                # debug print(key_word, len(o))
                if (len(o) == 0):
                    # essaie dans le menu
                    n = '//a[contains(text(),"コース詳細")]'
                    p = driver.find_elements_by_xpath(n)
                    p[0].click()
                    n = '//div[@class="course-dtl"]'
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
                    # check within table (from real contents)                    
                    try:
                        n = '//th[contains(text(),"コース内容")]/following-sibling::td'
                        q = driver.find_element_by_xpath(n)
                        t = q.text
                        # n = '//div[contains(text(),"' + key_word + '")]'
                        # q = driver.find_elements_by_xpath(n)
                        # r = q.parent.td
                        # # debug print(s)
                        # for e in q:
                        #     if ( e.tag_name != 'a' ):
                        # if ( s.find([key_word,key_word2]) != -1 ):
                        if any(x in t for x in key_words):
                            s += key_word
                            # # debug print(e.tag_name)
                            # # debug print(q.get_attribute('outerHTML'),q.get_attribute('innerHTML'))
                            # # debug print(q.text)
                    except NoSuchElementException:
                        # debug print('no key')
                        pass
                else:
                    s += key_word
            except:
                # debug print('pas de mot clé ',key_word)
                pass
                
            adresses.append(s)

            driver.close()   
            driver.switch_to.window(new_win[0])

    except NoSuchElementException:
        # debug print('error')
        pass
        
    return adresses

def get_fb_info(a,url)->str:
    global nb_email
    # a tag with href to fb
    # global new_win
    mails = ''
    if (a != None):
        try:
            # # debug print(a.get_attribute('outerHTML'),a.get_attribute('innetHTML'),a.text)
            a.click()

            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))
            win = driver.window_handles
            # # debug print(*win,sep=', ')
            driver.switch_to.window(win[2])

            # n = '//a[contains(@href,"/about/")]'
            # n = '//a/span[contains(text()," propos")]'
            n = '//a[contains(@href,"mailto")]'
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,n)))
            except:
                # debug print('pas de mail fb')
                driver.close()
                driver.switch_to.window(win[1])
                return '0'
            o = driver.find_elements_by_xpath(n)
            # # debug print(m.get_attribute('outerHTML'),m.get_attribute('innetHTML'),m.text)
            mails = str(len(o)) 
            for m in o:
                email = m.get_attribute('href').split(':')
                # debug print(email[1])
                mails += ' | ' + email[1]
                nb_email += 1

            driver.close()
            # # debug print(*new_win)
            driver.switch_to.window(win[1])

        except:
            # debug print('erreur click fb')
            pass
        return mails

    # graph -> marche pas ??
    # global graph
    # try:
    #     site_info = graph.get_object(id="https%3A//www.facebook.com/lembellir.tokyo",fields="og_object")
    #     # debug print(site_info["og_object"]["description"])
    #     objects = graph.get_object(id=url, fields='name')
    #     for page in objects.values():
    #         # debug print(page)
    #         # # debug print('{}: {}'.format(page['name'], ', '.join(page['emails'])))
    # except:
    #     # debug print('erreur fb')
    # return

def get_hp_info(url,fb) -> [str] :
    
    email = ''
    fb_url = ''
    form_url = ''
    
    try:
        driver.get(url)
    except:
        print('erreur url')
        return [email,fb_url,form_url]
   
    print(url)

    try:
        # check if mail
        email = seek_for_email()
        if fb:
            # check if FB
            n = '//a[contains(@href,"facebook")]'
            try:
                # WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,n)))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,n)))
                fb_urls = driver.find_elements_by_xpath(n)
                for f in fb_urls:
                    l = f.get_attribute("href")
                    print('fb ', l)
                    if ('sharer' not in l ):
                        fb_url = l
                        break
            except:
                print('pas de page fb')
               
        if (email == ''):
        # try other pages if any
            n = '//a[contains(@href,"about")]'
            try:
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,n)))
                o = driver.find_element_by_xpath(n)
                u = o.get_attribute('href')
                print(u)
                try:
                    driver.get(u)
                except:
                    print('erreur url')
                email = seek_for_email()
            except:
                print('pas de page about')
            
            n = '//a[contains(@href,"information")]'
            try:
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,n)))
                o = driver.find_element_by_xpath(n)
                u = o.get_attribute('href')
                print(u)
                try:
                    driver.get(u)
                except:
                    print('erreur url')
                email = seek_for_email()
            except:
                print('pas de page information')

            n = '//a[contains(@href,"contact")]'
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,n)))
                o = driver.find_element_by_xpath(n)
                u = o.get_attribute('href')
                print(u)
                try:
                    driver.get(u)
                except:
                    print('erreur url')
                email = seek_for_email()
                if email == '':
                    # pas d'email, cherche une forme...
                    n = '//form[contains(@method,"post")]'
                    try:
                        o = driver.find_element_by_xpath(n)
                        print('form')
                        form_url = u
                    except:
                        pass
            except:
                print('pas de page contact')


    except NoSuchElementException:
        print('error')
    return [email,fb_url,form_url]

def seek_for_email() -> str :
    email = ''
    # check if mail
    n = '//a[contains(@href,"mailto")]'
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,n)))
        o = driver.find_element_by_xpath(n)
        m = o.get_attribute('href').split(':')
        print(m[1])
        email = m[1]
        # got it return
        return email
    except:
        print('pas de mail')
    
    n = '//*[contains(text(),"mail")]'
    try:
        o = driver.find_element_by_xpath(n)
        if 'script' not in o.tag_name :
            print(o.text)
    except:
        pass
    n = '//*[contains(text(),"メール")]'
    try:
        o = driver.find_element_by_xpath(n)
        print(o.text)
    except:
        pass
    n = '//*[contains(text(),"@")]'
    try:
        o = driver.find_element_by_xpath(n)
        if 'style' not in o.tag_name :
            print(o.text)
    except:
        pass

    return email

def process_home_page(fichier):
    out_file = './lead/lead_french_edit5.csv'
    # f = open(fichier, 'r',encoding='utf-8')
    count = 0
    i = 0
    lignes = []

    with open(fichier, newline='',encoding='utf-8') as csvfile:
        ligne = csv.reader(csvfile, delimiter=',', quotechar='\"')
        for add in ligne:
            # print(add)
            # if count < 2:
            #     continue
            
            info = []
            url = add[4]
            fb_url = add[5]
            email_address = add[6]
            fb = False

            # get mail
            if ( email_address == '' and url != '' ):
                i+=1
                print(add[0],url)
                if (fb_url == '' or 'facebook.com/share' in fb_url): 
                    # get fb as well
                    fb_url = ''
                    fb = True
                if 'url' not in url :
                    info = get_hp_info(url,fb)
                    add[5] = info[1]
                    add[6] = info[0]
                    add[10] = info[2]
            
            if ( add[5] != '' or  add[6] != '' or  add[10] != '' ):
                new_line = ''
                # print('len(add)',len(add))
                for k in range(len(add)-1):
                    new_line += '\"' + add[k] + '\"' + ','
                # new_line = new_line.strip()
                lignes.append(new_line)
                count += 1

            if (count % 20 == 0 ):
                OutFile = open(out_file,'a+',encoding='utf-8')
                for s in lignes:
                    OutFile.write("%s\n" % s)
                OutFile.close()
                lignes.clear()
            # if ( i > 10 ):
            #         break

    OutFile = open(out_file,'a+',encoding='utf-8')
    for s in lignes:
        OutFile.write("%s\n" % s)
    OutFile.close()
    csvfile.close()
    return

from datetime import datetime
def saveAddresses(file_name,adresses):
    f = open(file_name,'a+',encoding='utf-8') 
    for s in adresses:
        f.write("%s\n" % s)
    f.close()
    return

def createFile(file_name):
    f = open(file_name,'w+',encoding='utf-8') 
    f.close()
    return

def getAddresses(fichier):
    adresses:str = []
    
    i=0
    for a in add[1:len(add)]:
        
        # print(b[0],b[6])
        if ( b[6] != ''):
            if ( b[7] == '1' ):
                already_done.append(b[6])
            if ( b[6] not in already_done ):
                print(b[6], i)
                i+=1
                adresses[b[0]] = b[6]
    return adresses

if __name__ == '__main__':
    initial_lead = False
    if initial_lead:
        web_name = 'gurunavi'
        web_name = 'retty'
        web_name = 'tabelog'
        web_name = 'michelin'
        # file_name = web_name + '_lead_list' + datetime.today().strftime('%Y-%m-%d-%Hh%M') + '.csv'
        file_name = web_name + '_lead_list-' + datetime.today().strftime('%Y-%m-%d') + '.csv'
        file_name = './lead/' + file_name
        # file_name = r'.\lead\lead_list.csv'
        createFile(file_name)
        # saveAddresses()
        get_lead(file_name,web_name)
    else:
        # fichier = r'.\lead\lead_french2.csv' 
        fichier = r'.\lead\lead_french.xlsx - lead_french_edit.csv' 
        process_home_page(fichier)