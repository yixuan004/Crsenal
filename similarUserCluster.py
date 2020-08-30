#encoding:utf-8
import requests as re
import json

def getUid(url):
    '''
    通过对url的get请求，获取用户uid
    input:
        url: 希望获取的查询列表
             例：url = 'http://39.106.90.67:99/api/v1/user/platform/weibo?cur=1&size=999&search=&tag=%255B1%255D'
             营销号界面，通过charles抓包得到
    output:
        ids: url页面中对应的全部用户uid
    '''
    ids = []
    response = re.get(url=url)#注意size 请求多少
    responseJson = json.loads(response.text)
    for item in responseJson['data']['records']:
        ids.append(item['id'])
        
    return ids

def test(ids):
    '''
    简化每个用户的信息
    input:
        ids: 用户id列表
    output:
        alllist: 用户列表，其中每条类似于dic {'uid':xxx, 'username':xxx, 'active':xxx, 'msgCountByMonth':xxx, 'keyChange':xxx, 'attitudeChange':xxx}
    '''
    alllist = []
    
    for id in ids:
        url = 'http://39.106.90.67:99/api/v1/user/' + str(id)
        tempdict = {}

        response = re.get(url=url)
        responseJson = json.loads(response.text)
        
        tempdict['uid'] = responseJson['data']['id'] # uid
        tempdict['username'] = responseJson['data']['username'] # 用户名
        
        ctrlflag = 0
        
        # TODO
        for liu in range(len(responseJson['data']['tags'])):
            if '月活跃' in responseJson['data']['tags'][liu]['tag']:
                tempdict['active'] = responseJson['data']['tags'][liu]['tag'] # x月活跃 不一定是，第一个tags不一定是
                ctrlflag = 1
                break
        if ctrlflag == 0:
            tempdict['active'] = 'noactive'

        tempdict['msgCountByMonth'] = responseJson['data']['msgCountByMonth'] # list 每个月发表的文章数，每条类似{'key':x月, 'count':4}
        tempdict['keyChange'] = responseJson['data']['keyChange'] # list 每个月的关键词，每条类似{'month': '1月', 'keywords': ['抗击', '确诊', '防控']}
        tempdict['attitudeChange'] = responseJson['data']['attitudeChange'] # list 每个月的心情，每条类似{'month': '7月', 'attitude': -1}

        alllist.append(tempdict)
    
    return alllist

def clusterByActive(alllist):
    '''
    依据活跃月份进行聚类
    input:
        alllist: 基于用户uid的列表提取出的用户详细信息，相对用户原始信息有一定简化
    output:
        cluster: 聚类结果，依据item['active']字段来判断哪个是该用户的活跃月份 {'1月活跃':[289,392,360],'2月活跃':[412,233,461],……}
    TODO:
        在目前版本的系统中，Twitter中部分数据没有标出活跃月份（即发帖数最多的月份），需要做到自动识别的功能
    '''
    cluster = {}
    for item in alllist:
        try:
            cluster[item['active']].append(item['uid']) #.append(item) 目前聚类结果只添加了uid，但可以根据item中的字段进行随意添加
        except:
            cluster[item['active']] = []
            cluster[item['active']].append(item['uid']) #.append(item) 目前聚类结果只添加了uid，但可以根据item中的字段进行随意添加
    #print("clusterByActive",cluster)
    return cluster
    
def clusterByKeyword(alllist,similarCount,diffCount):
    '''
    依据关键词进行聚类
    input:
        alllist: 基于用户uid的列表提取出的用户详细信息，相对用户原始信息有一定简化
        similarCount: 设定阈值，当相似词个数大于等于此阈值时，两个用户才被判定相似，与diffCount共同作用
        diffCount: 设定阈值，当不同的词小于等于此个数时，两个用户才被判定相似，与similarCount共同作用
    output:
        cluster: 聚类结果，按照关键词聚类得到的聚类结果{'1':[289,392,360],'2':[412,233,461],……}

    '''
    
    #生成一个所有关键词的列表，例：[新冠，疫情，特朗普，……]
    labelall = []
    for item in alllist:
        for item2 in item['keyChange']:
            for item3 in item2['keywords']:
                if item3 not in labelall:
                    labelall.append(item3)

    #one-hot encoding：对每个用户，对照关键词列表进行one-hot encoding
    lenlabelall = len(labelall)
    curious = [] 
    for item in alllist:
        templis= [0 for x in range(lenlabelall)]
        for item2 in item['keyChange']:
            for item3 in item2['keywords']:
                templis[labelall.index(item3)] = 1
        curious.append([item['uid'],templis,int(-1)])#item['uid']->item

    #cluster 聚类
    cluster = {}
    cnt = 0
    for i in curious:
        for j in curious:
            if i != j: # 列表中两两遍历聚类，不同的两个用户信息才具有聚类价值
                count = 0 # one-hot 编码相同的tag计数
                count2 = 0 # one-hot 编码不同的tag计数
                for index1 in range(len(i[1])):
                    if i[1][index1] == j[1][index1] and j[1][index1]==1: # 遍历tag标签，相同时count += 1
                        count += 1
                    if i[1][index1] != j[1][index1]: # 遍历tag标签，不同时count2 += 1
                        count2 += 1
                        
                if(count>=similarCount and count2<=diffCount): # 相同label大于等于similarCount，不同label小于等于diffCount
                    # 在两者符合聚类规则的情况下
                    
                    if i[2] == -1 and j[2] == -1: # 如果两者的cluster标签都是-1，则置一个新的cluster标签cnt
                        i[2] = cnt
                        j[2] = cnt
                        cnt += 1
                        cluster[str(i[2])] =  []
                        cluster[str(i[2])].append(i[0])
                        cluster[str(i[2])].append(j[0])
                        
                    elif i[2] == -1 and j[2] != -1: # 两者中j的cluster标签不是-1，则把i的cluster标签置为j的，并加入聚类中 【BUG fix】
                        i[2] = j[2]
                        cluster[str(j[2])].append(i[0])
                        
                    elif j[2] == -1 and i[2] != -1: # 两者中i的cluster标签不是-1，则把j的cluster标签置为i的，并加入聚类中
                        j[2] = i[2]
                        cluster[str(i[2])].append(j[0])
                    else:
                        # 可重复，互相加入对方的聚类中
                        cluster[str(j[2])].append(i[0])
                        cluster[str(i[2])].append(j[0])


    #cluster -1 把所有未被聚类到一起的，统一作为其它类进行聚类，cluster标签标志为1
    # for i in curious:
    #     if i[2] == -1:
    #         try:
    #              cluster[str(i[2])].append(i[0])
    #         except:
    #             cluster[str(i[2])] =  []
    #             cluster[str(i[2])].append(i[0])
            
    #print(cluster)
    return cluster
                    

#按照曲线进行聚类，如何判断两个曲线是否是相似的->按照up down？
#按照曲线进行聚类，如何判断两个曲线是否是相似的->按照up down？
def clusterByMonthCurve(alllist):
    '''
    按照活跃月份的变化趋势进行聚类，判断规则为up,down,keep
    input:
        alllist: 基于用户uid的列表提取出的用户详细信息，相对用户原始信息有一定简化
    output:
        cluster: 聚类结果，按照月份趋势聚类得到的聚类结果{'1':[289,392,360],'2':[412,233,461],……}
    TODO:
        目前的匹配规则是最严格的匹配规则，即趋势必须相似，后续如有需求，可以放宽此需求
    '''

    monthlen = 0
    try:
        monthlen = len(alllist[0]['msgCountByMonth'])
    except:
        print("alllist error")
    
    curious = [] 
    for item in alllist:
        templis= ['' for x in range(monthlen-1)]
        for i in range(1,monthlen):
            if item['msgCountByMonth'][i]['count'] - item['msgCountByMonth'][i-1]['count'] > 0:
                templis[i-1] = 'up'
            elif item['msgCountByMonth'][i]['count'] - item['msgCountByMonth'][i-1]['count'] == 0:
                templis[i-1] = 'keep'
            elif item['msgCountByMonth'][i]['count'] - item['msgCountByMonth'][i-1]['count'] < 0:
                templis[i-1] = 'down'
        
        curious.append([item['uid'],templis,int(-1)]) # [886, ['keep', 'keep', 'keep', 'keep', 'keep', 'up'], -1] id 同 月份曲线变化状态对应
        
    # 基本同关键词聚类
    cluster = {}
    cnt = 0
    for i in curious:
        for j in curious:
            if i != j:
                flag = 1
                for index1 in range(len(i[1])):
                    if i[1][index1] != j[1][index1]:
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
                        cluster[str(j[2])].append(i[0]) # 【BUG fix】
                    elif j[2] == -1 and i[2] != -1:
                        j[2] = i[2]
                        cluster[str(i[2])].append(j[0])
                    else:
                        continue
    #cluster -1 

            
    #print("clusterByMonthCurve",cluster)
    return cluster

    

def clusterByAttitudeCurve(alllist):
    '''
    按照心情的变化趋势进行聚类，判断规则为up,down,keep
    input:
        alllist: 基于用户uid的列表提取出的用户详细信息，相对用户原始信息有一定简化
    output:
        cluster: 聚类结果，按照心情趋势聚类得到的聚类结果{'1':[289,392,360],'2':[412,233,461],……}
    TODO:
        目前的匹配规则是最严格的匹配规则，即趋势必须相似，后续如有需求，可以放宽此需求
    '''
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
            # 0是一个可以变换的数字，有一种严格强度的感觉
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
                    
        curious.append([item['uid'],templis,int(-1)])
    

    cluster = {}
    cnt = 0
    
    for i in curious:
        for j in curious:
            if i != j:
                flag = 1
                for index1 in range(len(i[1])):
                    if i[1][index1] != j[1][index1]:
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
                        cluster[str(j[2])].append(i[0]) # 【BUG fix】
                        
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

def printDic(dictName, dict):
    '''
    词典可视化打印
    input:
        dictName: 字典名称
        dict: 字典
    output：
        None
    '''
    print("\n————————————————————————————————————————————————————\n")
    print(dictName)
    for key,value in dict.items():
        print('{key}:{value}'.format(key = key, value = value))
    print("\n————————————————————————————————————————————————————\n")

def clusterByMonthCount(alllist,threshold):
    '''
    按照月份的发帖数进行聚类，要求同类中的数目不能相差超过阈值
    input:
        alllist: 基于用户uid的列表提取出的用户详细信息，相对用户原始信息有一定简化
        threshold: 阈值，大于此阈值的会被输出
    output:
        cluster: 聚类结果
    bugfix:


    '''

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
        

    cluster = {}
    cnt = 0
    
    for i in curious:
        for j in curious:
            if i != j:
                flag = 1
                
                if abs(i[1] - j[1] > threshold):
                    flag = 0

                # 当两者相差超过阈值时
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
                        cluster[str(j[2])].append(i[0]) # 【BUG fix】
                        
                    elif j[2] == -1 and i[2] != -1:
                        j[2] = i[2]
                        cluster[str(i[2])].append(j[0])
                    else: # 如果两者的都不为-1，互相加入聚类 【BUG fix】
                        # 可重复，互相加入对方的聚类中
                        cluster[str(j[2])].append(i[0])
                        cluster[str(i[2])].append(j[0])
    #cluster -1 
    # for i in curious:
    #     if i[2] == -1:
    #         try:
    #              cluster[str(i[2])].append(i[0])
    #         except:
    #             cluster[str(i[2])] =  []
    #             cluster[str(i[2])].append(i[0])
            
    #print("clusterByMonthCount",cluster)
    return cluster

def intersectFourDict(dict1,dict2,dict3,dict4,threshold):
    '''
    四个词典的取交集，两两互相取，取交集大于threshold的，作为输出，阻止-1的label聚类到其中
    input:
        dict1-4:词典1-4
        threshold: 阈值，大于此阈值的会被输出
    output:
        cluster: 交集后的聚类结果
    BUG:
        Maybe some bug here
    '''
    cluster = {}
    cnt = 0
    for key,value in dict1.items():
        #print('{key}:{value}'.format(key = key, value = value))
        for key2,value2 in dict2.items():
            if key2 == -1:
                continue
            for key3,value3 in dict3.items():
                for key4,value4 in dict4.items():
                    #去重
                    value = list(set(value))
                    value2 = list(set(value2))
                    value3 = list(set(value3))
                    value4 = list(set(value4))

                    interlist1 = list(set(value).intersection(set(value2)))
                    interlist2 = list(set(value3).intersection(set(interlist1)))
                    interlist3 = list(set(value4).intersection(set(interlist2)))
                    jiaojigeshu = len(interlist3)

                    if jiaojigeshu >= threshold: # 取交集大于threshold的，作为输出
                        cnt += 1
                        cluster[cnt] =  []
                        cluster[cnt] += interlist3

                    
    #print("final",cluster)
    return cluster

if __name__ == '__main__':

    url = 'http://39.106.90.67:99/api/v1/user/platform/weibo?cur=1&size=999&search=&tag=%255B1%255D'
    url2 = 'http://39.106.90.67:99/api/v1/user/platform/weibo?cur=1&size=100&search=&tag=%255B%255D'
    url3 = 'http://39.106.90.67:99/api/v1/user/platform/twitter?cur=1&size=100&search=&tag=%255B%255D'

    print("running...")
    ids = getUid(url=url)
    ids_weibo100 = getUid(url=url2)
    ids_twitter100 = getUid(url=url3)

    totalids = ids+ids_weibo100+ids_twitter100
    #totalids = ids_twitter100 # twitter test
    print("totalids（ids+ids_weibo100+ids_twitter100）: ", totalids)


    alllist = test(totalids)
    #print("alllist: ",alllist)
    

    #dicClusterByKeyword = clusterByKeyword(alllist,similarCount=3)
    #printDic('dicClusterByKeyword',dicClusterByKeyword)

    dicClusterByActive =  clusterByActive(alllist)
    #printDic('dicClusterByActive',dicClusterByActive)

    dicClusterByMonthCurve = clusterByMonthCurve(alllist)
    #printDic('dicClusterByMonthCurve',dicClusterByMonthCurve)

    dicClusterByAttitudeCurve = clusterByAttitudeCurve(alllist)    
    #printDic('dicClusterByAttitudeCurve',dicClusterByAttitudeCurve)

    dicClusterByMonthCount = clusterByMonthCount(alllist,threshold=200)    
    #printDic('dicClusterByMonthCount',dicClusterByMonthCount)

    
    eueu = intersectFourDict(dicClusterByActive,dicClusterByMonthCurve,dicClusterByAttitudeCurve,dicClusterByMonthCount,threshold=5)
    
    newdic = {}
    for key,value in eueu.items():
        newdic[key] = []
        for item in value:
            if item in ids:
                newdic[key].append(('营销号',item))
            elif item in ids_weibo100:
                newdic[key].append(('微博前100',item))
            elif item in ids_twitter100:
                newdic[key].append(('twitter前100',item))

    #tranform to json form
    jsonForm = json.dumps(newdic,ensure_ascii=False)
    print(jsonForm)
    