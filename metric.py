# -*- coding: utf-8 -*-
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import sys
from urllib import parse
import zss
import re
import photo_check
import paragraph
import reference
import reading
import tree_compare
import check_translate_pair



def metric( reference, tree_compare, photo_check, check_translate_pair, paragraph, reading ):

    item_list=[ [ reference, 0.255 ],
                [ tree_compare, 0.201 ],
                [ photo_check, 0.178 ],
                [ paragraph, 0.243 ],
                [ reading , 0.124 ] ]
    
    check_minus=[]
    minus_item=[]
    total=1
    
    if check_translate_pair==1:
        result=1

    else:
        sum=0
        for x in range(len(item_list)):
            if item_list[x][0]!=-1:
                sum=sum+(item_list[x][0]*item_list[x][1])

            else:
                minus_item.append(x)

    
        if len(minus_item)!=0:
            for i in range(len(minus_item)):
                for j in range(len(item_list)):
                    if minus_item[i]==j:
                        total=total-item_list[j][1]


        result= sum/total

    return result
