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

    def moveSelectedSignals(self): # добавь еще чтобы выделение снималось
        for sel in self.treeSystems.selectedIndexes():
            item = self.treeSystems.itemFromIndex(sel) # убираем выделение
            item.setSelected(False)

            if (not sel.child(0,0).isValid()): # если нет дочерних элементов
                if (sel.data() not in self.listOfChilds): # если элемент уже добавлен
                    self.listOfChilds.append(sel.data())
                    self.listSelectedSignals.addItem(sel.data())
            else:
                index = 0
                while sel.child(index,0).isValid(): # проходимся по всем дочерним
                    item = self.treeSystems.itemFromIndex(sel.child(index,0)) # убираем выделение
                    item.setSelected(False)
                    selChild = sel.child(index,0).data()
                    if (selChild not in self.listOfChilds): # если элемент уже добавлен
                        self.listOfChilds.append(selChild)
                        self.listSelectedSignals.addItem(selChild)
                    index += 1

    def moveAllSelectedSignals(self):
        for index in range(self.treeSystems.topLevelItemCount()):
            item = self.treeSystems.topLevelItem(index)
            for childIndex in range(item.childCount()):
                childData = item.child(childIndex).data(0,0) # 0,0 потому что элемент у нас туту всего один и дочерних не имеет
                if (childData not in self.listOfChilds):
                    self.listOfChilds.append(childData) 
                    self.listSelectedSignals.addItem(childData)

    def deleteSelectedSignals(self):
        for item in self.listSelectedSignals.selectedItems():
            deletedItem = self.listSelectedSignals.takeItem(self.listSelectedSignals.row(item))
            self.listOfChilds.remove(deletedItem.data(0))

    def deleteAllSelectedSignals(self):
        self.listSelectedSignals.clear()
        self.listOfChilds = []

    def fixSelection(self, modelSelectionOfSelectedItem):
        if len(modelSelectionOfSelectedItem.indexes()) > 0:
            modelIndexOfSelectedItem = modelSelectionOfSelectedItem.indexes()[0]
            item = self.treeSystems.itemFromIndex(modelIndexOfSelectedItem)
            if (item.isSelected()):
                if (modelIndexOfSelectedItem.child(0,0).isValid()):
                    childs = item.childCount()
                    for index in range(childs):
                        childItem = self.treeSystems.itemFromIndex(modelIndexOfSelectedItem.child(index, 0))
                        childItem.setSelected(True) 
        else:
            for sel in self.treeSystems.selectedIndexes():
                item = self.treeSystems.itemFromIndex(sel)
                flag = False
                if (item.isSelected() and item.childCount() > 0):
                    for index in range(item.childCount()):
                        childItem = self.treeSystems.itemFromIndex(sel.child(index, 0))
                        if not childItem.isSelected():
                            flag = True
                if flag:
                    item.setSelected(False)

    # проблемы с отменой выделения родителя
    def countGroupsAndSignals(self, value):
        self.fixSelection(value)

        group = 0
        childs = 0
        for sel in self.treeSystems.selectedIndexes():
            if (not sel.child(0,0).isValid()):
                childs += 1
            else:
                group += 1
                index = 0
                while sel.child(index,0).isValid(): # проходимся по всем дочерним
                    childs += 1
                    index += 1
        self.labelSelected.setText('Выбрано: {0} групп, {1} сигналов'.format(group, childs))

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
        self.treeSystems.selectionModel().selectionChanged.connect(self.countGroupsAndSignals) # это для подсчёта выбранных групп и сигналов

        #проеверь чтобы postgres был запущен
        kks = db.MPK.select_column('Суффикс', False, False, False)
        kks = set(kks)
        for record in kks:
            row = QTreeWidgetItem(self.treeSystems, [record])
            self.treeSystems.addTopLevelItem(row)
            suffics = set(db.MPK.select_column('KKS', 'Суффикс', record, False))
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
        self.btnRigth.clicked.connect(self.moveSelectedSignals)
        
        self.btnLeft = QPushButton('<', self)
        self.btnLeft.setStyleSheet(centralButtonsSS)
        self.btnLeft.clicked.connect(self.deleteSelectedSignals)

        self.btnRigthAll = QPushButton('>>', self)
        self.btnRigthAll.setStyleSheet(centralButtonsSS)
        self.btnRigthAll.clicked.connect(self.moveAllSelectedSignals)
        
        self.btnLeftAll = QPushButton('<<', self)
        self.btnLeftAll.setStyleSheet(centralButtonsSS)
        self.btnLeftAll.clicked.connect(self.deleteAllSelectedSignals)

        widgets = (self.btnRigth, self.btnLeft, self.btnRigthAll, self.btnLeftAll)
        for widget in widgets:
            vbox4Btn.addWidget(widget)

        vboxSelectedList = QVBoxLayout()
        self.labelSelectedSignals = QLabel('Выбранные сигналы')

        self.listSelectedSignals = QListWidget()
        self.listSelectedSignals.setSelectionMode(QAbstractItemView.MultiSelection)

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