# encoding:utf-8
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
from tqdm import tqdm


def getUserBasicInfo(uid):
    '''
    TODO
    传入一个用户的uid，获取用户的微博名，地区，性别，年龄
    '''
    pass

def getUserSameFollowList(uid):
    '''
    已完成，待测试
    获取共同关注列表，从这里判断是不是两个人都关注了人民日报、央视新闻
    input
    output:
        ifBothFollowRenminYangshi:
            type: boolean
    '''
    url = 'https://weibo.com/p/' + str(uid) + '/follow?relate=same_follow&from=rel&wvr=5&loc=bothfollow'

    headers = {
    'Host': 'weibo.com',
    'Cookie': '',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    # 'referer': 'https://weibo.com/xinhuashidian?refer_flag=1005050006_&is_hot=1',
    'accept-language': 'zh-CN,zh;q=0.9'
    }
    time.sleep(2)
    response = requests.request("GET", url, headers=headers, data={}) # get

    # 
    with open('test/'+str(uid)+'.txt', 'a+', encoding='utf-8') as writer:
        writer.write(response.text)
    
    # 
    sameFollowHtml = ''
    with open('test/'+str(uid)+'.txt', 'r', encoding='utf-8') as reader:
        lines = reader.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('<script>FM.view({\"ns\":\"pl.content.followTab.index'):
                sameFollowHtml = eval(line.replace(r'<script>FM.view(', '').replace(r')</script>', ''))['html'].replace("<\\", '<')
                break
    
    sameFollowListSoup = BeautifulSoup(sameFollowHtml, "lxml") # 转化为html并进行解析
    
    ifBothFollowRenminYangshi = False
    ifFollowRenmin = False
    ifFollowYangshi = False

    for i in range(1, 20):
        baseSelector = 'body > div > div > div > div.follow_box > div > ul > li:nth-child(' + str(i) + ') > dl > dd.mod_info.S_line1'
        nameSelector = baseSelector + ' > div.info_name.W_fb.W_f14 > a.S_txt1'

        # 获取name
        try:
            nameHtml = str(sameFollowListSoup.select(nameSelector)[0])
            matchObj = re.match(r'(.*)>(.*)<(.*)', nameHtml, re.M|re.I)
            name = matchObj.group(2)
            if name == '人民日报':
                ifFollowRenmin = True
            if name == '央视新闻':
                ifFollowYangshi = Trues
            if len(name):
                with open("test/c.txt", 'a+', encoding='utf-8') as writer:
                    writer.write(name + '\n')
        except:
            break
    
    if ifFollowRenmin and ifFollowYangshi:
        ifBothFollowRenminYangshi = True
    
    return ifBothFollowRenminYangshi


def getUserFollowList(uid, outputDir):
    '''
    已完成，待测试
    传入一个用户的uid，获取用户的关注列表，从其中获取到更多用户的uid（实际上是refer+uid）
    '''
    # cookie可能需要定期更换
    # headers = {
    # 'Host': 'weibo.com',
    # 'Cookie': '',
    # 'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    # 'sec-ch-ua-mobile': '?0',
    # 'upgrade-insecure-requests': '1',
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'sec-fetch-site': 'same-origin',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-dest': 'iframe',
    # # 'referer': 'https://weibo.com/p/1005051652011054/follow?from=page_100505&wvr=6&mod=headfollow',
    # 'accept-language': 'zh-CN,zh;q=0.9'
    # }

    # url = 'https://weibo.com/p/' + str(uid) + '/follow?pids=Pl_Official_HisRelation__57&page=1'
    # response = requests.request("GET", url, headers=headers, data={})

    # # 把这个以uid+FollowList.txt的文件名写到一个txt中
    # with open('UserFollowList/' + str(uid) + 'FollowList.txt', 'a+', encoding='utf-8') as writer:
    #     writer.write(response.text)

    # # 从文件中读到那个dict
    # followHtml = ''
    # with open('UserFollowList/' + str(uid) + 'FollowList.txt', 'r', encoding='utf-8') as reader:
    #     lines = reader.readlines()
    #     for i, line in enumerate(lines):
    #         line = line.strip()
    #         if line.startswith('<script>FM.view({\"ns\":\"pl.content.followTab.index'):
    #             followHtml = eval(line.replace(r'<script>FM.view(', '').replace(r')</script>', ''))['html'].replace("<\\", '<')

    # followListSoup = BeautifulSoup(followHtml, "lxml") # 转化为html并进行解析

    # # 当page = 1时，使用这个来获取总的页数：
    # try:
    #     totalPageSelector = 'body > div > div > div > div.follow_box > div.WB_cardpage.S_line1 > div > a:nth-child(9)'
    #     totalPageHtml = str(followListSoup.select(totalPageSelector)[0])
    #     matchObj = re.match(r'(.*)>(.*)<(.*)', totalPageHtml, re.M|re.I)
    #     totalPage = int(matchObj.group(2))
    # except:
    #     totalPage = 1
    count = 0

    # 遍历所有页来获取
    time.sleep(2)
    for i in range(1, 6):
        headers = {
        'Host': 'weibo.com',
        'Cookie': '',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'iframe',
        # 'referer': 'https://weibo.com/p/1005051652011054/follow?from=page_100505&wvr=6&mod=headfollow',
        'accept-language': 'zh-CN,zh;q=0.9'
        }
        url = 'https://weibo.com/p/' + str(uid) + '/follow?pids=Pl_Official_HisRelation__57&page=' + str(i)
        response = requests.request("GET", url, headers=headers, data={})
        time.sleep(2)

        # 把这个以uid+FollowList.txt的文件名写到一个txt中
        with open('UserFollowList/' + str(uid) + '_page&' + str(i) + 'FollowList.txt', 'a+', encoding='utf-8') as writer:
            writer.write(response.text)

        # 从文件中读到那个dict
        followHtml = ''
        with open('UserFollowList/' + str(uid) + '_page&' + str(i) + 'FollowList.txt', 'r', encoding='utf-8') as reader:
            lines = reader.readlines()
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('<script>FM.view({\"ns\":\"pl.content.followTab.index'):
                    followHtml = eval(line.replace(r'<script>FM.view(', '').replace(r')</script>', ''))['html'].replace("<\\", '<')

        followListSoup = BeautifulSoup(followHtml, "lxml") # 转化为html并进行解析


        for j in range(1, 20):           
            try:
                baseSelector = 'body > div > div > div > div.follow_box > div.follow_inner > ul > li:nth-child(' + str(j) + ') > dl > dd.mod_info.S_line1'

                # 获取微博用户名 和微博用户uid
                nameSelector = baseSelector + ' > div.info_name.W_fb.W_f14 > a.S_txt1'
                nameHtml = str(followListSoup.select(nameSelector)[0])
                # print(nameHtml)
                
                nameMatchObj = re.match(r'(.*)>(.*)<(.*)', nameHtml, re.M|re.I)
                name = nameMatchObj.group(2)
                
                idMatchObj = re.match(r'(.*)id=(.*)&amp(.*)', nameHtml, re.M|re.I)
                id = idMatchObj.group(2)

                with open(outputDir, 'a+', encoding='utf-8') as writer:
                    writer.write(id + ',' + name + '\n')
                count += 1
            except:
                continue

            # 获取的关注数
            # 获取粉丝数目
            # 获取微博数目
            # 获取地址 ※
            # 获取性别 ※
            # 获取是否微博会员
    return count


def getUserWeiboContent(uid, startDate, endDate):
    '''
    TODO
    传入一个用户的uid，开始时间（例如202001），截止时间，获取中间用户发的微博数目等信息（做起来之后再看）
    '''
    pass

if __name__ == '__main__':

    totalCount = 0
    with open('uid.txt', 'r', encoding='utf-8') as reader:
        lines = reader.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            uid, userName = line.split(',')

            with open('3wuid.txt', 'a+', encoding='utf-8') as writer:
                writer.write(uid + ',' + userName + '\n')

            count1 = getUserFollowList(
                uid = '100505' + uid, # 100206 100505 选一个能用的
                outputDir = '3wuid.txt'
            )
            time.sleep(2)
            count2 = getUserFollowList(
                uid = '100206' + uid,
                outputDir = '3wuid.txt'
            )
            totalCount += 1 + count1 + count2
            print("本次获取到：" + '1, ' + str(count1)+ ', ' + str(count2) + '共 ' + str(1+count1+count2) + ' 条数据')
            print("共获取到：" + str(totalCount) + ' 条数据')