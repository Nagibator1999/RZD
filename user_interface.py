import sys
import os
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QListWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLineEdit, QLabel, QTreeView, QTreeWidgetItem, QTreeWidget, 
                            QAbstractItemView, QCheckBox)
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
        self.dictOfSignals = dict() # словарь с сигналами в которых мы потом производим поиск
        self.resultOfSearchList = list()
        self.treeSystemsVisible = True 

        self.initUI()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение', "Вы точно хотите выйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def hideTreeWidget(self, event):
        if (self.treeSystemsVisible):
            self.treeSystemsVisible = False
            self.treeSystems.hide()
            self.labelSelected.hide()

            self.searchResultList.show()
            self.searchLine.show()
            self.nuberOfSelectedLabel.show()
            self.buttonSearch.show()
            self.embeddedSignalsCheckBox.show()
            self.discreteSignalsCheckBox.show()
        else:
            self.treeSystemsVisible = True
            self.treeSystems.show()
            self.labelSelected.show()

            self.searchResultList.hide()
            self.searchLine.hide()
            self.nuberOfSelectedLabel.hide()
            self.buttonSearch.hide()
            self.embeddedSignalsCheckBox.hide()
            self.discreteSignalsCheckBox.hide()

    def searchSignals(self):
        # ищем в slef.dictOfSignals
        string = self.searchLine.text()
        self.resultOfSearchList = []
        self.searchResultList.clear()
        if (type(string) == str):
            if self.embeddedSignalsCheckBox.checkState() == 2: # 2 означает что на чекбокс тыкнули, 0 - нет
                for key in self.dictOfSignals.keys():
                    if string in key:
                        self.resultOfSearchList.append(key)
            if self.discreteSignalsCheckBox.checkState() == 2:
                for key in self.dictOfSignals.keys():
                    for record in self.dictOfSignals[key]:
                        if string in record:
                            self.resultOfSearchList.append(record)
            if (len(self.resultOfSearchList) == 0):
                self.searchResultList.addItem('Не найдено')
                self.searchResultList.setSelectionMode(QAbstractItemView.NoSelection)
            else:
                self.searchResultList.addItems(self.resultOfSearchList)
                self.searchResultList.setSelectionMode(QAbstractItemView.MultiSelection)

    def moveSelectedSignals(self):
        if self.treeSystems.isHidden(): # если поиск осуществляется через список а не дерево
            for sel in self.searchResultList.selectedIndexes():
                item = self.searchResultList.itemFromIndex(sel) # убираем выделение
                item.setSelected(False)
                data = item.data(0)
                if (data not in self.listOfChilds):
                    self.listOfChilds.append(data) 
                    self.listSelectedSignals.addItem(data)
        else: # есди поиск осуществляется через дерево
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
        if self.treeSystems.isHidden():
            for index in range(self.searchResultList.count()):
                item = self.searchResultList.item(index)
                data = item.data(0)
                if (data not in self.listOfChilds):
                    self.listOfChilds.append(data) 
                    self.listSelectedSignals.addItem(data)
        else:
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
        self.labelSystems.mousePressEvent = self.hideTreeWidget

        '-------------------------ListWidget---------------------------'
        self.treeSystems = QTreeWidget()
        self.treeSystems.setAlternatingRowColors(1)
        self.treeSystems.setHeaderHidden(1)
        self.treeSystems.setColumnCount(1)
        self.treeSystems.setSelectionMode(QAbstractItemView.MultiSelection)
        self.treeSystems.selectionModel().selectionChanged.connect(self.countGroupsAndSignals) # это для подсчёта выбранных групп и сигналов

        kks = db.MPK.select_column('Суффикс', False, False, False) #проеверь чтобы postgres был запущен
        kks = set(kks)
        for record in kks:
            row = QTreeWidgetItem(self.treeSystems, [record])
            self.treeSystems.addTopLevelItem(row)
            self.dictOfSignals[record] = list()
            suffics = set(db.MPK.select_column('KKS', 'Суффикс', record, False))
            for elem in suffics:
                self.dictOfSignals[record].append(elem)
                child = QTreeWidgetItem(row, [elem])
                row.addChild(child)   
        '----------------------------ListWidget--------------------------'

        self.labelSelected = QLabel('Выбрано: 0 групп, 0 сигналов')
        self.labelSearch = QLabel('Поиск')
        self.labelSearch.mousePressEvent = self.hideTreeWidget

        '--------------------------Hidden--------------------------------'
        self.buttonSearch = QPushButton('Искать', self)
        self.buttonSearch.clicked.connect(self.searchSignals)
        self.buttonSearch.hide()

        self.searchLine = QLineEdit(self)
        self.searchLine.hide()

        hboxSearchLayout = QHBoxLayout()
        hboxSearchLayout.addWidget(self.buttonSearch)
        hboxSearchLayout.addWidget(self.searchLine)

        self.embeddedSignalsCheckBox = QCheckBox('Упакованные сигналы', self)
        self.embeddedSignalsCheckBox.hide()
        self.discreteSignalsCheckBox = QCheckBox('Дискретные сигналы', self)
        self.discreteSignalsCheckBox.hide()

        hboxSearchParametersLayout = QHBoxLayout()
        hboxSearchParametersLayout.addWidget(self.embeddedSignalsCheckBox)
        hboxSearchParametersLayout.addWidget(self.discreteSignalsCheckBox)

        self.searchResultList = QListWidget()
        self.searchResultList.hide()
        self.searchResultList.setSelectionMode(QAbstractItemView.MultiSelection)

        self.nuberOfSelectedLabel = QLabel('0 выбрано из "сколько-то"')
        self.nuberOfSelectedLabel.hide()
        '--------------------------Hidden--------------------------------'

        self.labelDesignProtocolSignals = QLabel('Сигналы проектных протоколов')
        self.labelStoredProtocols = QLabel('Сохраненные протоколы')
        widgets = (self.labelSignalSelection, 
                   self.labelSystems, 
                   self.treeSystems, 
                   self.labelSelected, 
                   self.labelSearch, 
                   self.searchResultList, 
                   self.nuberOfSelectedLabel, 
                   self.labelDesignProtocolSignals, 
                   self.labelStoredProtocols)
        for widget in widgets:
            vboxList.addWidget(widget)
            if widget == self.labelSearch:
                vboxList.addLayout(hboxSearchLayout)
                vboxList.addLayout(hboxSearchParametersLayout)

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