from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

options = webdriver.ChromeOptions() 
options.add_argument('user-data-dir=C:\\Users\\Loys\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #Path to your chrome profile
driver = webdriver.Chrome(executable_path="E:\\Google drive - ltd-japon\\Dev\\web\\Chrome\\chromedriver.exe", chrome_options=options)

url = 'https://www.amazon.co.jp/'

# param = '鴨+フォアグラ'
# param = 'リエット+ド+カナール'
# param = 'ムース+ド+フォアグラ'
param = 'パテ'

url_param = 's?k='+ param + '&i=food-beverage'

file_name = r'.\review_seeking\reviews_amz[' + param + '].txt' 

f = open(file_name,'w',encoding='utf-8') 

def crawl_amz_products():
    global f

    driver.get(url+url_param)
    WebDriverWait(driver, 10)

    try:
        products = driver.find_elements_by_xpath('//div[@data-asin]') #contains(@data-asin,[A-Z0-9]+)]') #"

        s = '==> '+ str(len(products)) + ' products in the page'
        print(s)
        f.write("%s\n" % s)

        for p in products:
            asin = p.get_attribute('data-asin')
            if (asin == ''):
                continue
            s = 'product : ' + asin
            print(s)
            f.write("%s\n" % s)
            # print(p.get_attribute('outerHTML'))  
            # check if review exists
            try:
                review = p.find_element_by_xpath('.//a[contains(@href,"customerReviews")]')
                # print(review.get_attribute('outerHTML'))
                s = 'nbre de reviews : ' + review.find_element_by_xpath('.//span').text
                print(s)
                f.write("%s\n" % s)
                get_amz_review(review)
            except NoSuchElementException:
                s = 'pas de review'
                print(s)
                f.write("%s\n" % s)

    except NoSuchElementException:
        s = 'error'
        print(s)
        f.write("%s\n" % s)

    f.close()

    return

def get_amz_review(r):
    r.click()
    
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    new_win = driver.window_handles
    # print(len(new_win))
    # print(new_win[0],new_win[1])
    # https://stackoverflow.com/questions/53690243/selenium-switch-tabs
    driver.switch_to.window(new_win[1])
    WebDriverWait(driver, 20).until(EC.title_contains("Amazon"))

    try:

        product_title = driver.find_element_by_xpath('.//h1[@id="title"]')
        s = 'Title : ' + product_title.text
        print(s)
        f.write("%s\n" % s)

        try:
            price = driver.find_element_by_xpath('//span[@id="price_inside_buybox"]')
            s = price.text
            print(s)
            f.write("%s\n" % s)
        except NoSuchElementException:  
            try:
                price = driver.find_element_by_xpath('//span[@class="a-color-price"]')
                s = price.text
                print(s)
                f.write("%s\n" % s)
            except NoSuchElementException:
                pass
        
        try:
            feature_bullets = driver.find_element_by_xpath('//div[@id="feature-bullets"]')
            s = 'Feature list : ' + feature_bullets.text
            print(s)
            f.write("%s\n" % s)
        except NoSuchElementException:
            pass
        
        try:
            n = driver.find_element_by_xpath('//span[contains(text(), "まだカスタマーレビューはありません")]')
            s = 'pas de commentaires...'
            print(s)
            f.write("%s\n" % s)

        except NoSuchElementException:
        
            a = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//a[contains(text(), "日本からのレビューをすべて見る")]')))
            a.click()
            # WebDriverWait(driver, 20)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[contains(@id,"customer_review-")]')))
            review_data = driver.find_elements_by_xpath('//div[contains(@id,"customer_review-")]')
            # s = '# of comments ', len(review_data))
            i = 1
            for r in review_data:
                s = '\n Review '+ str(i)
                print(s)
                f.write("%s\n" % s)
                try:
                    text = r.find_element_by_xpath('.//div/span[contains(@class,"review-text-content")]')
                except NoSuchElementException:
                    text = r.find_element_by_xpath('.//div[contains(@class,"review-text-content")]')
                s = text.text
                print(s)
                f.write("%s\n" % s)
                i += 1
    except NoSuchElementException:
        s = 'erreur get_amz_review'
        print(s)
        f.write("%s\n" % s)
    driver.close()   
    driver.switch_to.window(new_win[0])

    s = '\n ===================\n'
    print(s)
    f.write("%s\n" % s)

    return

if __name__ == '__main__':

    crawl_amz_products()