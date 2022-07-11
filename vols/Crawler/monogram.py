from wsgiref import headers
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen

def find_monogram(word):
    url = "https://conjugator.reverso.net/conjugation-english-verb-"+word+".html"
    request =  Request(url,headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    })
    try:
        Web = urlopen(request)
    except:
        return "not found"

    # 找不到就回傳 not found
    Data = Web.read().decode("utf-8")
    bs4_Data = BeautifulSoup(Data,'html.parser')
    if(bs4_Data.find(name="span",id_="ch_lblCustomMessage" )):
         return "not find"

    find_Data =  bs4_Data.find(name="div",class_="result-block-api").find(name="div",class_="blue-box-wrap").find_all(name="i",class_="verbtxt")
    third_verb = find_Data[2].text

    return third_verb

if __name__ == "__main__":
    word = input("input word ")
    print(find_monogram(word))
