#encoding:utf-8
#词法分析：https://ai.baidu.com/tech/nlp/lexical
import requests
import json


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

	#筛选公司集团名称,但是当一句话中含有多个公司名称时，该如何进行筛选
	#->像数据库中传多条数据
	# 公司名；时间；公司新闻；
	for item in response['items']:
		if item['ne'] == 'ORG':
			#每着调一条机构名，就把这句话写进去一次数据库
			print(item['item'])

if __name__ == '__main__':
	clientId = ''
	clientSecret = ''
	accessToken = getAccessToken(clientId, clientSecret)

	sentence = '据港交所文件：百胜中国已通过港交所聆讯。'
	getCompanyNameFromSentence(accessToken, sentence)