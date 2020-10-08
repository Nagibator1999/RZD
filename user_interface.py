import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QListWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLineEdit, QLabel)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 QListWidget"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.initUI()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def initUI(self):
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.list = QListWidget()
        self.list.insertItem(0, "Java")
        self.list.insertItem(1, "Python")

        self.list2 = QListWidget()

        # центральный блок с кнопками
        self.btnRigth = QPushButton('>', self)
        self.btnLeft = QPushButton('<', self)
        self.btnRigthAll = QPushButton('>>', self)
        self.btnLeftAll = QPushButton('<<', self)

        # Ок и отмена внизу справа
        self.btnOK = QPushButton('OK', self)
        self.btnCancel = QPushButton('Отмена', self)

        # Описание и строка для ввода
        self.descriptionText = QLabel('Описание')
        self.line = QLineEdit(self)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btnOK)
        hbox.addWidget(self.btnCancel)

        vbox = QVBoxLayout()
        vbox.addWidget(self.btnRigth)
        vbox.addWidget(self.btnLeft)
        vbox.addWidget(self.btnRigthAll)
        vbox.addWidget(self.btnLeftAll)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.descriptionText)
        hbox2.addWidget(self.line)

        grid = QGridLayout()
        mainGrid = QGridLayout()

        grid.addWidget(self.list, 1,1)
        grid.addLayout(vbox, 1,2)
        grid.addWidget(self.list2, 1,3)
        mainGrid.addLayout(grid, 1,1)
        mainGrid.addLayout(hbox2, 2,1)
        mainGrid.addLayout(hbox, 3,1)

        self.setLayout(mainGrid)

        # vbox= QVBoxLayout()
        # self.list = QListWidget()
        # self.list.insertItem(0, "Java")
        # self.list.insertItem(1, "Python")
        # vbox.addWidget(self.list)
        
        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # self.okButton = QPushButton("OK", self)
        # self.cancelButton = QPushButton("Cancel", self)
        # hbox.addWidget(self.okButton)
        # hbox.addWidget(self.cancelButton)
        # vbox.addLayout(hbox)

        # self.setLayout(vbox)

        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())