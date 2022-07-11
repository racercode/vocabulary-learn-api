#from readline import append_history_file
from urllib.request import Request,urlopen
from bs4 import *
# Request 可以幫助發出複雜的請求(帶header)，所以不直接用urlopen
def GetWebData(word): # 輸入單字
    link = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/"+word
    request = Request(link,headers={
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    })
    Web = urlopen(request)
    Data = Web.read().decode('utf-8') 
    # 回傳帶了很多16進制垃圾(跳脫字元)，要轉回來
    # type = str所以要解析
    bs4_Data = BeautifulSoup(Data,'html.parser')
    # BeautifulSoup解析html的str成bs4.BeautifulSoup格式，可是他很慢就是

    if(bs4_Data.find(name="title").text=="劍橋詞典：英語-中文(繁體)翻譯"):
        return "Can't find the word in Cambridge",0
    # 如果找不到單字，回傳"Can't find the word"

    SetenceDatas = bs4_Data.find_all(name="div", class_="examp dexamp")
    listEn = []
    notAppend = []
    i=0
    for SetenceData in SetenceDatas:
        if(SetenceData.find(name="span",class_="trans dtrans dtrans-se hdb break-cj")==None):
            continue
        Setence = SetenceData.find(name="span",class_="eg deg").text
        # 這裡不能用.string要用.text，因為span裡面還塞了不少的<a>標籤(連結到個別單字頁面)
        if len(Setence.split(" "))<=5 :
            notAppend.append(i)
            i = i+1 
            continue
        listEn.append(Setence)
        i = i+1
        # listEn 為英文句子
    TransDatas = bs4_Data.find_all(name="span", class_="trans dtrans dtrans-se hdb break-cj")
    listCh = []
    i=0
    for TransData in TransDatas:
        if len(notAppend) != 0 and notAppend[0] == i:
            notAppend.pop(0)
            i = i+1
            continue
        Translation = TransData.text
        listCh.append(Translation)
        i = i+1

    #for i in range(0,20):
    #    print(listEn[i],listCh[i]) 測試用
    return listEn ,listCh  
    # 回傳格式 [ 'an _____ door/window', 'An _____ suitcase lay on her bed.'.... ]
    # ,["中文","這是中文"...]
    # 相對的中英文有同個index
    # 如果找不到單字，回傳"Can't find the word"
if __name__ == '__main__':
    word = input("輸入 ")
    print(GetWebData(word))






