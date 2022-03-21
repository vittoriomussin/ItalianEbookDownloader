import threading
from threading import Condition
from queue import Queue
import random
from bs4 import BeautifulSoup
import certifi
from urllib3 import ProxyManager, make_headers
import os
import requests
from selenium import webdriver
#from seleniumwire import webdriver
import time
from selenium.webdriver.common.by import By
from epub_conversion.utils import open_book, convert_epub_to_lines
from fake_useragent import UserAgent
import undetected_chromedriver.v2 as uc

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import zipfile

class EbookDownloader(threading.Thread):
    def __init__(self, SpookyEbook):
        threading.Thread.__init__(self)
        self.p = SpookyEbook

    def run(self):
        while True:
            #time.sleep(20)
            a = self.p.spooky_pop()
            print("EbookDownloader ha preso 1 link; n° di link rimasti:", len(self.p.libri))
            
            options = webdriver.ChromeOptions()

            options.add_argument("window-size=1280,800")  # ("start-maximized")#("--window-size=1100,1000") do not
            # create unique instances rotate User Agent, do not, to avoid unique UserAgent-screen instances ua =
            # UserAgent() userAgent = ua.random options.add_argument(f'user-agent={userAgent}')

            options.add_argument("--user-data-dir=C:/Users/vittorio/AppData/Local/Google/Chrome/User Data/Profile 2")
            options.add_argument("--disable-extensions")

            # Remove Navigator.Webdriver Flag
            options.add_argument("--disable-blink-features")
            options.add_argument('--disable-blink-features=AutomationControlled')

            preferences = {"download.default_directory": r"C:\Users\vittorio\CHRONEBOOKS\20\epubs_20"}
            # Expired { "success": true,
            # "challenge_ts": "2022-03-09T13:35:34Z", "hostname": "it.tiny-files.com", "score": 0.3, "action": "/" }0.3
            options.add_experimental_option("prefs", preferences)

            # Exclude the collection of enable-automation switches
            options.add_experimental_option("excludeSwitches", ["enable-automation"])

            #Turn-off useAutomationExtension
            options.add_experimental_option('useAutomationExtension', False)
            
            
            driver = webdriver.Chrome(executable_path=r"C:\Users\vittorio\ebookSoup\chromedriver.exe", options=options)#seleniumwire_options=sel_w_options
            #driver = webdriver.Chrome(os.path.join(path, 'chromedriver'),options=options) #
            # Remove Navigator.Webdriver Flag on the run
            # browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") #not
            # necessary due to '--disable-blink-features=AutomationControlled' that works for ChromeDriver version
            # 79.0.3945.16 or over

            # set a common UserAgent driver.execute_cdp_cmd('Network.setUserAgentOverride', {"user-agent":
            # "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51
            # Safari/537.36"})

            # Change the property value of the navigator for webdriver to undefined
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")




            #----------------------------------------------make a realistic page flow
            #driver.get("https://www.google.com/")
            #time.sleep(random.randint(1, 3) + random.random())
            
            #----------------------------------------------visiting the website's home
            #driver.get("https://ebookspy.com/")
            #time.sleep(random.randint(1, 3) + random.random())
            
            #----------------------------------------------visiting the page of the ebook
            #driver.get(a[0])
            #time.sleep(random.randint(1, 3) + random.random())
            
            # visiting the download page of the ebook
            try:
                driver.get(a[1])
                time.sleep(random.randint(1, 3) + random.random())
                html = driver.page_source
                time.sleep(random.randint(1, 3) + random.random())
                soup = BeautifulSoup(html, 'html.parser')
                time.sleep(random.randint(1, 3) + random.random())
                valore=(int(soup.find("small").get_text()[1:-7])/125000)/8
                print(valore)
                tempo = int(soup.find("span", {"id": "s1r0xd"}).get_text()) + random.random() + 1
                time.sleep(tempo)
                bottone = driver.find_element_by_id('btn_download')
                time.sleep(random.randint(1, 3) + random.random())
                bottone.click()
                print("1 ebook scaricato")
                
                quiete= valore+ random.random() + 1

                #quiete = random.randint(30, 35) + random.random() #prima era da 4 a 7
                time.sleep(quiete)
                driver.quit()
            except:
                driver.quit()
