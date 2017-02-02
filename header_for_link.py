from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import sys
import copy
import kor_sentence


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


def header_for_link(sourcesKOR, sourcesENG, i):
    # 쓸때 없는 table 부분 삭제
    tmp_kor = str(sourcesKOR)
    tmp_eng = str(sourcesENG)

    table_set_kor = check_table_index(sourcesKOR)
    table_set_eng = check_table_index(sourcesENG)

    # 불필요한 table제거 (kor)
    kkk = []
    for j in range(len(table_set_kor)):
        if table_set_kor[j] == []:
            continue
        kkk.append(tmp_kor[table_set_kor[j][0]:table_set_kor[j][1] + 9])

    for j in range(len(kkk)):
        tmp_kor = tmp_kor.replace(str(kkk[j]), '')

    # 불필요한 table제거 (eng)
    eee = []
    for j in range(len(table_set_eng)):
        if table_set_eng[j] == []:
            continue
        eee.append(tmp_eng[table_set_eng[j][0]:table_set_eng[j][1] + 9])

    for j in range(len(eee)):
        tmp_eng = tmp_eng.replace(str(eee[j]), '')

    sourcesKOR_tmp = BeautifulSoup(tmp_kor, "html.parser")
    sourcesENG_tmp = BeautifulSoup(tmp_eng, "html.parser")

    # 문단 부분만 추출
    para_kor = sourcesKOR_tmp.findAll('p')
    para_eng = sourcesENG_tmp.findAll('p')

    # 문단이 없으면 다음 문서로 넘어가기
    if len(para_kor) == 0 or len(para_eng) == 0:
        i = i + 1
        return -1

    # print(str(i)+".txt")

    # 추출할 header_link를 저장하기 위한 파일오픈
    f_header_kor = open("./header/kor/" + str(i) + ".txt", "w", encoding='UTF8')
    f_header_eng = open("./header/eng/" + str(i) + ".txt", "w", encoding='UTF8')

    ####  KOREA  HEADER  ####
    # header만 추출
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    kor_content_list = str(para_kor).translate(non_bmp_map).split("<p></p>")
    header_kor = remove_comma(str(kor_content_list[0]).translate(non_bmp_map))
    header_kor = remove_span(header_kor)

    # header_kor=remove_tags(header_kor)
    if header_kor[len(header_kor) - 2] == ',':
        header_kor = header_kor[1:len(header_kor) - 2]
    else:
        header_kor = header_kor[1:len(header_kor) - 1]

    # 문장을 나누고 파일에 link만 쓰기
    header_kor = header_kor[:len(header_kor) - 4]
    final_header_kor = kor_sentence.kor_sentence(header_kor)
    tmp_kor_link = [[] for j in range(len(final_header_kor))]

    # <a ~ </a>부분 잘라내기
    for m in range(len(final_header_kor)):
        start = 0
        finish = 0
        while 1:
            start = final_header_kor[m].find('<a')
            if start != -1:
                finish = final_header_kor[m].find('</a>')
                tmp_kor_link[m].append(final_header_kor[m][start:finish + 4])
            else:
                break

            while 1:
                start = final_header_kor[m].find('<a', start + 1)
                if start != -1:
                    finish = final_header_kor[m].find('</a>', finish + 1)
                    tmp_kor_link[m].append(final_header_kor[m][start:finish + 4])
                else:
                    break
            break

    # <a ~ </a>부분에서 단어만 뽑아서 파일에 쓰기
    tmp = [[] for j in range(len(tmp_kor_link))]
    for k in range(len(tmp_kor_link)):
        if len(tmp_kor_link[k]) == 0:
            f_header_kor.write("\n")
            continue
        for j in range(len(tmp_kor_link[k])):
            # title 부분
            st = tmp_kor_link[k][j].find('title="')
            if st == -1:
                continue
            fi = tmp_kor_link[k][j].find('"', st + 7)
            tt = tmp_kor_link[k][j]

            if str(tt[fi - 1]) == ' ':
                tt = tt[st + 7:fi - 1]
            else:
                tt = tt[st + 7:fi]

            kk = tt.find(':')
            if kk >= 0:
                tt = tt[kk + 1:]

            # > ... </a> 부분
            '''
            st2=tmp_kor_link[k][j].find('>')
            fi2=tmp_kor_link[k][j].find('</a>')
            tt2=tmp_kor_link[k][j]

            if str(tt2[fi2-1])==' ':
                   tt2=tt2[st2+1:fi2-1]
            else:
                   tt2=tt2[st2+1:fi2]

            #title과 > .. </a>비교
            tt=tt.lower()
            tt2=tt2.lower()

            if tt==tt2:
                f_header_kor.write(str(tt)+",")

            else:
                continue
            '''
            f_header_kor.write(str(tt) + ",")
        f_header_kor.write("\n")
    f_header_kor.write("\n")

    ####  ENGLISH HEADER  ####
    # header만 추출
    non_bmp_map2 = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    eng_content_list = str(para_eng).translate(non_bmp_map2).split("<p></p>")
    header_eng = remove_comma(str(eng_content_list[0]).translate(non_bmp_map2))
    header_eng = remove_span(header_eng)
    # header_eng=remove_tags(header_eng)
    if header_eng[len(header_eng) - 2] == ',':
        header_eng = header_eng[1:len(header_eng) - 2]
    else:
        header_eng = header_eng[1:len(header_eng) - 1]

    # 문장을 나누고 파일에 link만 쓰기
    final_header_eng = sent_tokenize(header_eng)
    final_header_eng = eng_sentence(final_header_eng)
    tmp_eng_link = [[] for j in range(len(final_header_eng))]

    # <a ~ </a>부분 잘라내기
    for m in range(len(final_header_eng)):
        start = 0
        finish = 0
        while 1:
            start = final_header_eng[m].find('<a')
            if start != -1:
                finish = final_header_eng[m].find('</a>')
                tmp_eng_link[m].append(final_header_eng[m][start:finish + 4])
            else:
                break

            while 1:
                start = final_header_eng[m].find('<a', start + 1)
                if start != -1:
                    finish = final_header_eng[m].find('</a>', finish + 1)
                    tmp_eng_link[m].append(final_header_eng[m][start:finish + 4])
                else:
                    break
            break
    # <a ~ </a>부분에서 단어만 뽑아서 파일에 쓰기
    tmp = [[] for j in range(len(tmp_eng_link))]
    for k in range(len(tmp_eng_link)):
        if len(tmp_eng_link[k]) == 0:
            f_header_eng.write("\n")
            continue
        for j in range(len(tmp_eng_link[k])):
            # title 부분
            st = tmp_eng_link[k][j].find('title="')
            if st == -1:
                continue
            fi = tmp_eng_link[k][j].find('"', st + 7)
            tt = tmp_eng_link[k][j]

            if str(tt[fi - 1]) == ' ':
                tt = tt[st + 7:fi - 1]
            else:
                tt = tt[st + 7:fi]

            kk = tt.find(':')
            if kk >= 0:
                tt = tt[kk + 1:]

            # > ... </a> 부분
            '''
            st2=tmp_eng_link[k][j].find('>')
            fi2=tmp_eng_link[k][j].find('</a>')
            tt2=tmp_eng_link[k][j]

            if str(tt2[fi2-1])==' ':
                   tt2=tt2[st2+1:fi2-1]
            else:
                   tt2=tt2[st2+1:fi2]

            #title과 > .. </a>비교
            tt=tt.lower()
            tt2=tt2.lower()

            if tt==tt2:
                f_header_eng.write(str(tt)+",")
                print("tt",tt)
                print("tt2",tt2)
            else:
                continue
            '''
            f_header_eng.write(str(tt) + ",")
        f_header_eng.write("\n")
    f_header_eng.write("\n")

    i = i + 1