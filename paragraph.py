#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

# check the number of the paragraph in header
def paragraph(sources_k,sources_e):
    kor_paragraph = 0
    eng_paragraph = 0

    # Korea #
    non_bmp_map=dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)
    #set uppber bound (</table>\n<p>) and lower bound(<p></p>)
    kor_header=str(sources_k).translate(non_bmp_map).split("<p></p>")[0]
    kor_header="".join(kor_header).split("</table>\n<p>")

    #if there is upper bound then add <p>
    if(len(kor_header)>1):
        kor_header = "<p> " + str(kor_header[1:])
    
    #get the number of paragraph
    kor_paragraph = len(str(kor_header).split("<p>"))-1

    # English #
    non_bmp_map2=dict.fromkeys(range(0x10000,sys.maxunicode+1),0xfffd)
    eng_header=str(sources_e).translate(non_bmp_map2).split("<p></p>")[0]
    eng_header="".join(eng_header).split("</table>\n<p>")
    if(len(eng_header)>1):
        eng_header = "<p>" + str(eng_header[1:])
    eng_paragraph = len(str(eng_header).split("<p>")) -1

    if(kor_paragraph == eng_paragraph):
        if(kor_paragraph == 0):
            result = -1
        else:
            result = 1 
    else:
        result = 0

    return result

