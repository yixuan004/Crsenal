#encoding:utf-8

def DBC2SBC(ustring):
    '''
    全角转半角函数
    '''
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if not (0x0021 <= inside_code and inside_code <= 0x7e):
            rstring += uchar
            continue
        rstring += chr(inside_code)
    return rstring


if __name__ == "__main__":
    text1 = '３７５０１部队后勤部供应站'
    text2 = '37501部队后勤部供应站'

    a = DBC2SBC(text1)
    b = DBC2SBC(text2)

    print(a, b)
    print(a==b)
    print(text1.replace('0', '&'))
    print(text2.replace('0', '&'))