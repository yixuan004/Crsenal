#encoding:utf-8
#CSV文件进一步预处理，设置为适合导入db的模式
import requests
import json
import time as timetime
import csv
import codecs
import sys
import pandas as pd

def getAccessToken(clientId, clientSecret):

	basicURL = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'
	clientIdURL = '&client_id=' + clientId
	clientSecretURL = '&client_secret=' + clientSecret

	tokenURL = basicURL + clientIdURL + clientSecretURL
	response = requests.get(tokenURL)
	accessToken = response.json()['access_token']

	return accessToken

def getCompanyNameFromSentence(accessToken, sentence):

	basicURL = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?'
	accessTokenURL = 'access_token=' + accessToken
	postURL = basicURL + accessTokenURL

	args = {
		'text': sentence
	}
	data = json.dumps(args).encode('utf-8')
	response = requests.post(url=postURL, data=data).json()

	return response['items']

def csvPretreatment(inputCsvFile, outputCsvFile, idCount, accessToken):

	file =open(inputCsvFile,'r') # sinaFinance7x24_2_.csv
	lines=file.readlines()
	file.close()

	print(len(lines))

	listId = []
	listCompanyName = []
	listTime = []
	listCompanyNews = []

	for line in lines:
		item = line.split(',')
		try:
			companyNews = str(item[-1])
			response = getCompanyNameFromSentence(accessToken, companyNews)
			timetime.sleep(1) # qps problem

			listORG = []
			for itemt in response:
				if itemt['ne'] == 'ORG': # 这个步骤要加入一个去重算法，否则将会有大批冗余数据混在数据中
					listORG.append(itemt['item'])
			
			listORG = list(set(listORG))
			print(listORG)

			for itemt in listORG:
				#每找到一条机构名，就把这句话写进去一次数据库
				companyName = str(itemt)
				id = str(idCount)
				time = str(item[1])
				
				#print(id, companyName, time, companyNews)
				#write into csv file
				print("正在写入第%d条数据"%(idCount))
				listId.append(id)
				listCompanyName.append(companyName)
				listTime.append(time)
				listCompanyNews.append(companyNews)

				idCount += 1
		except:
			print("ERROR")

	dataframe = pd.DataFrame({'id':listId,'companyName':listCompanyName,'time':listTime,'companyNews':listCompanyNews})
	dataframe.to_csv(outputCsvFile,index=False,sep=',',encoding="utf_8_sig") # 解决中文乱码、问号问题



if __name__ == '__main__':

	clientId = ''
	clientSecret = ''
	accessToken = getAccessToken(clientId, clientSecret)

	inputCsvFile = '/Users/curious/Desktop/sinaFinance7x24_2_.csv'
	outputCsvFile = '/Users/curious/Desktop/db_sinaFinance7x24_2_.csv'
	idCount = 1

	csvPretreatment(inputCsvFile, outputCsvFile, idCount, accessToken)



