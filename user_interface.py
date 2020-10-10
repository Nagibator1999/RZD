import sys
import os
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QListWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLineEdit, QLabel, QTreeView, QTreeWidgetItem, QTreeWidget, 
                            QAbstractItemView)
from PyQt5.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import QCoreApplication, QDir, Qt, QDataStream

import db

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Конфигурация показа'
        self.top = 200
        self.left = 500
        self.width = 800
        self.height = 600
        self.listOfChilds = list()
        self.initUI()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение', "Вы точно хотите выйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def onSelectionChanged(self, value):
        for sel in self.treeSystems.selectedIndexes():
            # val = '/'+sel.data()
            # print(sel.child(0,0))
            # while sel.parent().isValid():
            #     sel = sel.parent()
            #     val = '/' + sel.data() + val
            # print(sel)
            index = 0
            while sel.child(index,0).isValid():
                selChild = sel.child(index,0)
                self.listOfChilds.append(selChild.data())
                index += 1
            print(self.listOfChilds)

    def initUI(self):
        # selectedTreeElemStyleSheet = '''.QStandardItem {background-color: blue}'''
        centralButtonsSS = 'max-width: 20%; padding: 6px; margin: 10px; border-radius: 5px; border: 1px solid black'
        self.setStyleSheet(open(os.path.join(os.path.dirname(__file__), 'style.css')).read())

        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        vboxList = QVBoxLayout()
        self.labelSignalSelection = QLabel('Выбор сигнала')
        self.labelSystems = QLabel('Системы')

        '-------------------------ListWidget---------------------------'
        self.treeSystems = QTreeWidget()
        self.treeSystems.setAlternatingRowColors(1)
        self.treeSystems.setHeaderHidden(1)
        self.treeSystems.setColumnCount(1)
        self.treeSystems.setSelectionMode(QAbstractItemView.MultiSelection)
        self.treeSystems.selectionModel().selectionChanged.connect(self.onSelectionChanged)

        #проеверь чтобы postgres был запущен
        kks = db.MPK.select_column('KKS', False, False, False)
        kks = set(kks)
        for record in kks:
            row = QTreeWidgetItem(self.treeSystems, [record])
            self.treeSystems.addTopLevelItem(row)
            suffics = set(db.MPK.select_column('Суффикс', 'KKS', record, False))
            for elem in suffics:
                child = QTreeWidgetItem(row, [elem])
                row.addChild(child)   
        '----------------------------ListWidget--------------------------'

        self.labelSelected = QLabel('Выбрано: 0 групп, 0 сигналов')
        self.labelSearch = QLabel('Поиск')
        self.labelDesignProtocolSignals = QLabel('Сигналы проектных протоколов')
        self.labelStoredProtocols = QLabel('Сохраненные протоколы')
        widgets = (self.labelSignalSelection, self.labelSystems, self.treeSystems, self.labelSelected, self.labelSearch, self.labelDesignProtocolSignals, self.labelStoredProtocols)
        for widget in widgets:
            vboxList.addWidget(widget)

        vbox4Btn = QVBoxLayout()
        self.btnRigth = QPushButton('>', self)
        self.btnRigth.setStyleSheet(centralButtonsSS)
        self.btnLeft = QPushButton('<', self)
        self.btnLeft.setStyleSheet(centralButtonsSS)
        self.btnRigthAll = QPushButton('>>', self)
        self.btnRigthAll.setStyleSheet(centralButtonsSS)
        self.btnLeftAll = QPushButton('<<', self)
        self.btnLeftAll.setStyleSheet(centralButtonsSS)

        widgets = (self.btnRigth, self.btnLeft, self.btnRigthAll, self.btnLeftAll)
        for widget in widgets:
            vbox4Btn.addWidget(widget)

        vboxSelectedList = QVBoxLayout()
        self.labelSelectedSignals = QLabel('Выбранные сигналы')
        self.listSelectedSignals = QListWidget()
        self.labelHowMuchSelected = QLabel('Выбрано 3 из 3')
        widgets = (self.labelSelectedSignals, self.listSelectedSignals, self.labelHowMuchSelected)
        for widget in widgets:
            vboxSelectedList.addWidget(widget)
        
        hboxLists = QHBoxLayout()
        layouts = (vboxList, vbox4Btn, vboxSelectedList)
        for lay in layouts:
            hboxLists.addLayout(lay)

        hboxInputLine = QHBoxLayout()
        self.labelDescription = QLabel('Описание')
        self.inputLine = QLineEdit(self)
        widgets = (self.labelDescription, self.inputLine)
        for widget in widgets:
            hboxInputLine.addWidget(widget)

        hboxBottomButtons = QHBoxLayout()
        self.buttonOK = QPushButton('OK', self)
        self.buttonCancel = QPushButton('Отмена', self)
        hboxBottomButtons.addStretch(1)
        widgets = (self.buttonOK, self.buttonCancel)
        for widget in widgets:
            hboxBottomButtons.addWidget(widget)

        mainVBox = QVBoxLayout()
        layouts = (hboxLists, hboxInputLine, hboxBottomButtons)
        for lay in layouts:
            mainVBox.addLayout(lay)

        self.setLayout(mainVBox)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())