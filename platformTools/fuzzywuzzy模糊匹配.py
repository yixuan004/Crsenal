#encoding:utf-8
#sudo pip3 install fuzzywuzzy
#fuzzywuzzy中的匹配都是不带有语义的匹配方式,匹配准确度效果极为有限，但是为了检索效率和直接精确匹配，却也是不得不使用的办法？
#最终目标要实现的搜索，感觉难度超过了预期

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def demo():

	#简单匹配 fuzz.ratio("this is a test", "this is a test!")
	print(fuzz.ratio("this is a test", "this is a test!"))

	#非完全匹配 fuzz.partial_ratio("this is a test", "this is a test!")
	print(fuzz.partial_ratio("this is a test", "this is a test!"))

	#忽略顺序匹配 fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
	print(fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear"))

	#去除子集匹配 fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
	print(fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear"))

def matchCompanyName(companyName1, companyName2):

	return fuzz.token_sort_ratio(companyName1, companyName2)


if __name__ == '__main__':
	#demo()
	result = matchCompanyName("sentence1","sentence2")
	print(result)
