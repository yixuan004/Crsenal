from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time 
import datetime

def getDataFromWenshuCourt(startYear, startMonth, startDay, endYear, endMonth, endDay):
    
    #登录流程

    #driver = webdriver.Chrome(executable_path='/Users/curious/Desktop/chromedriver') # 创建一个浏览器对象

    #option = ChromeOptions()
    #option.add_experimental_option('excludeSwitches', ['enable-automation'])
    #driver = webdriver.Firefox(executable_path='/Users/curious/Desktop/chromedriver')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.dir', 'd:\\')
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream,application/exe,text/csv,application/pdf,application/x-msexcel,application/excel,application/x-excel, application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c,application/x-msdownload')

    

    driver = webdriver.Firefox(firefox_profile=profile)
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #   "source": """
    #   Object.defineProperty(navigator, 'webdriver', {
    #       get: () => undefined
    #   })
    #   """
    # })

    #driver.get('http://wenshu.court.gov.cn/website/wenshu/181010CARHS5BS3C/index.html?open=login') # 使用浏览器对象对网址发起请求
    driver.get('http://wenshu.court.gov.cn/website/wenshu/181010CARHS5BS3C/index.html?open=login')
    #最大化窗口
    #driver.maximize_window()
    #给时间切换下载地址
    time.sleep(5)

    #首先切换到iframe    
    driver.switch_to.frame('contentIframe')

    #输入文本，导出xpath 
    driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[1]/div/div/div/input').send_keys('账号账号账号')
    driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[2]/div/div/div/input').send_keys('密码密码密码%')
    driver.find_element_by_xpath('/html/body/div/div/form/div[3]/span').click()


    time.sleep(5)
    #依据用户的条件进行搜索，在这里进行搜索条件的筛选
    driver.switch_to.default_content() # firefox用
    
    #案由-刑事案由
    driver.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div/div[1]').click()
    #driver.find_element_by_link_text("高级检索").click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="s16"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="1_anchor"]').click()
    time.sleep(1)

    #案件类型-刑事案件
    driver.find_element_by_xpath('//*[@id="s8"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="gjjs_ajlx"]/li[3]').click()
    time.sleep(1)
    
    #审判程序-刑事一审
    driver.find_element_by_xpath('//*[@id="s9"]').click()
    time.sleep(1)   
    driver.find_element_by_xpath('//*[@id="0201_anchor"]').click()
    time.sleep(1)
    
    
    #文书类型-判决书
    driver.find_element_by_xpath('//*[@id="s6"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="gjjs_wslx"]/li[3]').click()
    time.sleep(1)

    
    

    #click 检索
    driver.find_element_by_xpath('//*[@id="searchBtn"]').click()
    time.sleep(10)

    #※※※※※※※※※※※※※※※※※关键词：非法占有
    #非法占有
    driver.find_element_by_xpath('//*[@id="j4_1_anchor"]').click()
    time.sleep(1)
    
    #每页15条
    driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[8]/div/select').click()
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[8]/div/select/option[3]').click()
    time.sleep(5)


    #指定搜索日期范围
    beginDate = datetime.date(startYear, startMonth, startDay)
    endDate = datetime.date(endYear, endMonth, endDay)
    d = beginDate
    delta = datetime.timedelta(days=1)

    while d <= endDate:
        #在这里进行数据的获取     
        nowDate = str(d.strftime("%Y-%m-%d"))
        print("正在获取第%s天的数据"%nowDate)

        #click 高级检索
        driver.find_element_by_xpath('//*[@id="_view_1545034775000"]/div/div[1]/div[1]').click()
        
        #点击1设置日期，注意先clear
        driver.find_element_by_xpath('//*[@id="cprqStart"]').clear()
        driver.find_element_by_xpath('//*[@id="cprqStart"]').send_keys(nowDate)
        time.sleep(1)

        #点击2设置日期，注意先clear
        driver.find_element_by_xpath('//*[@id="cprqEnd"]').clear()
        driver.find_element_by_xpath('//*[@id="cprqEnd"]').send_keys(nowDate)
        time.sleep(1)

        #点击检索
        driver.find_element_by_xpath('//*[@id="searchBtn"]').click()
        time.sleep(2)

        #全选
        driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[2]/div[4]/a[1]/label').click()
        time.sleep(1)
        #批量下载
        driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[2]/div[4]/a[3]').click()
        time.sleep(1)

        #下一页，使用try except作为退出条件
        while 1:    
            try:
                #click下一页
                driver.find_element_by_link_text("下一页").click()
                time.sleep(7)
                #全选
                driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[2]/div[4]/a[1]/label').click()
                time.sleep(4)
                #批量下载
                driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[2]/div[4]/a[3]').click()
                time.sleep(2)

            except:
                break

        time.sleep(2) # 下一天


        d += delta

    driver.quit() # 退出浏览器

if __name__ == '__main__':

    getDataFromWenshuCourt(
        startYear=2014,
        startMonth=1,
        startDay=1,
        endYear=2014,
        endMonth=12,
        endDay=31
    )