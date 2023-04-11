import sys
sys.path.append(".")
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

# if firefox: 
#     # fp = webdriver.FirefoxProfile('C:/Users/Loys/AppData/Roaming/Mozilla/Firefox/Profiles/ax8azgih.default')
#     # driver = webdriver.Firefox(firefox_profile=fp)  C:\Loys\Google drive - ltd-japon\Dev\web\Gekco
#     driver = webdriver.Firefox(executable_path="C:\\g-drive-LTD\\Dev\\web\\Gekco\\geckodriver.exe")
# else:
#     options = webdriver.ChromeOptions() 
#     options.add_argument('user-data-dir=C:\\Users\\Loys\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #Path to your chrome profile
#     driver = webdriver.Chrome(executable_path="C:\\g-drive-LTD\\Dev\\web\\Chrome\\chromedriver.exe", chrome_options=options)

# simple routine to log to a protected site
def connect_to_site(user_glogin,mdp) -> bool:

    driver.get("https://glogin.rms.rakuten.co.jp/")
    try:
        # entrer le mot de passe
        user = driver.find_element_by_xpath('//input[@id="rlogin-username-ja"]')
        user.send_keys(user_glogin)    
        pwd = driver.find_element_by_xpath('//input[@id="rlogin-password-ja"]')
        pwd.send_keys(mdp)
        o = driver.find_element_by_xpath('//button[@name="submit"]')
        o.click()
    except NoSuchElementException:
        print('Erreur de connexion')
        return False

    return True

import requests
def get_company_data(siren,type_donnees):

    # return data is jason
    # https://api.lasocietenouvelle.org/ 

    if type_donnees == "empreinte":
        URL = "https://api.lasocietenouvelle.org/legalunitfootprint/" + siren
        # PARAMS = {'address':location}
        # r = requests.get(url = URL, params = PARAMS)
        r = requests.get(url = URL)
    elif type_donnees == "Données par défaut":
        URL = "https://api.lasocietenouvelle.org/defaultfootprint/?code={code}&aggregate={aggregate}&area={area} "
    elif type_donnees == "Série de données":
        URL = "https://api.lasocietenouvelle.org/serie/{ID Serie}/?code={code}&aggregate={aggregate}&area={area}"
    
# Retourne les valeurs par défaut proposées à partir de la zone économique (area) et 
# l'activité principale (code), et pour l'agrégat souhaité (aggregate)
# GET /defaultfootprint/?code={code}&aggregate={aggregate}&area={area}

# Série de données 
# GET /serie/{ID Serie}/?code={code}&aggregate={aggregate}&area={area}

    return r.json()
   
import json
def print_jason(data):
    json_formatted_str = json.dumps(data, indent=2)
    print(json_formatted_str)
    return


if __name__ == '__main__':
# do something
    siren = "784671695"
    type_donnees = "empreinte"
    print_jason(get_company_data(siren,type_donnees))

    # if ( connect_to_site("","") ):
        
    # else:
        # exit
