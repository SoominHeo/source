#!/usr/bin/python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen

def reference(sources_k, sources_e):
    list_audio = sources_k.findAll('cite', attrs={'class':'citation'})
    cite_num_korean = len(list_audio)

    list_english = sources_e.findAll('cite', attrs={'class': 'citation'})
    cite_num_english = len(list_english)

    percent = int(cite_num_korean * 0.3)

    if ((cite_num_korean == 0) or (cite_num_english == 0)):
        return -1

    if(abs(cite_num_korean - cite_num_english) <= percent):
        return 1
    return 0