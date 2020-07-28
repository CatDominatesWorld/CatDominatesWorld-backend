from bs4 import BeautifulSoup
import re
from konlpy.tag import Mecab
import nltk
from face_conversion import convert_image
from urllib.parse import urljoin
from langdetect import detect, lang_detect_exception
import math

mecab = Mecab()

def textConvertKor(element, level):
    postPositionDict = {"를": "을", "가":"이", "라면":"이라면", "는":"은", "와":"과", "로써":"으로써", "로":"으로"}
    if (level == 5):
        ''' Replace everything to 냥 '''
        element = re.sub("[^.!?\s]","냥",element)
        element = re.sub("[.!?]","🐾", element)
        return element
    if (level >= 3):
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
                if (wordType in ["NNG", "NNP"]):
                    word = "냥"*len(word)
                elif (word in postPositionDict.keys()):
                    prevWordType = pos[posind-1][1]
                    if (prevWordType in ["NNG", "NNP"]):
                        word = postPositionDict[word]
                newElement += word
                posind += 1
                elemind += len(word)
                elemIndPrev = elemind
            else:
                elemind += 1
        newElement += element[elemIndPrev:elemind]
        element = newElement
    if (level >= 2):
        element = re.sub("요[.!?]","냥🐾", element)
        element = re.sub("다[.!?]","다냥🐾", element)
        element = re.sub("까[.!?]","까냥🐾", element)
    if (level == 1):
        element = re.sub("(다[.])","다🐾", element)
    return element


def wordToMeow(word):
    if (word == ""):
        return word
    punctuationSplit = re.split('(\W)', word)
    for i in range (len(punctuationSplit)):
        token = punctuationSplit[i]
        if (token == ""): continue
        if (re.match('\W', token)) is not None:
            continue
        meowCount = math.ceil(len(token) / 4)
        newToken = "meow"*meowCount
        if token[0].isupper():
            newToken = newToken.capitalize()
        punctuationSplit[i] = newToken
    newWord = ''.join(punctuationSplit)
    return newWord

def textConvertEng(element, level):
    if (level == 5):
        tokens = re.split("(\s)", element)
        for i in range (len(tokens)):
            token = tokens[i]
            if token.isspace():
                continue
            tokens[i] = wordToMeow(token)
        element = ''.join(tokens)
    
    if (5 > level >= 3):
        pos = nltk.pos_tag(nltk.word_tokenize(element))
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
                elemind += len(word)
                wordType = pos[posind][1]
                if (wordType in ["NN", "NNS", "NNP", "NNPS", "PRP"]):
                    word = wordToMeow(word)
                newElement += word
                posind += 1
                elemIndPrev = elemind
            else:
                elemind += 1
        newElement += element[elemIndPrev:elemind]
        element = newElement

    if (level >= 2):
        element = re.sub("[.!?]","🐾", element)
    if (level == 1):
        element = re.sub("[.]","🐾", element)
    return element


def parse_and_convert(content, level, url):
    content = content.replace('\n','')
    result = list(re.split("(</?[^<>]*>)", content))
    for i in range(len(result)):
        element = result[i]
        if (element == ""):
            continue
        if (element[0] == "<"):
            ''' Handle image '''
            soup = BeautifulSoup(element, 'html.parser')
            tag = soup.img
            if (tag == None): continue
            else:
                src = tag.get("src")
                if (src is None):
                    continue
                if (src.startswith("//")):
                    src = "https:" + src
                elif ((not src.startswith("data")) and (not src.startswith("http"))):
                    src = urljoin(url, src)
                path = convert_image(src)
                if (path is not None):
                    tag["src"] = path
                result[i]= str(tag)

        else:
            ''' Handle text '''
            prevElement = result[i-1]
            if prevElement.startswith("<script") or prevElement.startswith("<style"):
                continue
            try:
                detectResult = detect(element)
                if detectResult == 'en':
                    result[i] = textConvertEng(element, level)
                elif detectResult == 'ko':
                    result[i] = textConvertKor(element, level)
                else:
                    continue
            except lang_detect_exception.LangDetectException:
                continue         
    
    return ''.join(result)