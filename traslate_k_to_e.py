import os
import make_dictionary

# 이 함수 사용하기 전에
# ./header/kor/0.txt 에는 한국어 <a> tage 안에 있는 elements들이 들어 있고
# ./hedaer/eng/0.txt 에는 영어 <a> tage 안에 있는 elements들이 들어 있다. (성민오빠가 만든 header_for_link.py를 돌리면 이렇게 생성되도록 만들어야 해용)
# 성민 오빠 코드의 251번째 줄을
# f_header_kor=open("./header/kor/"+str(i)+".txt","w",encoding='UTF8')
# f_header_eng=open("./header/eng/"+str(i)+".txt","w",encoding='UTF8')
# 이렇게 만들어야 합니다.

# 이 함수를 실행시키면 ./header/changed_kor/0.txt 가 생성되고, 그 안에는 ./header/kor/0.txt 에 포함되어 있던 한국어 element들이 영어 element로 바뀌어서 저장이 된다.
# main 문에는 아래에 #using example을 참조하여 사용한다.

def translate_k_to_e(dic):
    lst = os.listdir("./header/kor/")
    for i in lst:
        print (i)
        f = open("./header/kor/"+str(i), "r", encoding="UTF8")
        k = open("./header/changed_kor/"+str(i), "w", encoding="UTF8")
        a = 0
        for j in f.readlines():
            words = j.split(",")
            words.pop()
            for element in words:
                if element in dic.keys():
                    k.write (str(dic[element]) + ",")
            k.write ("\n")
            a = a + 1

#using example
dic = make_dictionary.make_dictionary()
translate_k_to_e(dic)
