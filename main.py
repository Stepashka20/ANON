# -*- coding: utf8 -*-
import sys  
sys.path.append("./design")
sys.path.append("./modules")
from PyQt5 import QtWidgets
from PyQt5.QtCore import QPropertyAnimation,QEvent
import qdarkstyle,time
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox,QGraphicsOpacityEffect,QMenu
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from Server import Server
import Ui_messenger
import Ui_login
import Ui_settings

class LoginForm(QtWidgets.QMainWindow, Ui_login.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.Messenger = Messenger(self)

        self.server = Server(self)
        self.server.connect()

        self.pushButton.clicked.connect(self.on_click)
        

        self.setWindowIcon(QIcon("./res/icons8-anonymous-mask-96.png"))

        self.label.mousePressEvent = self.openRegister
        self.label_2.mousePressEvent = self.openLogin
        self.loginObjects = [self.lineEdit,self.lineEdit_2,self.checkBox,self.label,self.pushButton]
        self.registerObjects = [self.label_2,self.pushButton_2,self.lineEdit_3,self.lineEdit_4,self.lineEdit_5]
        self.openLogin()

    def setOpacity(self,element,opacity):
        op=QGraphicsOpacityEffect(self)
        op.setOpacity(opacity)
        element.setGraphicsEffect(op)

    def animationOpacity(self,element,start,end,duration):
        effect = QtWidgets.QGraphicsOpacityEffect(self)
        element.setGraphicsEffect(effect) 

        element.animation = QPropertyAnimation(effect, b'opacity')
        element.animation.setDuration(duration)       
        element.animation.setStartValue(start)
        element.animation.setEndValue(end)
        
        element.animation.start()

    def doShow(self):
        self.animation = QPropertyAnimation(self.pushButton, b'geometry')
        try:
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # Диапазон прозрачности постепенно увеличивается от 0 до 1.
        self.animation.setStartValue(self.pushButton.geometry())
        self.animation.setEndValue(self.pushButton.geometry().translated(200, 0))
        self.animation.start()

    def on_click(self):
        self.Messenger.show()
        
    def openRegister(self, event):
        for el in self.loginObjects:
            self.setOpacity(el,0)
            el.hide()

        for el in self.registerObjects:
            el.show()
            self.animationOpacity(el,0,1,200)

    def openLogin(self, event=None):
        for el in self.registerObjects:
            self.setOpacity(el,0)
            el.hide()

        for el in self.loginObjects:
            el.show()
            self.animationOpacity(el,0,1,200)

class Settings(QtWidgets.QMainWindow,Ui_settings.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./res/icons8-anonymous-mask-96.png"))


class Messenger(QtWidgets.QMainWindow, Ui_messenger.Ui_MainWindow):
    def __init__(self,Login):
        super().__init__()
        self.setupUi(self)
        self.Login = Login
        self.setWindowIcon(QIcon("./res/icons8-anonymous-mask-96.png"))

        entries = [{'name':"igor",'id':"id1"},{'name':"Igor",'id':"id2"}]

        for i in entries:
            item = QtWidgets.QListWidgetItem(i['name'])
            self.listWidget.addItem(item)
            item.setData(-1, i)

        # self.listWidget.addItems(entries)
        self.listWidget.installEventFilter(self)

        self.label.setText('''<h3 style="padding:0;margin:0">Коллега Влад</h3><div>был в сети недавно</div>''')
        self.textEdit.setHtml(open('test.html', 'r', encoding='utf-8').read())
        self.pushButton_2.clicked.connect(self.addUser)
        self.pushButton_4.clicked.connect(self.openSettings)
        self.pushButton.clicked.connect(self.send)
        self.lineEdit.returnPressed.connect(self.send)

    def send(self):
        self.Login.server.sendMessage(self.lineEdit.text())

    def updateHtml(self,html):
        self.textEdit.setHtml(html)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.listWidget and source.itemAt(event.pos()):
            menu = QMenu()
            blockUser = menu.addAction('Заблокировать')
            clearChat = menu.addAction('Очистить чат')
            delteChat = menu.addAction('Удалить чат')
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action == blockUser:
                print(1, source.itemAt(event.pos()).data(-1))
            if action == clearChat:
                print(2, source.itemAt(event.pos()).data(-1))
            if action == delteChat:
                print(3, source.itemAt(event.pos()).data(-1))

            return True
        return super().eventFilter(source, event)

    def addUser(self):
        self.textEdit.setHtml(open('test.html', 'r', encoding='utf-8').read())
        msg = QMessageBox()
        msg.setWindowTitle("Добавление пользователя")
        self.Login.server.sendMessage('Hello')
        ok = 1

        if ok: 
            msg.setText("Пользователь Коллега Влад добавлен")
            msg.setIcon(QMessageBox.Information)   
        else:
            msg.setText("Пользователь kollVL не найден")
            msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def openSettings(self):
        self.Settings = Settings()
        self.Settings.show()


def main():
    app = QtWidgets.QApplication(sys.argv) 
    window = LoginForm() 
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':
    main() 
