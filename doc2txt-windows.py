import os
import sys
import fnmatch
import win32com.client

docPath = ''
txtPath = ''

def convertDocToTxt():
    i = 0
    for root, dirs, files in os.walk(docPath):
        for _dir in dirs:
            pass
        for _file in files:
            if fnmatch.fnmatch(_file, '*.doc'):
                storeFile = txtPath + _file[:-3] + 'txt'
            elif fnmatch.fnmatch(_file, '*.docx'):
                storeFile = txtPath + _file[:-4] + 'txt'
                
            wordFile = os.path.join(root, _file)
            dealer.Documents.Open(wordFile)
            try:
                dealer.ActiveDocument.SaveAs(storeFile, FileFormat=7,Encoding=65001)
            except Exception as e:
                print(e)
            dealer.ActiveDocument.Close()

            os.remove(docPath+_file)
            
            print("正在制作第",i)
            i += 1
 
dealer = win32com.client.gencache.EnsureDispatch('Word.Application')

if __name__== '__main__':

    convertDocToTxt()