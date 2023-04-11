from selenium import webdriver
# from selenium.webdriver.chrome.options import Options as SeleniumOptions
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement
import re

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
kuroneko_pwd = 'xxxx'

def connectToYMT():
    driver.get("https://cmypage.kuronekoyamato.co.jp/portal/entrance")
    try:
        # enter mot de passe        
        k_id = driver.find_element_by_xpath('//input[@id="kuroneko_id"]')
        k_id.clear()
        k_id.send_keys(kuroneko_id)

        # enter mot de passe        
        pwd = driver.find_element_by_xpath('//input[@type="password"]')
        pwd.send_keys(kuroneko_pwd)

        o = driver.find_element_by_xpath('//button[@type="submit"]')
        o.click()

        a = driver.find_element_by_xpath('//a/p[contains(text(), "アドレス帳")]')
        a.click()
    except NoSuchElementException:
        print('erreur connexion YMT')

    return


if __name__ == '__main__':
    URL = 'https://sp-send.kuronekoyamato.co.jp/smpTaqWeb/Viwb1010Action_doInit.action'
    URL = 'https://www.rakuten.co.jp'
    driver.get(URL)
    try:
        o = driver.find_element_by_xpath('//*')
        # print(o.get_attribute('outerHTML'))
        # print(o.get_attribute('innerHTML'))
    except NoSuchElementException:
        print('error')

    # seems ok
    a = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//a[@id="portalEntrance"]')))
    a.click()

    print('fin')