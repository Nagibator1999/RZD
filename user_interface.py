import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QListWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLineEdit, QLabel, QTreeView, QTreeWidgetItem)
from PyQt5.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QCoreApplication, QDir

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Конфигурация показа'
        self.top = 200
        self.left = 500
        self.width = 800
        self.height = 600
        self.initUI()

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def getValueFromTree(self, value):
        print(value.data())
        print(value.row())
        print(value.column())

    def initUI(self):
        # styles
        stylesheet = '''.QPushButton {background-color: #ccc;}
                        .QLabel {font-size: 14px;}'''
        centralButtonsSS = 'max-width: 20%; padding: 6px; margin: 10px; border-radius: 5px; border: 1px solid black'
        self.setStyleSheet(stylesheet)

        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        vboxList = QVBoxLayout()
        self.labelSignalSelection = QLabel('Выбор сигнала')
        self.labelSystems = QLabel('Системы')
        #
        # self.listSystems = QListWidget()
        # self.listSystems.insertItem(0, "Java")
        # self.listSystems.insertItem(1, "Python")
        #
        self.treeSystems = QTreeView()
        self.treeSystems.setHeaderHidden(True)

        self.treeModel = QStandardItemModel()
        self.rootNode = self.treeModel.invisibleRootItem()

        python = QStandardItem('Python')
        python2 = QStandardItem('Pyhton 3.0')
        python.appendRow(python2)
        java = QStandardItem('Java')
        java2 = QStandardItem('Java 13.13')
        java.appendRow(java2)
        python.setEditable(False)
        python2.setEditable(False)
        java.setEditable(False)
        java2.setEditable(False)

        self.rootNode.appendRow(python)
        self.rootNode.appendRow(java)

        self.treeSystems.setModel(self.treeModel)
        self.treeSystems.expandAll() # разворачивает все разворачиваемые елементы
        self.treeSystems.doubleClicked.connect(self.getValueFromTree)
        # self.first_item = QTreeWidgetItem(self.treeSystems, ['Python'])
        # self.second_item = QTreeWidgetItem(self.first_item, ['Python 3.0'])
        
        
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