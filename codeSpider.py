#-*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QComboBox,
                             QListWidget, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot
import requests
import re
from bs4 import BeautifulSoup

#网页相关操作
URL = "http://www.codeforge.cn"
searchURL = "http://www.codeforge.cn/s/" #这是基础网址，后面还需要加上 str(pagenumber) 和 "/" 和 objSearch
DIR = "/home/ben/test/"
titList = []    #用于储存搜索网页得到的标题
URLList = []    #用于储存搜索网页得到的网址

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
    #QListWidget中选择的序号
    whichChoice = 0
    pagenumber = 1
    curpagenumber = 1
    objSearch = ''
    
    def __init__(self):
        super().__init__()
        self.searchBtn = QPushButton('搜索')
        self.searchEdit = QLineEdit()
        self.searchEdit.setPlaceholderText('请输入搜索关键字，空格分格')
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.searchEdit)
        self.hbox1.addWidget(self.searchBtn)

        self.downBtn = QPushButton('下载')
        self.downBtn.setEnabled(False)
        self.contentLabel = QLabel()
        #设置自动换行
        self.contentLabel.setWordWrap(True)
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
        self.titleList.itemSelectionChanged.connect(self.ListWidgetChange)
        self.behindBtn.clicked.connect(self.behindBtnClicked)
        
        self.setLayout(self.vbox)
        self.resize(400, 400)
        self.setWindowTitle('CodeforgeDown')

    def search(self):
        self.objSearch = ''
        #设置显示的当前网页序号
        self.curpagenumber = 1
        self.objSearch = self.searchEdit.text()
        if len(self.objSearch) < 2:
            QMessageBox.information(self, '提示', '不能输入少于两个字符')
       
        objSearch = re.sub(' ', '+', self.objSearch)
        content = getHtml(searchURL+"1/"+self.objSearch)
        #获取搜索结果总页数
        obj = re.compile('\d+</a> <a href="/s/2')
        res = obj.findall(content)
        self.pagenumber = re.sub('</a> <a href="/s/2', '', res[0])
        for i in range(int(self.pagenumber)):
            self.curBox.addItem(str(i+1))
            
        #获取相关项网址和标题
        obj = re.compile("<a href='.*' title='.*' target")
        res = obj.findall(content)
        for i in res:
        #获得标题
            objTitle = re.compile("title='.*' target")
            mytitle = objTitle.findall(i)
            mytitle = re.sub('title=', '', str(mytitle))
            mytitle = re.sub(' target', '', str(mytitle))
            mytitle = re.sub("'", '', str(mytitle))
            mytitle = re.sub('<font color=red>', '', str(mytitle))
            mytitle = re.sub('</font>', '', str(mytitle))
            titList.append(str(mytitle))
            #获得网址
            objmyURL = re.compile("/\w+/\d+")
            myURL = objmyURL.findall(i)
            URLList.append(str(myURL))
        for i in titList:
            self.titleList.addItem(str(i)[2:-2])
           
        #设置下一页，末页按钮可用
        self.behindBtn.setEnabled(True)
        self.lastBtn.setEnabled(True)

       
    
    def ListWidgetChange(self):
        #downBtn可用
        self.downBtn.setEnabled(True)
        whichChoice = self.titleList.currentRow()
        #临时需要增加的字符串
        tmpAdd = str(URLList[whichChoice + 1])
        #截取从第三个开始到倒数第二个字符之前
        tmpAdd = tmpAdd[2:-2]
        currentURL = URL + tmpAdd
        print(currentURL)
        tmpCon = requests.get(currentURL).text
        print(tmpCon)
        nowobj = re.compile('<META NAME="description" CONTENT=".*">')
        nowCon = nowobj.findall(tmpCon)
        print(nowCon)
        nowCon = str(nowCon)[36:-7]
        nowCon.strip()
        print(nowCon)
        self.contentLabel.setText(nowCon)
      
      
      
    def behindBtnClicked(self):
        if self.curpagenumber == int(self.pagenumber):
            self.behindBtn.setEnabled(False)
            self.lastBtn.setEnabled(False)
            QMessageBox.information(self, '提示', '已经是最后一页了！！！')
        else:
            titList = []
            URLList = []
            self.titleList.clear()
            self.curpagenumber += 1
            content = getHtml(searchURL+self.curpagenumber+"/"+self.objSearch)
            #获取相关项网址和标题
            obj = re.compile("<a href='.*' title='.*' target")
            res = obj.findall(content)
            for i in res:
                #获得标题
                objTitle = re.compile("title='.*' target")
                mytitle = objTitle.findall(i)
                mytitle = re.sub('title=', '', str(mytitle))
                mytitle = re.sub(' target', '', str(mytitle))
                mytitle = re.sub("'", '', str(mytitle))
                mytitle = re.sub('<font color=red>', '', str(mytitle))
                mytitle = re.sub('</font>', '', str(mytitle))
                titList.append(str(mytitle))
                #获得网址
                objmyURL = re.compile("/\w+/\d+")
                myURL = objmyURL.findall(i)
                URLList.append(str(myURL))
            for i in titList:
                self.titleList.addItem(str(i)[2:-2])
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
 
