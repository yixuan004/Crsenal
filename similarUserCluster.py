#encoding:utf-8
import requests as re
import json



def getUid(url):
    ids = []
    response = re.get(url=url)#注意size 请求多少
    response_json = json.loads(response.text)
    for item in response_json['data']['records']:
        ids.append(item['id'])
        
    return ids#营销号

    #http://39.106.90.67:99/api/v1/user/platform/weibo?cur=1&size=20&search=&tag=%255B%255D

def takeAcitve(elem):
    return elem['active']

def test(ids):
          
    alllist = []
    
    for id in ids:
        url = 'http://39.106.90.67:99/api/v1/user/' + str(id)
        tempdict = {}

        response = re.get(url=url)
        response_json = json.loads(response.text)
        
        tempdict['uid'] = response_json['data']['id'] # uid
        tempdict['username'] = response_json['data']['username'] # 用户名
        
        ctrlflag = 0
        
        for liu in range(len(response_json['data']['tags'])):
            if '月活跃' in response_json['data']['tags'][liu]['tag']:
                tempdict['active'] = response_json['data']['tags'][liu]['tag'] # x月活跃 不一定是，第一个tags不一定是
                ctrlflag = 1
                break
        if ctrlflag == 0:
            tempdict['active'] = 'noactive'

        tempdict['msgCountByMonth'] = response_json['data']['msgCountByMonth'] # list 每个月发表的文章数，每条类似{'key':x月, 'count':4}
        tempdict['keyChange'] = response_json['data']['keyChange'] # list 每个月的关键词，每条类似{'month': '1月', 'keywords': ['抗击', '确诊', '防控']}
        tempdict['attitudeChange'] = response_json['data']['attitudeChange'] # list 每个月的心情，每条类似{'month': '7月', 'attitude': -1}

        alllist.append(tempdict)
    
    #alllist.sort(key=takeAcitve) #按照活跃月份排序
    return alllist

def clusterByActive(alllist):
    cluster = {}
    for item in alllist:
        try:
            cluster[item['active']].append(item['uid'])#.append(item)
        except:
            cluster[item['active']] = []
            cluster[item['active']].append(item['uid'])#.append(item)
    #print("clusterByActive",cluster)
    return cluster
    
def clusterByKeyword(alllist,intersectcount):
    
    #create all label
    labelall = []
    for item in alllist:
        for item2 in item['keyChange']:
            for item3 in item2['keywords']:
                if item3 not in labelall:
                    labelall.append(item3)

    #one-hot
    lenlabelall = len(labelall)
    curious = [] 
    for item in alllist:
        templis= [0 for x in range(lenlabelall)]
        for item2 in item['keyChange']:
            for item3 in item2['keywords']:
                templis[labelall.index(item3)] = 1
        curious.append([item['uid'],templis,int(-1)])#item['uid']->item
#    for item in curious:
#        print(item)
#        print("\n")

    #cluster
    cluster = {}
    cnt = 0
    
    for i in curious:
        for j in curious:
            if i != j:

                count = 0
                count2 = 0
                for ttemp1 in range(len(i[1])):
                    if i[1][ttemp1] == j[1][ttemp1] and j[1][ttemp1]==1:
                        count += 1
                    if i[1][ttemp1] != j[1][ttemp1]:
                        count2 += 1
                        
                if(count>=intersectcount and count2 < 1):#对应位置都有的大于a，并且差集个数小于b
                  
                    if i[2] == -1 and j[2] == -1:
                        i[2] = cnt
                        j[2] = cnt
                        cnt += 1
                        cluster[str(i[2])] =  []
                        cluster[str(i[2])].append(i[0])
                        cluster[str(i[2])].append(j[0])
                        
                    elif i[2] == -1 and j[2] != -1:
                        i[2] = j[2]
                        cluster[str(i[2])].append(i[0])
                        
                    elif j[2] == -1 and i[2] != -1:
                        j[2] = i[2]
                        cluster[str(i[2])].append(j[0])
                    else:
                        continue
    #cluster -1 
    for i in curious:
        if i[2] == -1:
            try:
                 cluster[str(i[2])].append(i[0])
            except:
                cluster[str(i[2])] =  []
                cluster[str(i[2])].append(i[0])
            
    #print(cluster)
    return cluster
                    

#按照曲线进行聚类，如何判断两个曲线是否是相似的->按照up down？
#按照曲线进行聚类，如何判断两个曲线是否是相似的->按照up down？
def clusterByMonthCurve(alllist):

    monthlen = 0
    try:
        monthlen = len(alllist[0]['msgCountByMonth'])
        #print(monthlen)
    except:
        print("alllist error")
    
    curious = [] 
    for item in alllist:
        templis= ['' for x in range(monthlen-1)]
        for i in range(1,monthlen):
            #0是一个可以变换的数字，有一种严格强度的感觉
            if item['msgCountByMonth'][i]['count'] - item['msgCountByMonth'][i-1]['count'] > 0:
                templis[i-1] = 'up'
            elif item['msgCountByMonth'][i]['count'] - item['msgCountByMonth'][i-1]['count'] == 0:
                templis[i-1] = 'keep'
            elif item['msgCountByMonth'][i]['count'] - item['msgCountByMonth'][i-1]['count'] < 0:
                templis[i-1] = 'down'
            
            
            #templis[i-1] = item['msgCountByMonth'][i]['count'] - item['msgCountByMonth'][i-1]['count']
        
        curious.append([item['uid'],templis,int(-1)])#[886, ['keep', 'keep', 'keep', 'keep', 'keep', 'up'], -1]
        

#    for item in curious:
#        print(item)
#        print("\n")
    cluster = {}
    cnt = 0
    
    for i in curious:
        for j in curious:
            if i != j:
                flag = 1
                for ttemp1 in range(len(i[1])):
                    if i[1][ttemp1] != j[1][ttemp1]:
                        flag = 0
                        break
                if flag:
                    if i[2] == -1 and j[2] == -1:
                        i[2] = cnt
                        j[2] = cnt
                        cnt += 1
                        cluster[str(i[2])] =  []
                        cluster[str(i[2])].append(i[0])
                        cluster[str(i[2])].append(j[0])
                        
                    elif i[2] == -1 and j[2] != -1:
                        i[2] = j[2]
                        cluster[str(i[2])].append(i[0])
                        
                    elif j[2] == -1 and i[2] != -1:
                        j[2] = i[2]
                        cluster[str(i[2])].append(j[0])
                    else:
                        continue
            
    #cluster -1 
    for i in curious:
        if i[2] == -1:
            try:
                 cluster[str(i[2])].append(i[0])
            except:
                cluster[str(i[2])] =  []
                cluster[str(i[2])].append(i[0])
            
    #print("clusterByMonthCurve",cluster)
    return cluster

    

def clusterByAttitudeCurve(alllist):    
    attitudelen = 0
    try:
        attitudelen= len(alllist[0]['attitudeChange'])
        #print(alllist[0]['uid'],alllist[0]['attitudeChange'])
    except:
        print("alllist error")


    curious = [] 
    for item in alllist:
        templis= ['' for x in range(attitudelen-1)]
        for i in range(1,attitudelen):
            #0是一个可以变换的数字，有一种严格强度的感觉
            att1 = item['attitudeChange'][i-1]['attitude']
            att2 = item['attitudeChange'][i]['attitude']
            
            
            if (att2 == 1 and att1 == 1) or (att2 == 0 and att1 == 0) or (att2 == -1 and att1 == -1):
                # down -> down positive->postive 0->0
                templis[i-1] = 'keep'
            elif (att2 == 1 and att1 == 0) or (att2 == 1 and att1 == -1) or (att2 == -1 and att1 == 0):
                #down -> positive 0->positve down->0
                templis[i-1] = 'up'
            elif (att2 == 0 and att1 == 1) or (att2 == -1 and att1 == 1) or (att2 == 0 and att1 == -1):
                # positive->down 0->down positive->0
                templis[i-1] = 'down'
            
            
            #templis[i-1] = item['msgCountByMonth'][i]['count'] - item['msgCountByMonth'][i-1]['count']
        
        curious.append([item['uid'],templis,int(-1)])
    
#    for item in curious:
#        print(item)
#        print("\n")

    cluster = {}
    cnt = 0
    
    for i in curious:
        for j in curious:
            if i != j:
                flag = 1
                for ttemp1 in range(len(i[1])):
                    if i[1][ttemp1] != j[1][ttemp1]:
                        flag = 0
                        break
                if flag:
                    if i[2] == -1 and j[2] == -1:
                        i[2] = cnt
                        j[2] = cnt
                        cnt += 1
                        cluster[str(i[2])] =  []
                        cluster[str(i[2])].append(i[0])
                        cluster[str(i[2])].append(j[0])
                        
                    elif i[2] == -1 and j[2] != -1:
                        i[2] = j[2]
                        cluster[str(i[2])].append(i[0])
                        
                    elif j[2] == -1 and i[2] != -1:
                        j[2] = i[2]
                        cluster[str(i[2])].append(j[0])
                    else:
                        continue
            
    #cluster -1 
    for i in curious:
        if i[2] == -1:
            try:
                 cluster[str(i[2])].append(i[0])
            except:
                cluster[str(i[2])] =  []
                cluster[str(i[2])].append(i[0])
            
    #print("clusterByAttitudeCurve",cluster)
    return cluster
    
def printDic(dictname, dict):
    print("\n————————————————————————————————————————————————————\n")
    print(dictname)
    for key,value in dict.items():
        print('{key}:{value}'.format(key = key, value = value))
    print("\n————————————————————————————————————————————————————\n")

def jiao(dict1,dict2):
    
    cluster = {}
    cnt = 0
    for key,value in dict1.items():
        #print('{key}:{value}'.format(key = key, value = value))
        for key2,value2 in dict2.items():
            interlist = list(set(value).intersection(set(value2)))
            jiaojigeshu = len(interlist)
            #print(jiaojigeshu)
            if jiaojigeshu >= 10:
                cnt += 1
                cluster[cnt] =  []
                cluster[cnt] += interlist
    print("final",cluster)

def jiao4(dict1,dict2,dict3,dict4):
    cluster = {}
    cnt = 0
    for key,value in dict1.items():
        #print('{key}:{value}'.format(key = key, value = value))
        for key2,value2 in dict2.items():
            for key3,value3 in dict3.items():
            	for key4,value4 in dict4.items():
                
	                interlist1 = list(set(value).intersection(set(value2)))
	                interlist2 = list(set(value3).intersection(set(interlist1)))
	                interlist3 = list(set(value4).intersection(set(interlist2)))
	                jiaojigeshu = len(interlist3)

	                if jiaojigeshu >= 5:#个数
	                    cnt += 1
	                    cluster[cnt] =  []
	                    cluster[cnt] += interlist3
                    
    #print("final",cluster)
    return cluster
    

def clusterByMonthCount(alllist):

    monthlen = 0
    try:
        monthlen = len(alllist[0]['msgCountByMonth'])#每条类似{'key':x月, 'count':4}
        #print(monthlen)
    except:
        print("alllist error")
    
    curious = [] 
    for item in alllist:
        #templis= ['' for x in range(monthlen-1)]
        totalcount = 0
        for i in range(0,monthlen):
            #0是一个可以变换的数字，有一种严格强度的感觉
            
            totalcount += item['msgCountByMonth'][i]['count']

        curious.append([item['uid'],totalcount,int(-1)])
        

    # for item in curious:
    #    print(item)
    #    print("\n")

    cluster = {}
    cnt = 0
    
    for i in curious:
        for j in curious:
            if i != j:
                flag = 1
                
                if abs(i[1] - j[1] > 200):
                    flag = 0


                if flag:
                    if i[2] == -1 and j[2] == -1:
                        i[2] = cnt
                        j[2] = cnt
                        cnt += 1
                        cluster[str(i[2])] =  []
                        cluster[str(i[2])].append(i[0])
                        cluster[str(i[2])].append(j[0])
                        
                    elif i[2] == -1 and j[2] != -1:
                        i[2] = j[2]
                        cluster[str(i[2])].append(i[0])
                        
                    elif j[2] == -1 and i[2] != -1:
                        j[2] = i[2]
                        cluster[str(i[2])].append(j[0])
                    else:
                        continue
    #cluster -1 
    for i in curious:
        if i[2] == -1:
            try:
                 cluster[str(i[2])].append(i[0])
            except:
                cluster[str(i[2])] =  []
                cluster[str(i[2])].append(i[0])
            
    #print("clusterByMonthCount",cluster)
    return cluster



if __name__ == '__main__':
    url = 'http://39.106.90.67:99/api/v1/user/platform/weibo?cur=1&size=999&search=&tag=%255B1%255D'
    url2 = 'http://39.106.90.67:99/api/v1/user/platform/weibo?cur=1&size=100&search=&tag=%255B%255D'
    url3 = 'http://39.106.90.67:99/api/v1/user/platform/twitter?cur=1&size=100&search=&tag=%255B%255D'

    ids = getUid(url=url)
    ids_weibo100 = getUid(url=url2)
    ids_twitter100 = getUid(url=url3)

    totalids = ids+ids_weibo100+ids_twitter100

    print("111",totalids)

    alllist = test(totalids)
#    for item in alllist:
#        print("name:\t",item['username'],end='')
#        print("uid:\t",item['uid'])
    
    #clusterByKeyword(alllist,intersectcount=3)

    dicClusterByActive =  clusterByActive(alllist)
    printDic('dicClusterByActive',dicClusterByActive)
    
    dicClusterByMonthCurve = clusterByMonthCurve(alllist)
    printDic('dicClusterByMonthCurve',dicClusterByMonthCurve)
    dicClusterByAttitudeCurve = clusterByAttitudeCurve(alllist)    
    printDic('dicClusterByAttitudeCurve',dicClusterByAttitudeCurve)


    dicClusterByMonthCount = clusterByMonthCount(alllist)    
    printDic('dicClusterByMonthCount',dicClusterByMonthCount)

    
    eueu = jiao4(dicClusterByActive,dicClusterByMonthCurve,dicClusterByAttitudeCurve,dicClusterByMonthCount)
    

    newdic = {}
    for key,value in eueu.items():
        newdic[key] = []
        for item in value:
            if item in ids:
                newdic[key].append(('营销号',item))
            elif item in ids_weibo100:
                newdic[key].append( ('微博前100',item))
            elif item in ids_twitter100:
                newdic[key].append( ('twitter前100',item))
    #print(newdic)


    

    jsonform = json.dumps(newdic,ensure_ascii=False)
    print(jsonform)
    