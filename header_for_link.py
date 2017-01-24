from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import sys
import copy


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

def check_table_index(sources):
    
    #쓸때 없는 table 위치 찾기(kor)
    table_st=[]
    table_fi=[]
    st=-1
    fi=-1
    while 1:
        st=str(sources).find('<table',st+1)
        if st!=-1:
            table_st.append(st)
        else:
            break

    while 1:
        fi=str(sources).find('</table>',fi+1)
        if fi!=-1:
            table_fi.append(fi)
        else:
            break

    #table 쌍 맞춰서 리스트에 집어넣음 
    table_set=[[] for i in range(len(table_fi))]
    i=0
    j=0
    while 1:
        
        if i>=len(table_fi):
            break
        ct=0
        while 1:  
            if  j>=len(table_st) or table_fi[i]<table_st[j]:
                table_set[i].append(table_st[i])
                table_set[i].append(table_fi[j-1])
                break

            else:
                j=j+1
                ct=ct+1
                
        i=i+ct
    return table_set
                
i=0
while i<40:


    #저장된 한-영 HTML 받아오기
    
    f_kor=open("./kor/kor_"+str(i)+".txt","r",encoding='UTF8')
    html_kor=f_kor.read()
    sourcesKOR = BeautifulSoup(html_kor,"html.parser")

    f_eng=open("./eng/eng_"+str(i)+".txt","r",encoding='UTF8')
    html_eng=f_eng.read()
    sourcesENG = BeautifulSoup(html_eng,"html.parser")
    
    
   
    #쓸때 없는 table 부분 삭제
    

    tmp_kor=str(sourcesKOR)
    tmp_eng=str(sourcesENG)

    table_set_kor=check_table_index(sourcesKOR)
    table_set_eng=check_table_index(sourcesENG)


    #불필요한 table제거 (kor)  
    kkk=[]
    for i in range(len(table_set_kor)):
        if table_set_kor[i]==[]:
            continue
        kkk.append(tmp_kor[table_set_kor[i][0]:table_set_kor[i][1]+9])
        

    for i in range(len(kkk)): 
        tmp_kor=tmp_kor.replace(str(kkk[i]),'')

    #불필요한 table제거 (eng)  
    eee=[]
    for i in range(len(table_set_eng)):
        if table_set_eng[i]==[]:
            continue
        eee.append(tmp_eng[table_set_eng[i][0]:table_set_eng[i][1]+9])
        

    for i in range(len(eee)): 
        tmp_eng=tmp_eng.replace(str(eee[i]),'')
    
    
    sourcesKOR_tmp=BeautifulSoup(tmp_kor,"html.parser")
    sourcesENG_tmp=BeautifulSoup(tmp_eng,"html.parser")

   
    #문단 부분만 추출
    para_kor = sourcesKOR_tmp.findAll('p')
    para_eng = sourcesENG_tmp.findAll('p')

   
    #문단이 없으면 다음 문서로 넘어가기 
    if len(para_kor)==0 or len(para_eng)==0:
        i=i+1
        continue
                
    print("["+str(i)+"]")    

    #추출할 header_link를 저장하기 위한 파일오픈
    f_header_kor=open("./header/kor/"+str(i)+".txt","w",encoding='UTF8')
    f_header_eng=open("./header/eng/"+str(i)+".txt","w",encoding='UTF8')
       
    ####  KOREA  HEADER  ####
    #header만 추출 
    print("[kor]")
    non_bmp_map=dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)
    kor_content_list=str(para_kor).translate(non_bmp_map).split("<p></p>")
    header_kor=remove_comma(str(kor_content_list[0]).translate(non_bmp_map))
    header_kor=remove_span(header_kor)
    #header_kor=remove_tags(header_kor)
    if header_kor[len(header_kor)-2]==',':
        header_kor=header_kor[1:len(header_kor)-2]
    else:
        header_kor=header_kor[1:len(header_kor)-1]

    #문장을 나누고 파일에 link만 쓰기 
    final_header_kor=kor_sentence(header_kor)
    tmp_kor_link=[[]for i in range(len(final_header_kor))]

    #<a ~ </a>부분 잘라내기
    for m in range(len(final_header_kor)):
        start=0
        finish=0
        while 1:
                start=final_header_kor[m].find('<a')
                if start!=-1:
                    finish=final_header_kor[m].find('</a>')
                    tmp_kor_link[m].append(final_header_kor[m][start:finish+4])
                else:
                    break

                while 1:
                    start=final_header_kor[m].find('<a',start+1)
                    if start!=-1:
                        finish=final_header_kor[m].find('</a>',finish+1)
                        tmp_kor_link[m].append(final_header_kor[m][start:finish+4])
                    else:
                        break
                break

    #<a ~ </a>부분에서 단어만 뽑아서 파일에 쓰기 
    tmp=[[]for a in range(len(tmp_kor_link))]
    for a in range(len(tmp_kor_link)):
        for j in range(len(tmp_kor_link[a])):
            st=tmp_kor_link[a][j].find('title="')
            fi=tmp_kor_link[a][j].find('"',st+7)
            tt=tmp_kor_link[a][j]
            tmp[a].append(tt[st+7:fi])
            f_header_kor.write(str(tmp[a][j])+",")
        f_header_kor.write("\n")
    f_header_kor.write("\n")
                
            
    
    
    print("----------------------------------")

    ####  ENGLISH HEADER  ####
    #header만 추출
    print("[eng]")
    non_bmp_map2=dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)
    eng_content_list=str(para_eng).translate(non_bmp_map2).split("<p></p>")
    header_eng=remove_comma(str(eng_content_list[0]).translate(non_bmp_map2))
    header_eng=remove_span(header_eng)
    #header_eng=remove_tags(header_eng)
    if header_eng[len(header_eng)-2]==',':
        header_eng=header_eng[1:len(header_eng)-2]
    else:
        header_eng=header_eng[1:len(header_eng)-1]

    #문장을 나누고 파일에 link만 쓰기
    final_header_eng=sent_tokenize(header_eng)
    final_header_eng=eng_sentence(final_header_eng)
    tmp_eng_link=[[]for i in range(len(final_header_eng))]

    #<a ~ </a>부분 잘라내기
    for m in range(len(final_header_eng)):
        start=0
        finish=0
        while 1:
                start=final_header_eng[m].find('<a')
                if start!=-1:
                    finish=final_header_eng[m].find('</a>')
                    tmp_eng_link[m].append(final_header_eng[m][start:finish+4])
                else:
                    break

                while 1:
                    start=final_header_eng[m].find('<a',start+1)
                    if start!=-1:
                        finish=final_header_eng[m].find('</a>',finish+1)
                        tmp_eng_link[m].append(final_header_eng[m][start:finish+4])
                    else:
                        break
                break
    #<a ~ </a>부분에서 단어만 뽑아서 파일에 쓰기 
    tmp=[[]for a in range(len(tmp_eng_link))]
    for a in range(len(tmp_eng_link)):
        for j in range(len(tmp_eng_link[a])):
            st=tmp_eng_link[a][j].find('title="')
            fi=tmp_eng_link[a][j].find('"',st+7)
            tt=tmp_eng_link[a][j]
            tmp[a].append(tt[st+7:fi])
            f_header_eng.write(str(tmp[a][j])+",")
        f_header_eng.write("\n")
    f_header_eng.write("\n")
    i=i+1
    

    

