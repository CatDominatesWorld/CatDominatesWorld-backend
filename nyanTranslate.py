from bs4 import BeautifulSoup
import re
from konlpy.tag import Mecab
import nltk
from face_conversion import convert_image
from config import baseURL

mecab = Mecab()

def parse_and_convert(content, level):
    content = content.replace('\n','')
    result = list(re.split("(</?[^<>]*>)", content))
    for i in range(len(result)):
        element = result[i]
        if (element == ""):
            continue
        if (element[0] == "<"):
            soup = BeautifulSoup(element, 'html.parser')
            tag = soup.img
            if (tag == None): continue
            else:
                src = tag.get("src")
                if (src is None):
                    continue
                if (src.startswith("//")):
                    src = "https:" + src
                path = convert_image(src)
                if (path is not None):
                    tag["src"] = path
                result[i]= str(tag)

        else:
            prevElement = result[i-1]
            if prevElement.startswith("<script"):
                continue
            if (level == 5):
                element = re.sub("[^.!?\s]","냥",element)
                element = re.sub("[.!?]","냥🐾", element)
            elif (level >= 3):
                pos = mecab.pos(element)
                posind = 0
                elemind = 0
                elemIndPrev = 0
                newElement = ""
                while (elemind < len(element)):
                    if (posind == len(pos)):
                        elemind += 1
                        continue
                    word = pos[posind][0]
                    if element.startswith(word, elemind):
                        if (elemIndPrev != elemind):
                            newElement += element[elemIndPrev:elemind]
                        wordType = pos[posind][1]
                        if (wordType in ["NNG", "NNP", "NNB"]):
                            word = "냥"*len(word)
                        newElement += word
                        posind += 1
                        elemind += len(word)
                        elemIndPrev = elemind
                    else:
                        elemind += 1
                element = newElement
            if (level >= 2):
                element = re.sub("요?[.!?]","냥🐾", element)
            if (level == 1):
                element = re.sub("(다[.])","다🐾", element)
            result[i] = element
    return ''.join(result)