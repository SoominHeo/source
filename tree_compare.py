# -*- coding: utf-8 -*-
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import sys
from urllib import parse
import zss
import re

def extract_contents_structure(sources):
    lst = []
    list_audio = sources.findAll('span', attrs={'class':'tocnumber'})
    for i in list_audio:
        temp = re.split('>|<', str(i))
        lst.append(temp[2])
    return lst

def make_tree(list):
    root = zss.Node('root')
    kid1 = zss.Node('tmp')
    kid2 = zss.Node('tmp')
    kid3 = zss.Node('tmp')
    
    for x in list:
        l = len(x.split('.'))
        if(l==1):
            kid1 = zss.Node('1')
            root.addkid(kid1)
        elif(l==2):
            kid2 = zss.Node('2')
            kid1.addkid(kid2)
        elif(l==3):
            kid3 = zss.Node('3')
            kid2.addkid(kid3)
    
    return root

def tree_compare(sources_k,sources_e):
    list_k = extract_contents_structure(sources_k)
    A = make_tree(list_k)
    list_e = extract_contents_structure(sources_e)
    B = make_tree(list_e)
    if(( len(list_k)+len(list_e) )/2==0):
        return -1
    if(zss.simple_distance(A,B)/(( len(list_k)+len(list_e) )/2)<0.6):
        return 1
    else:
        return 0
    
