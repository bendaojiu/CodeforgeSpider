#-*- cofing:utf-8 -*-
import re
import requests
import sys, os
from PyQt5.QtWidgets import QWidget, QComboBox, QApplication, QListWidget,\
    QPushButton, QVBoxLayout, QHBoxLayout
from bs4 import BeautifulSoup

fileName = 'Modbus.h__html'
filename = ''
for i in fileName:
    if i != '_':
        filename = filename + i
    else:
        break
print(filename)