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
searchURL = "http://www.codeforge.cn/s/" #这是基础网址，后面还需要加上 str(pagenumber) 和 "/" 和 objSearch
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
        self.searchBtn = QPushButton('搜索')
        self.searchEdit = QLineEdit()
        self.searchEdit.setPlaceholderText('请输入搜索内容')
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.searchEdit)
        self.hbox1.addWidget(self.searchBtn)

        self.downBtn = QPushButton('下载')
        self.downBtn.setEnabled(False)
        self.contentLabel = QLabel()
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.contentLabel)
        self.vbox2.addWidget(self.downBtn)

        self.titleList = QListWidget()
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.titleList)
        self.hbox2.addLayout(self.vbox2)

        self.firstBtn = QPushButton('首页')
        self.firstBtn.setEnabled(False)
        self.preBtn = QPushButton('前一页')
        self.preBtn.setEnabled(False)
        self.curBox = QComboBox()
        self.behindBtn = QPushButton('下一页')
        self.behindBtn.setEnabled(False)
        self.lastBtn = QPushButton('末页')
        self.lastBtn.setEnabled(False)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(self.firstBtn)
        self.hbox3.addWidget(self.preBtn)
        self.hbox3.addWidget(self.curBox)
        self.hbox3.addWidget(self.behindBtn)
        self.hbox3.addWidget(self.lastBtn)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        self.searchBtn.clicked.connect(self.search)
        
        self.setLayout(self.vbox)
       

    def search(self):
        if len(self.searchEdit.text()) < 2:
            QMessageBox.Information(self, '提示', '不能输入少于两个字符', QMessageBox.Yes)
        #以上有问题，不能实现检测输入内容是不是小于两个
        objSearch = self.searchEdit.text()
        print(searchURL+"1/"+objSearch)
        #res = getHtml(searchURL+"1/"+objSearch)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
 
