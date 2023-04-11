from selenium import webdriver
from selenium.common.exceptions import *
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import re

firefox = False
language = 'EN'
address = []

if firefox: 
    # fp = webdriver.FirefoxProfile('C:/Users/Loys/AppData/Roaming/Mozilla/Firefox/Profiles/ax8azgih.default')
    # driver = webdriver.Firefox(firefox_profile=fp)
    driver = webdriver.Firefox()
else:
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('user-data-dir=C:\\Users\\Loys\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #Path to your chrome profile
    driver = webdriver.Chrome(executable_path="E:\\Dev\\web\\Chrome\\chromedriver.exe", chrome_options=options)
    # driver.minimize_window()

def amz():    
    hasOrders = False
    # options = webdriver.FirefoxOptions()
    # driver_path = 'E:\\Dev\\web\\Gekco'

    # driver = webdriver.Firefox(executable_path=driver_path,firefox_options=options)
    
    # allCookies = setCookies()
    # print(allCookies)

    amz_id = 'loys@ltd-japon.com'
    amz_pwd = 'xxxxx'
    
    global driver

    # allCookies = setCookies()
    
    login_page = 'https://sellercentral.amazon.co.jp/'
    driver.get(login_page)
    # assert "Amazon" in driver.title
    # for c in allCookies:
    #     driver.add_cookie(c)
  
    # <button class="secondary" type="button">  Sign In </button>
    try:
        b = driver.find_element_by_xpath('//kat-button[@id="sign-in-button"]')
        print('sign-in-button')
        # b = driver.find_element_by_xpath('//button[normalize-space()="Sign In"]')
    except:
        print('pb....')

    driver.implicitly_wait(2)   
    b.click()
    
    # check if switch account page is presented
    # ('//h3[text()="フランスのご馳走の専門店！"]')
    signIn = False
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[text()="アカウントの切り替え"]')))
        print(element)
        a = driver.find_element_by_xpath('//h1[text()="アカウントの切り替え"]')
        print('got switch account page', a)
        try:
            o = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[@action="/ap/switchaccount"]'))) # '//a[@data-name="switch_account_request"]')))
            if amz_id in o.text:
                print('sign-in page')
                signIn = True
                ActionChains(driver).move_to_element(o).click(o).perform()
        except NoSuchElementException:
            print('no switch_account_request element')
    except NoSuchElementException:
        print('no switch page or error')
    except TimeoutException:
        print('normal login')

    if signIn:
        # should be the direct password login page
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form[@name="signIn"]')))
            password = driver.find_element_by_id("ap_password")
            password.clear()
            password.send_keys(amz_pwd)
            driver.implicitly_wait(2)
        except NoSuchElementException:
            print('no switch_account_request element')
    else:
        print('standard page')

        # check here if login id/pwd already in fields

        # username = driver.find_element_by_id("ap_email")
        # username.clear()
        # driver.implicitly_wait(2)
        # username.send_keys(amz_id)
        # driver.implicitly_wait(2)

        # password = driver.find_element_by_id("ap_password")
        # password.clear()
        # driver.implicitly_wait(2)
        # password.send_keys(amz_pwd)
        # driver.implicitly_wait(2)

    b = driver.find_element_by_id('signInSubmit')    
    b.click()

    if driver.find_elements_by_id('auth-mfa-otpcode'):
        print("auth-mfa-otpcode exists")
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "OrderSummary")))
            print('got logged page', element)
            allCookies = getCookies()
        finally:
            driver.close()
            return  
    else:
        print('passed OTP')

    action = ActionChains(driver)
    firstLevelMenu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'sc-navtab-orders')))
    action.move_to_element(firstLevelMenu).perform()
    print("got orders menu")
    secondLevelMenu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//a[contains(text(),"Manage Orders")]')))
    # ActionChains(driver).move_to_element(secondLevelMenu).click(secondLevelMenu).perform()
    secondLevelMenu.click()

    # check if we are indeed in "Manage Orders" page
    manageOrders = False
    try:
        h1 = driver.find_elements_by_xpath('//h1')
    except:
        print('not in orders page')
    for h in h1:
        span = h.find_element_by_xpath('.//span[text()="Manage Orders"]')
        print(span.text)
        if "Manage Orders" in span.text:
            print('manage orders page')
            manageOrders = True
            break
        else:
            print('Error, no orders page')
            continue
    
    print('manageOrders', manageOrders)
    if manageOrders:
        # how many orders ?
        print('how many orders ?')
        # bizarre ici, timing aleatoire --> voir WebDriverWait is fork etc... marche seulement avec les print explicites...
        o = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//a[@data-test-id="tab-/mfn/unshipped"]/h4/span[@class="myo-spa-highlight"]'))) # /h4/span.myo-spa-highlight')
        # driver.implicitly_wait(2)
        ActionChains(driver).move_to_element(o).perform()
        print("o text :",o.text)
        n = o.text
        print('n : ', n)
        n = n.replace('Unshipped','')
        n = n.strip()
        if n.isdigit():
            i = int(n)
            print('# of orders: ',i)
            if i > 0: 
                hasOrders = True
    else:
        print('pb... not in orders page !')
        return

    global address
    if hasOrders:
        # list up all orders...
    #     table =  driver.find_element_by_xpath("//table[@class='datadisplaytable']")
    #     for row in table.find_elements_by_xpath(".//tr"):
    # print([td.text for td in row.find_elements_by_xpath(".//td[@class='dddefault'][1]"])
        cur_win = driver.current_window_handle # get current/main window
        orders = driver.find_element_by_xpath('//table[@id="orders-table"]/tbody')
        for row in orders.find_elements_by_xpath('.//tr'):
            col = row.find_elements_by_xpath('.//td')
            a = col[2].find_element_by_xpath('.//div/div/a')
            # print(a.get_attribute('outerHTML'))
            # a.click()
            # https://gist.github.com/lrhache/7686903            
            a.send_keys(Keys.CONTROL + Keys.RETURN)
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

            win_handles = driver.window_handles
            if len(win_handles) > 2:
                print('pb win_handles')
            for win in win_handles:
                if win != cur_win:
                    driver.switch_to_window(win) # switch to new window
                    a = driver.find_element_by_xpath('//div[@data-test-id="shipping-section-buyer-address"]')
                    # print(a.text)
                    add = process_amz_address(a)
                    # add other parameters 
                    # 1. order #
                    order_number = 'XXX'
                    add = order_number + ',' + add
                    # 2. date
                    add = datetime.today().strftime('%Y-%m-%d') + ',' + add
                    print(add)
                    address.append(add) 
                    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                    driver.close()

            driver.switch_to_window(cur_win) # switch back to main window

    # save addresses
    saveAddresses()
    
    # logout
    try:
        # b = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//li[@class="sc-logout-quicklink"]')))
        # action.move_to_element(b).perform()
        action = ActionChains(driver)
        a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//li[@id="sc-quicklink-settings"]')))
        action.move_to_element(a).perform()
        b = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//li[@class="sc-logout-quicklink"]')))
        action.move_to_element(b).click(b).perform()
        # b.click()
    except:
        print('error logout')
    
    driver.close()

def process_amz_address(adr) -> str :
    # supposed to be only list of span
    add = ''
    for a in adr.find_elements_by_xpath('.//*'):
        s = a.text.strip('\n')
        # print('s ', s, len(s))
        if len(s) > 0:
            add = add + s + ','
    add = add[:-1]
    # print('>>> ',add)
    return add

def saveAddresses():
    global address
    f = open(r'.\adresses_amz.txt','w',encoding='utf-8') 
    for s in address:
        f.write("%s\n" % s)
    f.close()
    return

def setCookies() -> dict:

    # get cookies from normal firefox ?
    f = open(r'E:\Dev\web\scraping\amz\seller_amz_cookies.txt','rb') 
    allCookies = pickle.load(f)
    f.close()
    return allCookies

def getCookies() -> dict:
    print('>>> get cookies')
    allCookies = driver.get_cookies()
    f = open(r'E:\Dev\web\scraping\amz\seller_amz_cookies.txt','wb') 
    pickle.dump( allCookies , f)
    f.close()
    return allCookies

# logout
def logout_ymt():
    global driver

    try:
        action = ActionChains(driver)
        a = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,'//body/header[@id="header"]/ul/li')))
        # print(a.get_attribute('innerHTML'))
        for b in a:
            print(b.get_attribute('innerHTML'))
            if 'ログアウト' in b.text:
                print('got logout') 
                action.move_to_element(b).click(b).perform()
                driver.implicitly_wait(5)
                driver.close()
                return
    except:
        print('error logout')
        return

# enter addresses in Yamato
def ymt():

    global driver

    login_page = 'https://cmypage.kuronekoyamato.co.jp/portal/entrance?id=kojintop'
    driver.get(login_page)

    # need to do proper login, suppose now that id is in cache
    try:
        b = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
        print(b.text)
        if 'ログイン' in b.text:
            print('got YMT login page')
            # ActionChains(driver).move_to_element(b).perform()
            b.click()
            # got new window ?
            a = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="right"]/ul/li')))
            for p in a:
                if 'アドレス帳' in p.text:
                    print('got アドレス帳')
                    ActionChains(driver).move_to_element(p).perform()
                    p.click()
                    c = driver.find_element_by_xpath('//a[@id="button_regist"]')
                    print(c.text)
                    c.click()
                    # TO DO here !!
                    ymt_enter_address()
                    break
    except:
        print('error YMT')

    logout_ymt()
    return

def ymt_enter_address():
    return

if __name__ == '__main__':
    # amz()
    ymt()