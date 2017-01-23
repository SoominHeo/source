import re
def make_dictionary():
    dict = {}
    f = open("pair.csv", "r", encoding="UTF8")
    lines = f.readlines()
    a = 0
    for line in lines:
        splt = re.split(",\t|\n", line)
        dict[splt[2]] = splt[3]
    return dict
    f.close()
'''
# using example

dic = make_dictionary();
a = 0
for i in dic:
    a = a + 1
    if a%1000 == 0:
        print ("[" + str(a) + "]"+i+":"+dic[i])
'''