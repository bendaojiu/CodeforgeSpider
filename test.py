#-*- cofing:utf-8 -*-
import re
import requests
import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QApplication, QListWidget

URL = "http://www.codeforge.cn"
contentList = []
titList = []    #用于储存搜索网页得到的标题
URLList = []    #用于储存搜索网页得到的网址

content = requests.get("http://www.codeforge.cn/s/1/线程").text
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
    
class UI(QWidget):
    whichChoice = 0
    
    def __init__(self):
        super().__init__()
        self.curListWidget = QListWidget(self)
        for i in titList:
            self.curListWidget.addItem(str(i))
        self.curListWidget.itemSelectionChanged.connect(self.test)
        self.curListWidget.move(20, 20)
        
        self.setGeometry(200, 200, 200, 200)
        
        
    def test(self):
        whichChoice = self.titleList.currentRow()
        currentURL = URL + str(URLList(whichChoice + 1))[2:-2]
        print(currentURL)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())