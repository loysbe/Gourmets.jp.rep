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


options = webdriver.ChromeOptions() 
# options.add_argument('user-data-dir=C:\\Users\\Loys\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #Path to your chrome profile
options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1")
driver = webdriver.Chrome(executable_path="C:\\Loys\\Google drive - ltd-japon\\Dev\\web\\Chrome\\chromedriver.exe", chrome_options=options)

url = "https://www.int-mypage.post.japanpost.jp/mypage/M010000.do"

driver.get(url)

print('poi')