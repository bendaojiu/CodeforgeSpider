#-*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QComboBox,
                             QListWidget, QLabel, QMessageBox)
import requests
import re
from bs4 import BeautifulSoup

#网页相关操作
pagenumber = 1
objSearch = "abc"
URL = "www.codeforge.cn"
objURL = "http://www.codeforge.cn/article/185551"
searchURL = "http://www.codeforge.cn/s/"+str(pagenumber)+"/"+objSearch
DIR = "/home/ben/test/"

#获取网页源码
def getHtml(url):
    r = requests.get(url)
    return r.text

#获取文件地址
def getFileURL(text):
    obj = re.compile('/read/\d+/\w+.\w+_html')
    #print text
    return obj.findall(text)

#获取文件名
def getFileName(text):
    obj = re.compile('\w+\.\w{1,3}')
    return obj.search(text).group()

#获取文件内容
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

#创建工程文件夹
#def MakeProject(name, path):
#创建文件并写入内容
#def MakeFile(name, content):
class UI(QWidget):
    def __init__(self):
        super().__init__()
        searchBtn = QPushButton('搜索')
        searchBtn.clicked.connect(self.search())
        searchEdit = QLineEdit('请输入搜索内容', self)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(searchEdit)
        hbox1.addWidget(searchBtn)

        downBtn = QPushButton('下载')
        downBtn.setEnabled(False)
        contentLabel = QLabel()
        vbox2 = QVBoxLayout()
        vbox2.addWidget(contentLabel)
        vbox2.addWidget(downBtn)

        titleList = QListWidget()
        hbox2 = QHBoxLayout()
        hbox2.addWidget(titleList)
        hbox2.addLayout(vbox2)

        firstBtn = QPushButton('首页')
        firstBtn.setEnabled(False)
        preBtn = QPushButton('前一页')
        preBtn.setEnabled(False)
        curBox = QComboBox()
        behindBtn = QPushButton('下一页')
        behindBtn.setEnabled(False)
        lastBtn = QPushButton('末页')
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
            QMessageBox.Information(self, tr('提示'), tr('不能输入少于两个字符'))
            return
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    print('hello')
    sys.exit(app.exec_())
 
