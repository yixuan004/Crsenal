def calculateCommonSubstr(str1, str2):
    '''
    计算两个字符串之间的【最长】【连续】【公共】【子序列】（最长公共子串），假定str1为'额长江信息'
    str2为'长江信息网络科技有限公司'时，希望计算结果为4
    str2为'长江农场劳动服务所信息室'时，希望计算结果为2
    '''
    # init
    len1, len2 = len(str1), len(str2)
    dp = [[0 for i in range(len2+1)] for j in range(len1+1)] # 动态规划矩阵，多一位
    lenMaxSubstring = 0
    commonSubstr = ''
    p = 0
    
    # calculate
    for i in range(len1):
        for j in range(len2):
            if str1[i] == str2[j]:
                # 相同则累加
                dp[i+1][j+1] = dp[i][j] + 1
                if dp[i+1][j+1] > lenMaxSubstring:
                    # 获取最大匹配长度
                    lenMaxSubstring = dp[i+1][j+1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    commonSubstr = str1[p-lenMaxSubstring: p]
    return commonSubstr, lenMaxSubstring

if __name__ == '__main__':
    
    commonSubstr, lenMaxSubstring = calculateCommonSubstr(
        str1 = '额呃呃呃呃呃',
        str2 = '长江农场劳动服务所信息室' 
    )
    print("commonSubstr", commonSubstr)
    print("lenMaxSubstring", lenMaxSubstring)