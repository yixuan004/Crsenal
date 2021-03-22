import requests
import json
from bs4 import BeautifulSoup # html处理库
from collections import OrderedDict
from tqdm import tqdm
import time

def getURLDataFromFinancialNews(keyword, page):
    '''
    说明：
        不开放pageSize了，每页10条和前端对应上，虽然效率有牺牲比较好debug
    '''

    baseURL = "https://was.financialnews.com.cn/web/search?&channelid=291444&searchscope=&timescope=&timescopecolumn=&orderby=&andsen=&total=&orsen=&exclude="
    url = baseURL + "&page=" + str(page) + "&searchword=" + keyword + "&keyword=" + keyword + "&perpage=10" + "&outlinepage=10"
    payload = {}
    headers = {
        'Host': 'was.financialnews.com.cn',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_trs_uv=kmixjba1_1825_udq; JSESSIONID=E6BA2E2E02197A219EC01E26C53EFA69'
    }
    response = requests.request("GET", url, headers=headers, data=payload) # 得到一个html的返回结果，GET记得关代理
    soup = BeautifulSoup(response.text, "html5lib") # 转化为soup对象，html5lib解析器
    
    # debug
    # with open("/Users/curious/Desktop/BUPT/工程开发/Crsenal/中国金融新闻网爬虫/response保存/代码get测试-t3.html", 'a+', encoding='utf-8') as writer:
    #     writer.write(response.text)

    # 开始html解析
    tempList = []

    for i in range(2, 1+10): # pageSize定死为每页10条

        boxSelectorPath = '#column1 > div > table > tbody > tr > td > ol > li:nth-child(' + str(i) + ')'
        titleSelectorPath = boxSelectorPath + ' > div:nth-child(1)'
        hrefSelectorPath = boxSelectorPath + ' > div:nth-child(1)'
        pubtimeSelecorPath = boxSelectorPath + ' > div.pubtime'

        title = soup.select(titleSelectorPath)[0].get_text() # 获取标题
        nextLevelDirectoryUrl = str(soup.select(hrefSelectorPath)[0]).split(' ')[2][6: -1] # 鲁棒性较差的获取连接
        pubtime = soup.select(pubtimeSelecorPath)[0].get_text() # 获取pubtime
        
        # debug
        # print("title: ", title)
        # print("nextLevelDirectoryUrl: ", nextLevelDirectoryUrl)
        # print("pubtime: ", pubtime)
        tempList.append([title, nextLevelDirectoryUrl, pubtime])
    
    return tempList

def getContent(outsideTitle, nextLevelDirectoryUrl, pubtime, fileDirName):

    url = nextLevelDirectoryUrl
    payload={}
    headers = {
        'Host': 'www.financialnews.com.cn',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_trs_uv=kmixjba1_1825_udq; _trs_ua_s_1=kmjc0mat_1825_k0y9'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    content = response.text.encode(response.encoding).decode(response.apparent_encoding) # 转码
    soup = BeautifulSoup(content, "html5lib")

    titleSelectorPath = 'body > div:nth-child(4) > div.left > div.content > div.content_title'
    title = soup.select(titleSelectorPath)[0].get_text()

    paraTextSelectorPath = '#Zoom1 > div.TRS_Editor > div'
    paraText = soup.select(paraTextSelectorPath)[0].get_text().strip()

    contentInfoSelectorPath = 'body > div:nth-child(4) > div.left > div.content > div.content_info'
    contentInfo = soup.select(contentInfoSelectorPath)[0].get_text().strip().replace(' ', '').replace('\n', ';')

    # print("title: ", title)
    # print("paraText: ", paraText)
    # print("contentInfo: ", contentInfo)

    # 写一个个的json文件
    writeJsonDict = OrderedDict() # 有序
    writeJsonDict['outsideTitle'] = outsideTitle
    writeJsonDict['outsidePubtime'] = pubtime
    writeJsonDict['insideTitle'] = title
    writeJsonDict['insideParaText'] = paraText
    writeJsonDict['insideContentInfo'] = contentInfo 

    jsonStr = json.dumps(writeJsonDict, indent=4, ensure_ascii=False)
    with open(fileDirName, 'a+', encoding='utf-8') as writer:
        writer.write(jsonStr)

if __name__ == '__main__':

    cnt = 0
    errorCnt = 0

    for i in tqdm(range(1, 5000)):
        try:
            tempList = getURLDataFromFinancialNews(
                keyword = '银行', 
                page = i
            )
            if len(tempList):
                for item in tempList:
                    try:
                        getContent(
                            outsideTitle = item[0],
                            nextLevelDirectoryUrl = item[1], 
                            pubtime = item[2],
                            fileDirName = '/Users/curious/Desktop/BUPT/工程开发/Crsenal/中国金融新闻网爬虫/data/' +  str(cnt) + '.json'
                        )
                        cnt += 1
                    except:
                        # print("sth error on: ", item)
                        errorFileName = '/Users/curious/Desktop/BUPT/工程开发/Crsenal/中国金融新闻网爬虫/errorlog/errorlog.txt'
                        with open(errorFileName, 'a+', encoding='utf-8') as writer:
                            writer.write(str(item)+'\n')
                    time.sleep(0.5) # 防止爆接口
            else:
                print("sth error on page: ", i)
        except:
            print("sth error on page: ", i)
            continue

    print("done!")