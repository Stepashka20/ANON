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

        self.loginBtn.clicked.connect(self.on_click)
        

        self.setWindowIcon(QIcon("./res/icons8-anonymous-mask-96.png"))

        self.registerLabel.mousePressEvent = self.openRegister
        self.loginLabel.mousePressEvent = self.openLogin
        self.loginObjects = [self.loginAuthorization,self.passwordAuthorization,self.rememberMe,self.registerLabel,self.loginBtn]
        self.registerObjects = [self.loginLabel,self.registerBtn,self.passwordRegister,self.loginRegister,self.screenNameRegister]

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
            self.usersList.addItem(item)
            item.setData(-1, i)

        # self.usersList.addItems(entries)
        self.usersList.installEventFilter(self)

        self.personInfo.setText('''<h3 style="padding:0;margin:0">Коллега Влад</h3><div>был в сети недавно</div>''')
        self.MessagesList.setHtml(open('test.html', 'r', encoding='utf-8').read())
        self.findPersonBtn.clicked.connect(self.addUser)
        self.settingsBtn.clicked.connect(self.openSettings)
        self.sendMessageBtn.clicked.connect(self.send)
        self.inputMessage.returnPressed.connect(self.send)

    def send(self):
        self.Login.server.sendMessage(self.inputMessage.text())

    def updateHtml(self,html):
        self.MessagesList.setHtml(html)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.usersList and source.itemAt(event.pos()):
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
        msg = QMessageBox()
        msg.setWindowTitle("Добавление пользователя")
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
