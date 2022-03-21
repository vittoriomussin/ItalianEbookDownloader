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
from selenium.webdriver.common.by import By
from epub_conversion.utils import open_book, convert_epub_to_lines


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


class SpookyEbook:
    def __init__(self, anno):
        self.lock = Condition()
        self.Proxies = ["85.208.127.54:12323","85.208.127.19:12323", "85.208.126.157:12323", "85.208.126.183:12323", "85.208.125.147:12323"]
        self.proxyuserpass="14a3ba81d0340:fd8e75877c"
        self.anno=anno
        self.libri = []
        # initializing directory
        arr = os.listdir(r"C:\Users\vittorio\CHRONEBOOKS\20\epubs_20")
        directory = ""
        for i in arr:
            directory = directory + " " + i
        directory = directory.replace("Ã¬", "ì").replace("Ã¹", "ù").replace("Ã¨","è").replace("Ã²", "ò").replace("Ã", "à")
        directory = removepunct(directory)
        directory = removeextraspaces(directory)
        # initializing ebook file
        with open("epubs_20.txt", 'r') as f:
            lines = f.readlines()
            for i in lines:
                libro =(i.split(";")[1],i.split(";")[-1])
                x = i.split(";")[0].replace("Ã¬", "ì").replace("Ã¹", "ù").replace("Ã¨", "è").replace("Ã²", "ò").replace("Ã", "à")
                titolo = ausialiaria(x)
                titolo = removepunct(titolo)
                titolo = removeextraspaces(titolo)
                if titolo not in directory:
                    self.libri.append(libro)
        print(len(self.libri))

    def spooky_pop(self):
        self.lock.acquire()
        l=self.libri.pop(0)
        self.lock.release()
        return l

    def spooky_epub2text(self, e):
        self.lock.acquire()
        book = open_book(e)
        lines = convert_epub_to_lines(book)
        testo = ""
        for line in lines:
            if "<p>" in line and "<br />" not in line and "&nbsp;" not in line:
                testo = testo + line.replace("<p>", "").replace("</p>", "")
        path = r"C:\Users\vittorio\ebookSoup\txts_anni80" + "\\" + e[34:-5] + ".txt"
        with open(path, 'w', encoding="utf8") as f:
            f.write(testo)
        self.lock.release()
