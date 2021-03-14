import requests
import json
from bs4 import BeautifulSoup # html处理库

def getURLDataFromSina(keyword, pageSize, page):
    '''
    说明:
        通过关键词从新浪新闻搜索中获取数据，通过配合修改pageSize和page到一个合适的组合，可以获取到更多的数据
        实测：
            pageSize10，page最多到50；pageSize100，调整page到50虽然有空数据，但是好像能获取到更多的数据
            前端界面最多每页10条展示50条数据
    input:
        keyword:
            dataType: str
            说明: 需要查询的关键词
            示例: 中国银行
        pageSize:
            dataType: int
            说明: 每页获取的数据数
            示例: 10
        page:
            dataType: int
            说明: 获取第几页的数据
            示例: 1
    output:
        tempList:
        dataType: list
        说明: 返回的列表组合，其中每一项依次title, 链接, [日期, 具体时间]
        示例: [['中银上证国企100ETF净值上涨2.62％ 请保持关注', 'http://cj.sina.com.cn/articles/view/1704103183/65928d0f020026t2n', ['2021-03-12', '07:06:00']], ...]

    '''    

    baseURL = "http://search.sina.com.cn/?&c=news&from=channel&col=&range=all&source=&country=&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0"
    url = baseURL + "&q=" + keyword + "&size=" + str(pageSize) + "&page=" + str(page)
    payload = {}
    # 加cookie从尝试来说好像可以获取到更多的数据
    headers = {
        'Host': 'search.sina.com.cn',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'U_TRS1=0000001b.c526122a.60111b44.a0fea1eb; UOR=www.baidu.com,blog.sina.com.cn,; SINAGLOBAL=111.197.119.75_1611733829.558886; SCF=AlGTQWV36ioExcFFeTepvRa3DNH2sQXTYKc9l18zmv5VRD6rqqPlmJ6Tl3ideZuHPpxmhhpWB-Y7VkDf7frlWp0.; UM_distinctid=177b1728599400-0de244d75e2495-33647509-13c680-177b172859a781; __gads=ID=f1b7afa8447e4ad1-22400f6c0ec600a6:T=1613589809:RT=1613589809:S=ALNI_Mbva08CEXTucIyJz_VdTZuWa9qK8A; Apache=221.219.25.106_1615609319.707385; SUB=_2A25NSE26DeRhGeBI6VoX8ybEwjqIHXVuPDhyrDV_PUNbm9AKLWzdkW9NRodniGjpHKgWlmd07OMPtGZK1syijYKV; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFUm.qi08R7DA3he1qPNVpf5NHD95QcSozRSoeR1h.cWs4DqcjGMJLfUgv0q7tt; ALF=1647145322; U_TRS2=0000006a.ec91a3a3.604c3dea.22103c9a; ULV=1615609323357:5:2:2:221.219.25.106_1615609319.707385:1615609318930; beegosessionID=add80052dcc3b5c18f3628a7381243ef; SEARCH-SINA-COM-CN=37f74a9f53ebe4bdbdbaca38a6b451f7; beegosessionID=4e9e3a5f731610c3c9090e045ae7b309; SEARCH-SINA-COM-CN=484fb5dd86ee7bffbce4d7b80076f126'
    }

    response = requests.request("GET", url, headers=headers, data=payload) # 得到一个html的返回结果
    soup = BeautifulSoup(response.text, "html.parser") # 转化为soup对象

    # debug
    # with open('respnse-html保存/debug-2.html', 'a+', encoding='utf-8') as writer:
    #     writer.write(response.text)

    # 开始html解析
    tempList = []
    for i in range(6, 6+pageSize): # 共有pageSize条数据
        selectPathLinkText1 = "#result > div:nth-child(" + str(i) + ") > h2 > a"
        selectPathTime1 = "#result > div:nth-child(" + str(i) + ") > h2 > span"
        selectPathLinkText2 = "#result > div:nth-child(" + str(i) + ") > div > h2 > a"
        selectPathTime2 = "#result > div:nth-child(" + str(i) + ") > div > h2 > span"
        title = ''
        link = ''
        time = []
        if len(soup.select(selectPathLinkText1)):
            # print("title: ", soup.select(selectPathLinkText1)[0].get_text())
            # print("link: ", soup.select(selectPathLinkText1)[0]['href'])
            # print("time: ", soup.select(selectPathTime1)[0].get_text())
            title = soup.select(selectPathLinkText1)[0].get_text() # 获取标题
            link = soup.select(selectPathLinkText1)[0]['href'] # 获取链接
            time = soup.select(selectPathTime1)[0].get_text().split(' ')[1:] # 获取时间，后两个是有用的信息
        elif len(soup.select(selectPathLinkText2)):
            # print("title: ", soup.select(selectPathLinkText2)[0].get_text())
            # print("link: ", soup.select(selectPathLinkText2)[0]['href'])
            # print("time: ", soup.select(selectPathTime2)[0].get_text())
            title = soup.select(selectPathLinkText2)[0].get_text() # 获取标题
            link = soup.select(selectPathLinkText2)[0]['href'] # 获取链接
            time = soup.select(selectPathTime2)[0].get_text().split(' ')[1:] # 取后两个是有用的信息

        tempList.append([title, link, time])

    print("tempList: ", tempList)
    print("len of tempList", len(tempList))
    return tempList

def getContent(title, url, time):
    '''
    说明:
        进入到第二个界面中获取具体文本内容和title等，每次处理一条数据
    input:
        title:
            dataType: str
            说明: 在第一个界面中获取到的title
            示例: 中国银行行长，人选落定！
        url:
            dataType: str
            说明: 新闻对应的url
            示例: http://finance.sina.com.cn/wm/2021-02-25/doc-ikftssap8754329.shtml
        time:
            dataType: list
            说明: [日期时间, 具体时间]的列表
            示例: ['2021-02-25', '21:32:49']
    '''
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload) # 得到一个html的返回结果
    content = response.text.encode(response.encoding).decode(response.apparent_encoding) # 转码
    soup = BeautifulSoup(content, "html.parser") # 转化为soup对象
    
    # debug
    # with open('respnse-html保存/debug-5.html', 'a+', encoding='utf-8') as writer:
    #     writer.write(content)
    
    if 'http://finance.sina.com.cn' in url or 'http://t.cj.sina.com.cn' in url:
        selectMainTitlePath = "body > div.main-content.w1240 > h1"
        mainTitle = soup.select(selectMainTitlePath)[0].get_text() # 获取标题
        selectMainArticlePath = "#artibody"
        mainArticle = soup.select(selectMainArticlePath)[0].get_text().strip().replace("\n", '').replace("海量资讯、精准解读，尽在新浪财经APP", '') # 获取正文
    elif 'http://k.sina.com.cn' in url:
        selectMainTitlePath = "body > div.main-content.w1240 > h1"
        mainTitle = soup.select(selectMainTitlePath)[0].get_text() # 获取标题
        selectMainArticlePath = "#article"
        mainArticle = soup.select(selectMainArticlePath)[0].get_text().strip().replace("\n", '') # 获取正文-
    
    print("mainTitle", mainTitle)
    print("mainArticle", mainArticle)
    return mainTitle, mainArticle, time
    
def saveFile(fileDir, fileName, mainArticle):
    '''
    说明：
        写文件函数，后续可以根据需要拓展，现在可以根据文件夹路径和文件名写文件
    input:
        fileDir:
            dataType: str
            说明: 文件保存的路径（一个文件夹）
            示例: /Users/curious/Desktop/news/
        fileName:
            dataType: str
            说明: 想要把文件保存成什么文件名（注：有时候文件名不能包含特殊字符会出现异常，暂时没处理）
            示例: 中国建设银行获评“最佳零售银行大奖”
        mainArticle:
            dataType: str
            说明: 要写入文件中的内容
            示例: 日前，由《零售银行》《数字银行》联合腾讯云共同举办的“第四届中国零售金融创新实践大奖评选”公布获奖名单。
    output:
        status:
            dataType: str
            说明: 写入是否成功，成功为SUCCESS，不成功为ERROR
            示例: SUCCESS
    '''
    try:
        with open(fileDir+fileName+'.txt', 'a+', encoding='utf-8') as writer:
            writer.write(mainArticle)
        return 'SUCCESS'
    except:
        return 'ERROR'

if __name__ == '__main__':

    tempDataList = getURLDataFromSina(
        keyword = '建设银行', 
        pageSize = 10, 
        page = 5
    )

    # 批量遍历，一条一条调用getContent
    for item in tempDataList:
        title = item[0]
        url = item[1]
        time = item[2]
        mainTitle, mainArticle, time = getContent(
            title = title, 
            url = url, 
            time = time
        )
        # 写文件
        saveFile(
            fileDir = '/Users/curious/Desktop/news/', 
            fileName = mainTitle, 
            mainArticle = mainArticle
        )

    # getContent(
    #     title = "中国银行行长，人选落定！", 
    #     url = "http://finance.sina.com.cn/wm/2021-02-25/doc-ikftssap8754329.shtml", 
    #     time = ['2021-02-25', '21:32:49']
    # )