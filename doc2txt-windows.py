import os
import sys
import fnmatch
import win32com.client

#PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
doc_path = 'C:\\Users\\Administrator\\Desktop\\a\\ALL\\'
txt_path = 'C:\\Users\\Administrator\\Desktop\\b\\'

def convert_dir_to_txt():
    """
    将默认整个文件夹下的文件都进行转换
    :return:
    """
    i = 0
    for root, dirs, files in os.walk(doc_path):
        for _dir in dirs:
            pass
        for _file in files:
            if fnmatch.fnmatch(_file, '*.doc'):
                store_file = txt_path + _file[:-3] + 'txt'
            elif fnmatch.fnmatch(_file, '*.docx'):
                store_file = txt_path + _file[:-4] + 'txt'
            word_file = os.path.join(root, _file)
            dealer.Documents.Open(word_file)
            try:
                dealer.ActiveDocument.SaveAs(store_file, FileFormat=7,Encoding=65001)
            except Exception as e:
                print(e)
            dealer.ActiveDocument.Close()
            #print()
            os.remove(doc_path+_file)
            print("正在制作第",i)
            i += 1
 
dealer = win32com.client.gencache.EnsureDispatch('Word.Application')


if __name__== '__main__':

    convert_dir_to_txt()