#-*- cofing:utf-8 -*-
import re
import requests
import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QApplication, QListWidget,\
    QPushButton, QVBoxLayout, QHBoxLayout

URL = "http://www.codeforge.cn"
contentList = []



    
class UI(QWidget):
    whichChoice = 0
    titList = []    #用于储存搜索网页得到的标题
    URLList = []    #用于储存搜索网页得到的网址
    
    def __init__(self):
        super().__init__()
        self.getURLAndTitle(requests.get('http://www.codeforge.cn/s/1/线程').text)
        self.curListWidget = QListWidget(self)
        self.Btn1 = QPushButton('first')
        self.Btn2 = QPushButton('next')
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.Btn1)
        self.vbox.addWidget(self.Btn2)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.curListWidget)
        self.hbox.addLayout(self.vbox)
        
        for i in self.titList:
            self.curListWidget.addItem(str(i)[2:-2])
            print(i)
        self.Btn1.clicked.connect(self.btn1)
        self.Btn2.clicked.connect(self.btn2)
        self.setLayout(self.hbox)
        self.setGeometry(200, 200, 400, 300)
        
    def btn1(self):
        self.getURLAndTitle(requests.get('http://www.codeforge.cn/s/2/线程').text)
        self.curListWidget.clear()
        for i in self.titList:
            self.curListWidget.addItem(str(i)[2:-2])
            print(i)
        
    def btn2(self):
        return
    
    
    #获取相关项网址和标题        
    def getURLAndTitle(self, content):
        self.titList = []
        self.URLList = []
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
            self.titList.append(str(mytitle))
            #获得网址
            objmyURL = re.compile("/\w+/\d+")
            myURL = objmyURL.findall(i)
            self.URLList.append(str(myURL))
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
   
    ui = UI()
    ui.show()
    sys.exit(app.exec_())