from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import sys
import copy
import kor_sentence

i=0
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
                
        
def header(sourcesKOR, sourcesENG,i):
        
    #저장된 한-영 HTML 받아오기
    f_kor=open("src/kor/kor_"+str(i)+".txt","r",encoding='UTF8')
    html_kor=f_kor.read()
    sourcesKOR = BeautifulSoup(html_kor,"html.parser")

    f_eng=open("src/eng/eng_"+str(i)+".txt","r",encoding='UTF8')
    html_eng=f_eng.read()
    sourcesENG = BeautifulSoup(html_eng,"html.parser")
    
    
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
    tmp_kor=str(sourcesKOR)
    tmp_eng=str(sourcesENG)
    
    table_set_kor=check_table_index(sourcesKOR)
    table_set_eng=check_table_index(sourcesENG)


    #불필요한 table제거 (kor)  
    kkk=[]
    for j in range(len(table_set_kor)):
        if table_set_kor[j]==[]:
            continue
        kkk.append(tmp_kor[table_set_kor[j][0]:table_set_kor[j][1]+9])
        

    for k in range(len(kkk)): 
        tmp_kor=tmp_kor.replace(str(kkk[k]),'')

    #불필요한 table제거 (eng)  
    eee=[]
    for l in range(len(table_set_eng)):
        if table_set_eng[l]==[]:
            continue
        eee.append(tmp_eng[table_set_eng[l][0]:table_set_eng[l][1]+9])
        

    for t in range(len(eee)): 
        tmp_eng=tmp_eng.replace(str(eee[t]),'')
        
    
    sourcesKOR_tmp=BeautifulSoup(tmp_kor,"html.parser")
    sourcesENG_tmp=BeautifulSoup(tmp_eng,"html.parser")

   
    #문단 부분만 추출
    para_kor = sourcesKOR_tmp.findAll('p')
    para_eng = sourcesENG_tmp.findAll('p')

   
    #문단이 없으면 다음 문서로 넘어가기 
    if len(para_kor)==0 or len(para_eng)==0:
        return -1   

    #추출할 header를 저장하기 위한 파일오픈
    f_header_kor=open("kor_header/kor_"+str(i)+".txt","w",encoding='UTF8')
    f_header_eng=open("eng_header/eng_"+str(i)+".txt","w",encoding='UTF8')

       
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
    final_header_kor=kor_sentence.kor_sentence(header_kor)
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
    

    

