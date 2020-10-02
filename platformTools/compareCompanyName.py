#encoding:utf-8
#短文本相似度检索：https://ai.baidu.com/tech/nlp_basic/simnet
#sudo pip3 install requests
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


def compareCompanyName(accessToken, text_1, text_2):

	basicURL = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?'
	accessTokenURL = 'access_token=' + accessToken
	postURL = basicURL + accessTokenURL

	args = {
		'text_1': text_1,
		'text_2': text_2
	}

	data = json.dumps(args).encode('utf-8')
	response = requests.post(url=postURL, data=data)
	print(response.json())

if __name__ == '__main__':

	clientId = ''
	clientSecret = ''
	accessToken = getAccessToken(clientId, clientSecret)
	#提供了一种按照score排序的可能，问题是检索一次数据库，反复调用compare接口恐怕会消耗过多次数，如何避免
	compareCompanyName(accessToken, '广州恒大', '广州恒大淘宝')