import requests #line:2
from bs4 import BeautifulSoup #line:3
import urllib .parse #line:4
import re #line:5
import time #line:6
from tqdm import tqdm #line:7
def getUserBasicInfo (OO0OOO0000O0OO000 ):#line:9
    ""#line:13
    pass #line:14
def getUserSameFollowList (O0O000O000O00000O ):#line:16
    ""#line:24
    OO0OO0000OO0O0O0O ='https://weibo.com/p/'+str (O0O000O000O00000O )+'/follow?relate=same_follow&from=rel&wvr=5&loc=bothfollow'#line:25
    O0OOOO0O0OOO000O0 ={'Host':'weibo.com','Cookie':'your cookie','cache-control':'max-age=0','sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"','sec-ch-ua-mobile':'?0','upgrade-insecure-requests':'1','user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','sec-fetch-site':'same-origin','sec-fetch-mode':'navigate','sec-fetch-user':'?1','sec-fetch-dest':'document','accept-language':'zh-CN,zh;q=0.9'}#line:42
    time .sleep (2 )#line:43
    O0000O00OOOOO0O0O =requests .request ("GET",OO0OO0000OO0O0O0O ,headers =O0OOOO0O0OOO000O0 ,data ={})#line:44
    with open ('/Users/curious/Desktop/WeiboSpyder/test/'+str (O0O000O000O00000O )+'.txt','a+',encoding ='utf-8')as OO000O000O0O000OO :#line:47
        OO000O000O0O000OO .write (O0000O00OOOOO0O0O .text )#line:48
    OOO00OOO00OOOO0O0 =''#line:51
    with open ('/Users/curious/Desktop/WeiboSpyder/test/'+str (O0O000O000O00000O )+'.txt','r',encoding ='utf-8')as O0OO0OO000O0O0OOO :#line:52
        OO0O0OOOOO000O0O0 =O0OO0OO000O0O0OOO .readlines ()#line:53
        for OO0O0OOOO0OO0OO00 ,O00OO0000OOO00O00 in enumerate (OO0O0OOOOO000O0O0 ):#line:54
            O00OO0000OOO00O00 =O00OO0000OOO00O00 .strip ()#line:55
            if O00OO0000OOO00O00 .startswith ('<script>FM.view({\"ns\":\"pl.content.followTab.index'):#line:56
                OOO00OOO00OOOO0O0 =eval (O00OO0000OOO00O00 .replace (r'<script>FM.view(','').replace (r')</script>',''))['html'].replace ("<\\",'<')#line:57
                with open ("/Users/curious/Desktop/WeiboSpyder/test/jjjj.html",'a+',encoding ='utf-8')as OO000O000O0O000OO :#line:58
                    OO000O000O0O000OO .write (OOO00OOO00OOOO0O0 )#line:59
                break #line:60
    O0OO0OOOOO00O0OO0 =BeautifulSoup (OOO00OOO00OOOO0O0 ,"lxml")#line:62
    OO0O0O000OO00OOO0 =False #line:64
    O0O0OO0OOO0OO0OOO =False #line:65
    OOOO0OO00O0O00O0O =False #line:66
    for OO0O0OOOO0OO0OO00 in range (1 ,20 ):#line:68
        OOOO00O0OO0O0O0O0 ='body > div > div > div > div.follow_box > div > ul > li:nth-child('+str (OO0O0OOOO0OO0OO00 )+') > dl > dd.mod_info.S_line1'#line:69
        OOOOO00O0O0O0O0O0 =OOOO00O0OO0O0O0O0 +' > div.info_name.W_fb.W_f14 > a.S_txt1'#line:70
        try :#line:73
            O00O00OO0OOOOO0OO =str (O0OO0OOOOO00O0OO0 .select (OOOOO00O0O0O0O0O0 )[0 ])#line:74
            O0O00OO0O0O0OO0O0 =re .match (r'(.*)>(.*)<(.*)',O00O00OO0OOOOO0OO ,re .M |re .I )#line:75
            O0O0OOOOOO00O0O0O =O0O00OO0O0O0OO0O0 .group (2 )#line:76
            if O0O0OOOOOO00O0O0O =='人民日报':#line:77
                O0O0OO0OOO0OO0OOO =True #line:78
            if O0O0OOOOOO00O0O0O =='央视新闻':#line:79
                OOOO0OO00O0O00O0O =True #line:80
            if len (O0O0OOOOOO00O0O0O ):#line:81
                with open ("/Users/curious/Desktop/WeiboSpyder/test/curious.txt",'a+',encoding ='utf-8')as OO000O000O0O000OO :#line:82
                    OO000O000O0O000OO .write (O0O0OOOOOO00O0O0O +'\n')#line:83
        except :#line:84
            break #line:85
    if O0O0OO0OOO0OO0OOO and OOOO0OO00O0O00O0O :#line:87
        OO0O0O000OO00OOO0 =True #line:88
    return OO0O0O000OO00OOO0 #line:90
def getUserFollowList (OO00O0OO0OO0000O0 ,OOO0OOO0O0OOOOO00 ):#line:92
    ""#line:96
    O0OO0O0OOOOO00OOO =0 #line:139
    time .sleep (2 )#line:142
    for OO0O000OO00OO0OOO in range (1 ,6 ):#line:143
        O0000OOOOO0O00O0O ={'Host':'weibo.com','Cookie':'your cookie','sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"','sec-ch-ua-mobile':'?0','upgrade-insecure-requests':'1','user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','sec-fetch-site':'same-origin','sec-fetch-mode':'navigate','sec-fetch-dest':'iframe','accept-language':'zh-CN,zh;q=0.9'}#line:157
        O0O000O0O0OO0O00O ='https://weibo.com/p/'+str (OO00O0OO0OO0000O0 )+'/follow?pids=Pl_Official_HisRelation__57&page='+str (OO0O000OO00OO0OOO )#line:158
        O00O00OOO000OO0OO =requests .request ("GET",O0O000O0O0OO0O00O ,headers =O0000OOOOO0O00O0O ,data ={})#line:159
        time .sleep (2 )#line:160
        with open ('/Users/curious/Desktop/WeiboSpyder/UserFollowList/'+str (OO00O0OO0OO0000O0 )+'_page&'+str (OO0O000OO00OO0OOO )+'FollowList.txt','a+',encoding ='utf-8')as O00000OOO00O00O00 :#line:163
            O00000OOO00O00O00 .write (O00O00OOO000OO0OO .text )#line:164
        OO00O000OO000O00O =''#line:167
        with open ('/Users/curious/Desktop/WeiboSpyder/UserFollowList/'+str (OO00O0OO0OO0000O0 )+'_page&'+str (OO0O000OO00OO0OOO )+'FollowList.txt','r',encoding ='utf-8')as O0OOOOOOO0000OO0O :#line:168
            O00OOO0OO0O00OOO0 =O0OOOOOOO0000OO0O .readlines ()#line:169
            for OO0O000OO00OO0OOO ,OO0O00OO000O0OO0O in enumerate (O00OOO0OO0O00OOO0 ):#line:170
                OO0O00OO000O0OO0O =OO0O00OO000O0OO0O .strip ()#line:171
                if OO0O00OO000O0OO0O .startswith ('<script>FM.view({\"ns\":\"pl.content.followTab.index'):#line:172
                    OO00O000OO000O00O =eval (OO0O00OO000O0OO0O .replace (r'<script>FM.view(','').replace (r')</script>',''))['html'].replace ("<\\",'<')#line:173
        OO0O0OOOO00O000O0 =BeautifulSoup (OO00O000OO000O00O ,"lxml")#line:175
        for OO00OO000O0O0OOOO in range (1 ,20 ):#line:178
            try :#line:179
                O0O0O000OOOO00O0O ='body > div > div > div > div.follow_box > div.follow_inner > ul > li:nth-child('+str (OO00OO000O0O0OOOO )+') > dl > dd.mod_info.S_line1'#line:180
                OOO0OOO00O000OO00 =O0O0O000OOOO00O0O +' > div.info_name.W_fb.W_f14 > a.S_txt1'#line:183
                OOO000000O0OO0000 =str (OO0O0OOOO00O000O0 .select (OOO0OOO00O000OO00 )[0 ])#line:184
                OO0OOOOO00OO00O00 =re .match (r'(.*)>(.*)<(.*)',OOO000000O0OO0000 ,re .M |re .I )#line:187
                OO000O000OOO0O0OO =OO0OOOOO00OO00O00 .group (2 )#line:188
                O0OO00000OOOOO0OO =re .match (r'(.*)id=(.*)&amp(.*)',OOO000000O0OO0000 ,re .M |re .I )#line:190
                OO00OOOOO0O00O000 =O0OO00000OOOOO0OO .group (2 )#line:191
                with open (OOO0OOO0O0OOOOO00 ,'a+',encoding ='utf-8')as O00000OOO00O00O00 :#line:193
                    O00000OOO00O00O00 .write (OO00OOOOO0O00O000 +','+OO000O000OOO0O0OO +'\n')#line:194
                O0OO0O0OOOOO00OOO +=1 #line:195
            except :#line:196
                continue #line:197
    return O0OO0O0OOOOO00OOO #line:205
def getUserWeiboContent (OO00OO0OOO0OO0000 ,OOO0OOOO0O0OO0O0O ,O00O0O0OOO0OOOOO0 ):#line:207
    ""#line:211
    pass #line:212
if __name__ =='__main__':#line:214
    totalCount =0 #line:216
    with open ('3wuid.txt','r',encoding ='utf-8')as reader :#line:217
        lines =reader .readlines ()#line:218
        for i ,line in enumerate (lines ):#line:219
            line =line .strip ()#line:220
            uid ,userName =line .split (',')#line:221
            with open ('4wuid.txt','a+',encoding ='utf-8')as writer :#line:223
                writer .write (uid +','+userName +'\n')#line:224
            count1 =getUserFollowList ('100505'+uid ,'4wuid.txt')#line:229
            time .sleep (2 )#line:230
            count2 =getUserFollowList ('100206'+uid ,'4wuid.txt')#line:234
            totalCount +=1 +count1 +count2 #line:235
            print ("本次获取到："+'1, '+str (count1 )+', '+str (count2 )+'共 '+str (1 +count1 +count2 )+' 条数据')#line:236
            print ("共获取到："+str (totalCount )+' 条数据')