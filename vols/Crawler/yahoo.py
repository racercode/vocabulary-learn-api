#from readline import append_history_file
from logging.config import listen
from urllib.request import Request,urlopen
from bs4 import *
# Request 可以幫助發出複雜的請求(帶header)，所以不直接用urlopen
def GetWebData(word): # 輸入單字
    link = "https://tw.dictionary.search.yahoo.com/search?p="+word
    request = Request(link,headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    })
    Web = urlopen(request)
    Data = Web.read().decode('utf-8') 
    # 回傳帶了很多16進制垃圾(跳脫字元)，要轉回來
    # type = str所以要解析
    bs4_Data = BeautifulSoup(Data,'html.parser')
    # BeautifulSoup解析html的str成bs4.BeautifulSoup格式，可是他很慢就是
    if(bs4_Data.find(name="h3", class_="title lh-24")==None):
        return "Can't find the word in yahoo",0,0,0,0,0
    # 如果找不到單字，回傳"Can't find the word"

    Tense = [] # 時態
    Comparative = [] #比較級
    Plural =  [] # 單複數
    VerbChange = [] # 動詞變化 (可能有兩種過去式之類的 ex wet-wet-wet, wet-wetted-wetted ) 格式為(過去1,過去2,過去分詞1,過去分詞2,現在分詞)
    FirstLine=bs4_Data.find(name="li", class_="ov-a fst lst mt-0 noImg") # 第一行
    if(FirstLine!=None):
        if FirstLine.span.text[0]=="比":
            for item in FirstLine.span.find_all('b'):
                Comparative.append(item.text)
        if FirstLine.span.text[0]=="過":
            for item in FirstLine.span.find_all('b'):
                Tense.append(item.text)
        if FirstLine.span.text[0]=="名":
            for item in FirstLine.span.find_all('b'):
                Plural.append(item.text)
        if FirstLine.span.text[0]=="動":
            for item in FirstLine.span.find_all('b'):
                VerbChange.append(item.text)        
    
    SecondLine = bs4_Data.find(name="li", class_="ov-a noImg") #第二行
    if(SecondLine!=None):
        if SecondLine.span.text[0]=="比":
            for item in SecondLine.span.find_all('b'):
                Comparative.append(item.text)
        if SecondLine.span.text[0]=="過":
            for item in SecondLine.span.find_all('b'):
                Tense.append(item.text)
        if SecondLine.span.text[0]=="名":
            for item in SecondLine.span.find_all('b'):
                Plural.append(item.text)
        if SecondLine.span.text[0]=="動":
            for item in SecondLine.span.find_all('b'):
                VerbChange.append(item.text)

    # 我沒有找到任何單字有第三行的，所以暫定沒有，以後出現再處理

    listEn = []
    listCh = []
    SetenceAreaDatas = bs4_Data.find_all(name="div", class_="compTextList")
    for i in SetenceAreaDatas:
        Means = i.ul.find_all("li")
        for j in Means:
            Sentences = j.find_all("span",class_="d-b fz-14 fc-2nd lh-20")
            for k in Sentences:
                Period  = k.text.split(". ")
                Question = k.text.split("? ")
                Exclamation = k.text.split("! ")
                if(len(Period)==2):
                    listEn.append(Period[0]+".")
                    listCh.append(Period[1])
                if(len(Question)==2):
                    listEn.append(Question[0]+"?")
                    listCh.append(Question[1])
                if(len(Exclamation)==2):
                    listEn.append(Exclamation[0]+"!")
                    listCh.append(Exclamation[1])

    # 更多解釋裡塞了太多垃圾東西，我就不處理了

    #print(listEn,listCh,Tense,Comparative,Plural,VerbChange,len(listEn),len(listCh) )

    return listEn,listCh,Tense,Comparative,Plural,VerbChange
    # 回傳格式 [ 'an _____ door/window', 'An _____ suitcase lay on her bed.'.... ]
    # ,["中文","這是中文"...]
    # ,[過去式,過去分詞,現在分詞] 動詞
    # ,[比較級,最高級] 形容詞
    # ,[名詞複數] 可數名詞
    # ,[過去式1,過去式2,過去分詞1,過去分詞2,現在分詞] 如果過去式有兩種則有值
    # 相對的中英文有同個index
    # 如果找不到單字，回傳"Can't find the word"
if __name__ == '__main__':
    word = input("輸入 ")
    print(GetWebData(word))






