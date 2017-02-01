from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import sys
import copy

def kor_sentence(p):
    temp=""
    st=[]
    start = 0
    finish = 0
    s_start=0
    s_finish=0
    prev=""

    for z in range(len(p)):

              if z==0 and p[z]=="\"" or p[z]=="“":
                       temp=temp+p[z]
                       start=1
                       continue
              elif z==0:
                       temp=temp+p[z]
                       continue
                
              elif z>0:
                       prev=p[z-1]


              # next word
              if z==len(p)-1:
                       next_word=""
              else:
                       next_word=p[z+1]


              # double quotes beginning and ending
              if p[z]=="\"":
                      if start==1:
                          finish=1
                      else:
                          start=1

              elif p[z]=="“":
                      start=1
                  
              elif p[z]=="”" and start==1:
                      finish=1


              # single quotes beginning and ending 
              if p[z]=="\'":
                      if s_start==1:
                          s_finish=1
                      else:
                          s_start=1
              elif p[z]=="‘":
                      s_start=1

              elif p[z]=="’" and s_start==1:
                      s_finish=1

                      
               # separate sentences
              if p[z]=="." or p[z]=="!" or p[z]=="?":
                      if prev=="가" or prev== "나" or prev== "다" or prev== "라" or prev== "까" or prev== "지" or prev== "요" or prev=="죠" or prev=="임" or prev=="음" or prev=="함" or prev=="오":
                              if start==1 and finish==0:
                                      temp=temp+p[z]

                              elif start==1 and finish==1:
                                      if next_word=="":
                                              temp=temp+p[z]+"\n"
                                              st.append(temp)
                                              temp=""
                                              start=0
                                              finish=0

                                      elif next_word!=" " and next_word!="\n":
                                              temp=temp+p[z]

                                      elif next_word==" " or next_word=="\n":
                                              temp=temp+p[z]+"\n"
                                              st.append(temp)
                                              temp=""
                                              start=0
                                              finish=0

                              
                              #single case
                              elif s_start==1 and s_finish==0:
                                      temp=temp+p[z]
                        
                              elif s_start==1 and s_finish==1:
                                      if next_word=="":
                                              temp=temp+p[z]+"\n"
                                              st.append(temp)
                                              temp=""
                                              s_start=0
                                              s_finish=0

                                      elif next_word!=" " and next_word!="\n":
                                              temp=temp+p[z]
                           
                        
                                      elif next_word==" " or next_word=="\n":
                                              temp=temp+p[z]+"\n"
                                              st.append(temp)
                                              temp=""
                                              s_start=0
                                              s_finish=0

                              else:
                                      temp=temp+p[z]+"\n"
                                      st.append(temp)
                                      temp=""
                                      start=0
                                      finish=0

                      elif prev==")":
                              if p[z-2]=="다" or p[z-2]=="나" or p[z-2]=="가" or p[z-2]=="라" or p[z-2]=="까" or p[z-2]=="지"or p[z-2]=="요"or p[z-2]=="죠" or p[z-2]=="임" or p[z-2]=="음" or p[z-2]=="함" or p[z-2]=="오":
                                      temp=temp+p[z]+"\n"
                                      st.append(temp)
                                      temp=""
                                      start=0
                                      finish=0

                      else:
                              temp=temp+p[z]

              else:
                     temp=temp+p[z]                  

    for index in range(len(st)):
       ct=0
       for w in range(len(st[index])):

           if st[index][w]==" " or st[index][w]=="\n":
               ct=ct+1
           else:
               break

       st[index]=st[index][ct:len(st[index])]


    return st                 
