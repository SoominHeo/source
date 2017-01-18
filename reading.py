#!/usr/bin/python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen

def reading(sources_k, sources_e):
    list_audio = sources_k.findAll('ul')
    list_audio_e = sources_e.findAll('ul')

    nk=0
    ne=0
    for i in list_audio:
        list_citation = i.findAll('cite', attrs={'class': 'citation'})
        nk = nk + len(list_citation)

    for j in list_audio_e:
        list_citation_e = j.findAll('cite', attrs={'class': 'citation'})
        ne = ne + len(list_citation_e)

    #print("reading: "+str(nk) + "/" + str(ne))

    percent = int(nk * 0.4)
    if ((nk == 0) or (ne == 0)):
        return -1
    if(abs(nk - ne) <= percent):
        return 1
    return 0
