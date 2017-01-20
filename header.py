from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import sys
import copy

i=18
number = str(i)

def remove_tags(data):
    p=re.compile(r'<.*?>')
    return p.sub('', data)

def remove_span(data):
    p=re.compile(r'<span.*>.*?</span>')
    return p.sub('',data)

def remove_comma(data):
    result=data.replace("</p>, <p>"," ")
    
    for x in range(1,21):
        result=result.replace("["+str(x)+"]","")
        
    return result

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

def eng_sentence(final_header_eng):

    start=-1
    finish=-1
    cnt=0
    

    # '('로 시작해서 ')'까지 찾아서 제거
    
    x=0
    while 1:
        if x==len(final_header_eng):
            break
            
        start=final_header_eng[x].find('(')
        if start==-1:
            x=x+1
            continue
        
        finish=final_header_eng[x].find(')',start)
        if finish==-1:
            tmp=final_header_eng[x][start:len(final_header_eng[x])+1]
        else:
            tmp=final_header_eng[x][start:finish+1]

        final_header_eng[x]=final_header_eng[x].replace(tmp,'')
        start=final_header_eng[x].find('(')
            
        if start==-1:
            x=x+1
                
        finish=-1

    # ~~~')'까지 찾아서 제거
    for x in range(len(final_header_eng)):

        finish=final_header_eng[x].find(')')
        if finish==-1:
            continue
        
        tmp=final_header_eng[x][:finish+1]
        final_header_eng[x]=final_header_eng[x].replace(tmp,'')
        finish=-1

    # 공백이거나 '.'만 있는 라인제거
    
    for x in range(len(final_header_eng)):

        if final_header_eng[cnt]=='' or final_header_eng[cnt]=='.':
            del final_header_eng[cnt]
        else:
            cnt=cnt+1

        if len(final_header_eng)-1==cnt:
            break
            
    

    return final_header_eng
                
        
def header(sourcesKOR, sourcesENG,i):


    #저장된 한-영 HTML 받아오기
    '''
    f_kor=open("dd/dd/kor/kor_"+str(i)+".txt","r",encoding='UTF8')
    html_kor=f_kor.read()
    sourcesKOR = BeautifulSoup(html_kor,"html.parser")

    f_eng=open("dd/dd/eng/eng_"+str(i)+".txt","r",encoding='UTF8')
    html_eng=f_eng.read()
    sourcesENG = BeautifulSoup(html_eng,"html.parser")
    '''
    
    #샘플 한-영 HTML 받아오기
    '''
    f_kor=open("dd/kor/kor_"+str(i)+".txt","r",encoding='UTF8')
    html_kor=f_kor.read()
    sourcesKOR = BeautifulSoup(html_kor,"html.parser")

    f_eng=open("dd/eng/eng_"+str(i)+".txt","r",encoding='UTF8')
    html_eng=f_eng.read()
    sourcesENG = BeautifulSoup(html_eng,"html.parser")
    '''
    
   
    #쓸때 없는 table 부분 삭제
    bd_kor=str(sourcesKOR).find('</table>\n<p>')
    bd_eng=str(sourcesENG).find('</table>\n<p>')

    tmp_kor=str(sourcesKOR)
    tmp_eng=str(sourcesENG)
    
    tmp_kor=tmp_kor.replace(tmp_kor[:bd_kor+9],'')
    tmp_eng=tmp_eng.replace(tmp_eng[:bd_eng+9],'')
    
    sourcesKOR_tmp=BeautifulSoup(tmp_kor,"html.parser")
    sourcesENG_tmp=BeautifulSoup(tmp_eng,"html.parser")

   
    #문단 부분만 추출
    para_kor = sourcesKOR_tmp.findAll('p')
    para_eng = sourcesENG_tmp.findAll('p')

   
    #문단이 없으면 다음 문서로 넘어가기 
    if len(para_kor)==0 or len(para_eng)==0:
        i=i+1
        return -1
                
    #print("["+str(i)+"]")    

    #추출할 header를 저장하기 위한 파일오픈
    f_header_kor=open("dd/dd/kor_header/[header]kor_"+str(i)+".txt","w",encoding='UTF8')
    f_header_eng=open("dd/dd/eng_header/[header]eng_"+str(i)+".txt","w",encoding='UTF8')

       
    ####  KOREA  HEADER  ####
    #header만 추출 
    #print("[kor]")
    non_bmp_map=dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)
    kor_content_list=str(para_kor).translate(non_bmp_map).split("<p></p>")
    #kor_content_list="<p>".join(kor_content_list).split("</table>\n<p>")
    header_kor=remove_comma(str(kor_content_list[0]).translate(non_bmp_map))
    header_kor=remove_span(header_kor)
    header_kor=remove_tags(header_kor)
    if header_kor[len(header_kor)-2]==',':
        header_kor=header_kor[1:len(header_kor)-2]
    else:
        header_kor=header_kor[1:len(header_kor)-1]

    #문장을 나누고 파일에 쓰기 
    final_header_kor=kor_sentence(header_kor)
    for m in range(len(final_header_kor)):
                   #print(final_header_kor[m])
                   f_header_kor.write(final_header_kor[m])
    f_header_kor.write("\n")
    
    #print("----------------------------------")

    ####  ENGLISH HEADER  ####
    #header만 추출
    #print("[eng]")
    non_bmp_map2=dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)
    eng_content_list=str(para_eng).translate(non_bmp_map2).split("<p></p>")
    #eng_content_list="<p>".join(eng_content_list).split("</table>\n<p>")
    header_eng=remove_comma(str(eng_content_list[0]).translate(non_bmp_map2))
    header_eng=remove_span(header_eng)
    header_eng=remove_tags(header_eng)
    if header_eng[len(header_eng)-2]==',':
        header_eng=header_eng[1:len(header_eng)-2]
    else:
        header_eng=header_eng[1:len(header_eng)-1]

    #문장을 나누고 파일에 쓰기
    
    final_header_eng=sent_tokenize(header_eng)
    final_header_eng=eng_sentence(final_header_eng)
    for x in range(len(final_header_eng)):
                #print(final_header_eng[x])
                f_header_eng.write(final_header_eng[x])
                f_header_eng.write("\n") 
    f_header_eng.write("\n")            

    return 0 
    #print("\n\n")
    #print("\n\n")

    

