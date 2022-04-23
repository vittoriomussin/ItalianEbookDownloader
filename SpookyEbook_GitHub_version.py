from threading import Condition
from queue import Queue
import random
from bs4 import BeautifulSoup
import certifi
from urllib3 import ProxyManager, make_headers
import os
import requests
from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.by import By
from epub_conversion.utils import open_book, convert_epub_to_lines
#-----------------------------for webdriver-----------------------------------
import threading
from fake_useragent import UserAgent
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import zipfile
import speedtest

#-----------------------------------auxiliary functions--------------------------------------------
def removepunct(x):
    punct = """, ; . : _ - " " < > ! ' ' £ $ % & / ( ) = ? ^ | * § ° """.split()
    for i in punct:
        x = x.replace(i, "")
    return x


def removeextraspaces(x):
    a = x.split()
    ritorno = " ".join(a)
    return ritorno


def ausialiaria(x):
    titolo = ""
    T = x.split(" ")
    for t in T:
        if t == "by":
            return titolo
        titolo = titolo + " " + t

def testinternet(link):
    try:
        r=requests.get(link)
    except:
        valore=False
    else:
        valore=True
    return valore
#------------------------------------
class SpookyEbook:
    def __init__(self, filtro):
        self.lock = Condition()
        self.anno=filtro
        self.libri = []
        with open("link_not_found_register.txt", 'a') as f:
            f.write("")
        self.link_not_found_register=""
        # initializing directory
        arr = os.listdir(r"C:\Users\vittorio\CHRONEBOOKS\20\epubs_20")
        directory = ""
        for i in arr:
            directory = directory + " " + i
        directory = directory.replace("Ã¬", "ì").replace("Ã¹", "ù").replace("Ã¨","è").replace("Ã²", "ò").replace("Ã", "à")
        directory = removepunct(directory)
        directory = removeextraspaces(directory)
        # initializing ebook file
        #da sostituire prendendo i links da ebookspy_links.txt
        with open("ebookspy_links.txt", 'r') as f:
            lines = f.readlines()
            for i in lines:
                if self.anno in i:
                    libro =i.split(";")[1]
                    x = i.split(";")[0].replace("Ã¬", "ì").replace("Ã¹", "ù").replace("Ã¨", "è").replace("Ã²", "ò").replace("Ã", "à")
                    titolo=ausialiaria(x)
                    try:
                        titolo = removepunct(titolo)
                    except AttributeError:
                        pass
                    else:
                        titolo = removeextraspaces(titolo)
                        if titolo not in directory:
                            self.libri.append(libro)
            print(len(self.libri))

    def spooky_pop(self):
        self.lock.acquire()
        l=self.libri.pop(0)
        self.lock.release()
        return l
    
    def write_link_not_found_register(self, l):
        self.lock.acquire()
        with open("link_not_found_register.txt", 'a') as f:
            w=str(l)+"\n"
            f.write(w)
        self.lock.release()
    
    def read_link_not_found_register(self):
        self.lock.acquire()
        with open("link_not_found_register.txt", 'r') as f:
            lines = f.readlines()
            for i in lines:
                self.link_not_found_register=self.link_not_found_register + i + "\n"
        self.lock.release()

#def ebookspy():
#    pass

#def zlibrary():
#    pass
#    #/html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a
    
#-------------------------------------------web driver thread--------------------------------------------
class EbookDownloader(threading.Thread):
    def __init__(self, SpookyEbook):
        threading.Thread.__init__(self)
        self.p = SpookyEbook

    def run(self):
        rete=0
        self.p.read_link_not_found_register()
        while True:
            if rete>5:
                print("Rete non disponibile, aspetto 5 minuti")
                time.sleep(300)
            #time.sleep(20)
            a = "https://ebookspy.com/" + self.p.spooky_pop()
            if a in self.p.link_not_found_register:
                print("Link non trovato, già presente nel registro")
                continue
            print("EbookDownloader ha preso 1 link; n° di link rimasti:", len(self.p.libri))
            
            #-------------------------------------webdriver initialization------------------------------------------------------
            options = webdriver.ChromeOptions()
            options.add_argument("window-size=1280,800")  # ("start-maximized")#("--window-size=1100,1000") do not
            # create unique instances rotate User Agent?, do not, to avoid unique UserAgent-screen instances ua =
            # UserAgent() userAgent = ua.random options.add_argument(f'user-agent={userAgent}')
            options.add_argument("--user-data-dir=C:/Users/vittorio/AppData/Local/Google/Chrome/User Data/Profile 2")
            options.add_argument("--disable-extensions")
            # Remove Navigator.Webdriver Flag
            options.add_argument("--disable-blink-features")
            options.add_argument('--disable-blink-features=AutomationControlled')
            #Setting the default download directory
            preferences = {"download.default_directory": r"C:\Users\vittorio\CHRONEBOOKS\20\epubs_20"}
            options.add_experimental_option("prefs", preferences)
            # Exclude the collection of enable-automation switches
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            #Turn-off useAutomationExtension
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(executable_path=r"C:\Users\vittorio\ebookSoup\chromedriver.exe", options=options)
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
            
            #-------------------------------------webdriver actions---------------------------------------------------------
            # make a realistic page flow
            if testinternet("https://www.google.com/")==False:
                print("Rete non disponibile")
                rete+=1
                driver.quit()
                continue
            driver.get("https://www.google.com/")
            time.sleep(random.randint(1, 3) + random.random())
            
            # visiting the website's home
            if testinternet("https://ebookspy.com/")==False:
                print("Rete non disponibile")
                rete+=1
                driver.quit()
                continue
            driver.get("https://ebookspy.com/")
            time.sleep(random.randint(1, 3) + random.random())
                    
            # visiting the page of the ebook
            if testinternet(a)==False:
                print("Rete non disponibile")
                rete+=1
                driver.quit()
                continue
            driver.get(a)
            time.sleep(random.randint(1, 3) + random.random())
            html_0 = driver.page_source
            soup = BeautifulSoup(html_0, 'html.parser')
            b=""
            for anchor in soup.find_all("a"):
                if anchor.get_text()[-5:]==".epub":
                    b=anchor.get("href")
            
            # visiting the download page of the ebook
            if b=="":
                print("Link non trovato")
                self.p.write_link_not_found_register(a)
                driver.quit()
                continue
            if testinternet(b)==False:
                print("Rete non disponibile")
                rete+=1
                driver.quit()
                continue
            driver.get(b)
            time.sleep(random.randint(1, 3) + random.random())
            html = driver.page_source
            time.sleep(random.randint(1, 3) + random.random())
            soup = BeautifulSoup(html, 'html.parser')
            time.sleep(random.randint(1, 3) + random.random())
            tempo = int(soup.find("span", {"id": "s1r0xd"}).get_text()) + random.random() + 1
            before= datetime.datetime.now()
            wifi  = speedtest.Speedtest()
            internet_download=wifi.download()/1000000 - 1.5
            tempo_da_sottrarre=datetime.datetime.now()-before
            time.sleep(tempo-tempo_da_sottrarre.total_seconds())
            bottone = driver.find_element_by_id('btn_download')
            time.sleep(random.randint(1, 3) + random.random())
            bottone.click()
            print("1 ebook scaricato")
            valore=(int(soup.find("small").get_text()[1:-7])/125000)/internet_download
            quiete= valore+ random.random() + 1
            time.sleep(quiete)
            driver.quit()

#-----------------------------------------main------------------------------------------------


if __name__=="__main__":
    m = SpookyEbook(";202")
    print("Programma avviato")
    a = EbookDownloader(m)
    a.start()
    a.join()
    print("Programma terminato")