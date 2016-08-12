import re
import requests
import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QApplication, QListWidget

content = requests.get("http://www.codeforge.cn/s/1/%E7%BA%BF%E7%A8%8B").text
obj = re.compile("<a href='.*' title='.*' target")
res = obj.findall(content)



class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.curListWidget = QListWidget()
        for i in res:
            self.curListWidget.addItem(i)
        self.curListWidget.move(20, 20)
        
        self.setGeometry(200, 200, 200, 200)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())