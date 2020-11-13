from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time


class Vote:

    @staticmethod
    def voteCoin():

        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.link.open_newwindow', 1) # 不打开新的标签页，也请修改webdriver.perf的json文件

        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get('https://www.bilibili.com')
        time.sleep(1)
        driver.maximize_window()
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/span/div/span').click() # 登录按钮XPath

        #扫码登录时间
        time.sleep(20)

        #打开坏女人主页
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/input').send_keys('清漾同学') # 搜索UP主名称
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/div').click() # 点击查询
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[1]/div[2]/ul[1]/li/div[1]/a/div/img').click() # 进入个人主页
        time.sleep(2)

        #进入后遍历每个发布的视频
        #切换进入投稿tab
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/div[1]/a[3]/span[2]').click()
        time.sleep(2)


        for i in range(1,30+1): # 30条
            liXPath = '/html/body/div[2]/div[4]/div/div/div/div[2]/div[3]/div/div/ul[2]/li['+str(i)+']/a[2]'
            #print(liXPath)
            driver.find_element_by_xpath(liXPath).click()
            time.sleep(5)

            #投币
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[3]/div[1]/span[2]/canvas').click() # 点击硬币
            time.sleep(2)

            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div/div/div[2]/div[1]').click() # 1硬币
            time.sleep(2)

            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div/div/div[4]/span').click() # 确定
            time.sleep(2)

            driver.back() # 退回上级
            time.sleep(2)

        #b站默认每页30个，点击下一页，dowhile，暂未实现
        
if __name__ == '__main__':
    Vote.voteCoin()