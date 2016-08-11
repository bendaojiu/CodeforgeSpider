#-*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QComboBox,
                             QListWidget, QLabel, QMessageBox)
import requests
import re
from bs4 import BeautifulSoup

#��ҳ��ز���
pagenumber = 1
objSearch = "abc"
URL = "www.codeforge.cn"
objURL = "http://www.codeforge.cn/article/185551"
searchURL = "http://www.codeforge.cn/s/"+str(pagenumber)+"/"+objSearch
DIR = "/home/ben/test/"

#��ȡ��ҳԴ��
def getHtml(url):
    r = requests.get(url)
    return r.text

#��ȡ�ļ���ַ
def getFileURL(text):
    obj = re.compile('/read/\d+/\w+.\w+_html')
    #print text
    return obj.findall(text)

#��ȡ�ļ���
def getFileName(text):
    obj = re.compile('\w+\.\w{1,3}')
    return obj.search(text).group()

#��ȡ�ļ�����
def getContent(text):
    soup = BeautifulSoup(text)
    return soup.pre.string

def getProjectName(text):
    soup = BeautifulSoup(text)
    a = soup.title.string
    b = ""
    for i in a:
        if i == " ":
            break
        else:
            b = b+i
    return b

#���������ļ���
#def MakeProject(name, path):
#�����ļ���д������
#def MakeFile(name, content):
class UI(QWidget):
    def __init__(self):
        super().__init__()
        searchBtn = QPushButton('����')
        searchBtn.clicked.connect(self.search())
        searchEdit = QLineEdit('��������������', self)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(searchEdit)
        hbox1.addWidget(searchBtn)

        downBtn = QPushButton('����')
        downBtn.setEnabled(False)
        contentLabel = QLabel()
        vbox2 = QVBoxLayout()
        vbox2.addWidget(contentLabel)
        vbox2.addWidget(downBtn)

        titleList = QListWidget()
        hbox2 = QHBoxLayout()
        hbox2.addWidget(titleList)
        hbox2.addLayout(vbox2)

        firstBtn = QPushButton('��ҳ')
        firstBtn.setEnabled(False)
        preBtn = QPushButton('ǰһҳ')
        preBtn.setEnabled(False)
        curBox = QComboBox()
        behindBtn = QPushButton('��һҳ')
        behindBtn.setEnabled(False)
        lastBtn = QPushButton('ĩҳ')
        lastBtn.setEnabled(False)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(firstBtn)
        hbox3.addWidget(preBtn)
        hbox3.addWidget(curBox)
        hbox3.addWidget(behindBtn)
        hbox3.addWidget(lastBtn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)
        self.show()

    def search(self):
        if len(self.searchEdit.getText()) < 2:
            QMessageBox.Information(self, tr('��ʾ'), tr('�����������������ַ�'))
            return
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    print('hello')
    sys.exit(app.exec_())
 
