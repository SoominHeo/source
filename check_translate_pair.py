# -*- coding: utf-8 -*-
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import sys
from urllib import parse
import zss
import re

def check_translate_pair(sources_k):
    l = sources_k.findAll('a',attrs={'accesskey':'t'})
    s = str(l[0]).split(' ')
    url = "https://ko.wikipedia.org"+str(s[2][6:-1])
    try:
        address = urlopen(url)
    except:
        return 0
    sor = BeautifulSoup(address,"html.parser")
    b_list = sor.findAll('b')
    
    
    for x in b_list:
        if(str(x).find("title=\"en:\"")!=-1):
            return 1
            break
    return 0
