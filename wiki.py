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
import metric
cnt = 40




def save_list(newlist,csv):
    for x in newlist:
        s=x.split(' ')
        url=""
        title=""
        for y in s:
            if(y[0:5]=="href="):
                url = "https://ko.wikipedia.org"+y[6:len(y)-1]
    
        s=x.split('"')
        nextistitle=0
        for y in s:
            if(nextistitle==1):
                title=y
                break;
            if(y[len(y)-6:]=="title="):
                nextistitle=1
                continue;
        now = time.localtime()
        tt = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        save_csv(url,title,tt,csv)
    if(url=="https://ko.wikipedia.org/wiki/%F0%9F%98%BC"):
        return -1

    return 1

def save_csv(url,title,tt,csv):
    print(str(url)+",\t"+str(title)+",\t"+str(tt)+"\n")
    csv.write(str(url)+",\t"+str(title)+",\t"+str(tt)+"\n")

def make_list_csv():
    csv = open("urlindex.csv","w",encoding='UTF8')
    nexturl = 'https://ko.wikipedia.org/w/index.php?title=%ED%8A%B9%EC%88%98:%EB%AA%A8%EB%93%A0%EB%AC%B8%EC%84%9C&from=%21';

    i=0
    tmp=nexturl
    chk=0

    while 1:
        print(str(i)+ " page")
        i+=1
        if(chk==1):
            chk=0
        if(chk==2):
            chk=0
        try:
            address = urlopen(nexturl)
            sources = BeautifulSoup(address,"html.parser")
            list_audio = sources.findAll('li')
            next = sources.findAll('div',attrs={'class':'mw-allpages-nav'})
            if(next==-1):
                break;
        except:
            print("ERROR")
            chk=2
            continue

        for x in next:
            d = str(x).split('|')
            s = str(x).split(' ')
            if(len(d)==1):
                for y in s:
                    if(y[0:5]=="href="):
                        d = y[6:len(y)-1].replace("amp;","")
                        tmp=nexturl
                        nexturl = 'https://ko.wikipedia.org'+d
                        break;

            if(len(d)==2):
                dd = 0
                for y in s:
                    if(y[0:5]=="href=" and dd==0):
                        dd=1
                        continue
                    elif(y[0:5]=="href=" and dd==1):
                        print("next")
                        dd=0
                        d = y[6:len(y)-1].replace("amp;","")
                        tmp=nexturl
                        nexturl = 'https://ko.wikipedia.org'+d
                        break;
                            
        newlist = []
        for x in list_audio:
            if(str(x).find('pt-anonuserpage')<0):
                newlist.append(str(x))
            else:
                break;
    
        if(save_list(newlist,csv)==-1):
            break;
    csv.close()

def readcsv():
    f = open("500.csv","r",encoding='UTF8')
    return f


def script(list_audio,source):
    global cnt
    for x in list_audio:
        s = str(x).split(' ')
        for y in s:
            if(y[0:5]=="href="):
                try:
                    englishURL = urlopen(y[6:len(y)-1])
                    sourcesENG = BeautifulSoup(englishURL,"html.parser")
                    kor_file = open("kor/kor_"+str(cnt)+".txt","w",encoding='UTF8')
                    eng_file = open("eng/eng_"+str(cnt)+".txt","w",encoding='UTF8')
                    kor_file.write(str(source))
                    eng_file.write(str(sourcesENG))
                    kor_file.close()
                    eng_file.close()
                    print(str(cnt)+"\n")
                    cnt += 1
                except:
                    break;



def cro():
    f = readcsv();
    while 1:
        line = f.readline()
        if not line: break
        print(line)
        s = line.split(',\t')
        try:
            address = urlopen(s[0])
        except:
            print("URL_OPEN_ERROR!")
            continue
        sources = BeautifulSoup(address,"html.parser")
        list_audio = sources.findAll('a',attrs={'lang':'en'})
        if(len(list_audio)==1):
            script(list_audio,sources)


def pair():
    f = readcsv();
    p = open("pair.csv","w",encoding='UTF8')
    while 1:
        line = f.readline()
        if not line: break
        s = line.split(',\t')
        try:
            address = urlopen(s[0])
        except:
            print("URL_OPEN_ERROR!")
            continue
        sources = BeautifulSoup(address,"html.parser")
        list_audio = sources.findAll('a',attrs={'lang':'en'})
        if(len(list_audio)==1):
            for x in list_audio:
                d = str(x).split(' ')
                for y in d:
                    if(y[0:5]=="href="):
                        try:
                            url=parse.unquote(y[6:len(y)-1])
                            t=url.split('/')
                            print(s[0]+",\t"+str(y[6:len(y)-1])+",\t"+s[1]+",\t"+str(t[-1])+"\n")
                            p.write(s[0]+",\t"+str(y[6:len(y)-1])+",\t"+s[1]+",\t"+str(t[-1])+"\n")
                        except:
                            break;
    p.close()


        
        

def check_all_pair():
    f = open("New_Random_Sample_382.csv","w")
    a = 0
    while 1:
        #print(a)

        try:
            k = open("dd/new random/kor/kor_"+str(a)+".txt","r",encoding='UTF8')
            sources_k = BeautifulSoup(k,"html.parser")
            e = open("dd/new random/eng/eng_"+str(a)+".txt","r",encoding='UTF8')
            sources_e = BeautifulSoup(e,"html.parser")

            t1=reference.reference(sources_k,sources_e)
            t2=tree_compare.tree_compare(sources_k,sources_e)
            t3=photo_check.photo_check(sources_k,sources_e)
            t4=check_translate_pair.check_translate_pair(sources_k)
            t5=paragraph.paragraph(sources_k,sources_e)
            t6=reading.reading(sources_k,sources_e)
        
            final_result=metric.metric(t1,t2 ,t3 ,t4 ,t5 ,t6) 

            print("["+str(a)+"]",round(final_result,2))
            f.write(str(t1)+","+str(t2)+","+str(t3)+","+str(t4)+","+str(t5)+","+str(t6)+","+str(final_result)+"\n")
            a=a+1
        except:
            break


    f.close()


#make_list_csv()
#pair()
#cro()
check_all_pair()

