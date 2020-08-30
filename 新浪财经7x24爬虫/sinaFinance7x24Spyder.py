#encoding:utf-8

import requests
import json
import time
import csv
import codecs
import sys
import pandas as pd


def getJsonStr(base_url):
    json_str =''
    try:
        headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
        response = requests.get(base_url,timeout=5,headers=headers)
        html = response.text
        html_cl = html[12:-14]
        html_json = eval(html_cl)
        json_str = json.dumps(html_json)
    except:
        print("getJsonStr ERROR")
        
    finally:
        return json_str

def jsonStrAnalysis(json_date): 

    date_dic={}
    try:
        python_dic = json.loads(json_date)
        
        list_str=python_dic["result"]['data']['feed']['list']
       
        for list_dic in list_str:#对list的多组数据解析
            need_option=['id','rich_text','create_time','tag']
            for listkey in list(list_dic.keys()):
                if listkey not in need_option:
                    list_dic.pop(listkey)
            date_dic[list_dic['id']]=list_dic
    except:
        print("jsonStrAnalysis ERROR")
    finally:
        return date_dic

def listDicDisplay(listdic):
    create_timez_str=tag_id_str=type_str=rich_text_str=data_id_str=''
    #下面为解析出来的数据           
    data_id_str = listdic['id']
    rich_text_str=listdic['rich_text']
    create_timez_str = listdic['create_time']
    tag_str = listdic['tag']
    
    tag_id_str = []
    type_str = []
    for tag_dic in tag_str:
        #print(tagpp)
        tag_id_str.append(tag_dic['id'])
        type_str.append(tag_dic['name'])

    #print
    #print('新浪数据库中id为',data_id_str,'的数据')
    #print('时间:',create_timez_str)
    #print('id:',tag_id_str,'     类型:',type_str)
    #print('内容:',rich_text_str)

    return data_id_str,create_timez_str, tag_id_str, type_str, rich_text_str


       
if __name__=='__main__':

    
    listaa = []
    lista = []
    listb = []
    listc = []
    listd = []

    start = 1 #指定开始条数
    cnt = start
    for i in range(start,10001):
        base_url_new = 'http://zhibo.sina.com.cn/api/zhibo/feed?callback=jQuery0&page=' + str(i) + '&page_size=1&zhibo_id=152&tag_id=3&dire=f&dpc=1&pagesize=2&_=0%20Request%20Method:GET'

        json_date = getJsonStr(base_url_new)
        jsaoutput_dic = jsonStrAnalysis(json_date)
        for dataid in jsaoutput_dic.keys():
            aa,a,b,c,d = listDicDisplay(jsaoutput_dic[dataid])
            listaa.append(str(aa))
            lista.append(str(a))
            listb.append(str(b))
            listc.append(str(c))
            listd.append(str(d))

            #print(richtextstr)
            #time.sleep(1)
        print("正在写入第%d条数据"%(i))

        if i % 5000 == 0:

            dataframe = pd.DataFrame({'数据库内部编号':listaa,'时间':lista,'tagid':listb,'类型':listc,'内容':listd}) # 只使用时间，内容
            filename = 'sinaFinance7x24_' + str(cnt) + '_.csv'
            dataframe.to_csv(filename,index=False,sep=',',encoding="utf_8_sig") # 解决中文乱码问题
            cnt += 1
            listaa = []
            lista = []
            listb = []
            listc = []
            listd = []

    #write unwrite data
    dataframe = pd.DataFrame({'数据库内部编号':listaa,'时间':lista,'tagid':listb,'类型':listc,'内容':listd}) # 只使用时间，内容
    filename = 'sinaFinance7x24_' + str(cnt) + '_.csv'
    dataframe.to_csv(filename,index=False,sep=',',encoding="utf_8_sig") # 解决中文乱码问题
    cnt += 1
    listaa = []
    lista = []
    listb = []
    listc = []
    listd = []