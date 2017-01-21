from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import sys
import copy


def photo_check(sources_ko,sources_en):
    
     photo_1=sources_ko.findAll('a',attrs={'class':'internal'})
     photo_2=sources_ko.findAll('a',attrs={'class':'image'})
     
     photo_address_ko=[]
     for x in range(len(photo_1)):
         tmp=str(photo_1[x]).split('href="')
         tmp[1]=tmp[1].upper()
         if( tmp[1].find('.JPG')>0 or
             tmp[1].find('.PNG')>0 or
             tmp[1].find('.SVG')>0 or
             tmp[1].find('.JPEG')>0 or
             tmp[1].find('.OGV')>0 ):

             tmp2=tmp[1].split('"')
             tmp3=tmp2[0].split(':')
             
             if len(tmp3[1])==0 or tmp3[1]=='COMMONS-LOGO.SVG':
                  continue
             photo_address_ko.append(tmp3[1])
             
     
     for x in range(len(photo_2)):
         tmp=str(photo_2[x]).split('href="')
         tmp[1]=tmp[1].upper()
         if( tmp[1].find('.JPG')>0 or
             tmp[1].find('.PNG')>0 or
             tmp[1].find('.SVG')>0 or
             tmp[1].find('.JPEG')>0 or
             tmp[1].find('.OGV')>0 ):

             tmp2=tmp[1].split('"')
             tmp3=tmp2[0].split(':')

             if len(tmp3[1])==0 or tmp3[1]=='COMMONS-LOGO.SVG':
                  continue
             if tmp3[1] not in photo_address_ko:
                  photo_address_ko.append(tmp3[1])

     
     photo_en_1=sources_en.findAll('a',attrs={'class':'internal'})
     photo_en_2=sources_en.findAll('a',attrs={'class':'image'})                         

     photo_address_en=[]
     for x in range(len(photo_en_1)):
         tmp_e=str(photo_en_1[x]).split('href="')
         tmp_e[1]=tmp_e[1].upper()
         if( tmp_e[1].find('.JPG')>0 or
             tmp_e[1].find('.PNG')>0 or
             tmp_e[1].find('.SVG')>0 or
             tmp_e[1].find('.JPEG')>0 or
             tmp_e[1].find('.OGV')>0 ):

             tmp2_e=tmp_e[1].split('"')
             tmp3_e=tmp2_e[0].split(':')

             if (len(tmp3_e) == 1): continue
             if len(tmp3_e[1])==0 or tmp3_e[1]=='COMMONS-LOGO.SVG':
                  continue
             photo_address_en.append(tmp3_e[1])

     for x in range(len(photo_en_2)):
         tmp_e=str(photo_en_2[x]).split('href="')
         tmp_e[1]=tmp_e[1].upper()
         if( tmp_e[1].find('.JPG')>0 or
             tmp_e[1].find('.PNG')>0 or
             tmp_e[1].find('.SVG')>0 or
             tmp_e[1].find('.JPEG')>0 or
             tmp_e[1].find('.OGV')>0 ):

             tmp2_e=tmp_e[1].split('"')
             tmp3_e=tmp2_e[0].split(':')
             
             if len(tmp3_e[1])==0 or tmp3_e[1]=='COMMONS-LOGO.SVG':
                  continue
             if tmp3_e[1] not in photo_address_en:
                  photo_address_en.append(tmp3_e[1])
                  

     total=0
    
     for i in range(len(photo_address_ko)):
         for j in range(len(photo_address_en)):
             if photo_address_ko[i]==photo_address_en[j]:
                total=total+1
                
     

     if len(photo_address_ko)==0 and len(photo_address_en)==0 :
          result=-1
          return result 

     if len(photo_address_ko)>=len(photo_address_en):
          denominator=len(photo_address_en)
     else:
          denominator=len(photo_address_ko)
          
     numerator=total

     try:
          if denominator>5:
               if (numerator/denominator)>=0.8:
                    result=1
               else:
                    result=0
          else:
               if (numerator/denominator)>=0.6:
                    result=1
               else:
                    result=0
     except:
          result=0
          
     return result

             





