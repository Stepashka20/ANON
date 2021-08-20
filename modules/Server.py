import websocket,time

from PyQt5.QtCore import QThread
from PyQt5 import Qt

class Server:
    def __init__(self,mainUI):
        self.mainUI = mainUI

    def connect(self):
        self.socketThread = readSocket(self.mainUI,self)
        self.socketThread.threadSignalMain.connect(self.on_threadSignal)
        self.socketThread.start()
    
    def on_threadSignal(self,signal):
        print("Принят сигнал",signal)
        self.mainUI.Messenger.updateHtml(signal)
        
    def sendMessage(self,message):
        self.socketThread.sendMessage(message)

class readSocket(QThread):
    threadSignalMain = Qt.pyqtSignal(str)

    def __init__(self,mainUI,Server):
        QThread.__init__(self)
        self.mainUI = mainUI
        self.Server = Server

    def __del__(self):
        try:
            self.stop()
            self.wait()
        except:
            pass

    def run(self):
        print("start ws")
        time.sleep(0.1)
        self.ws = websocket.WebSocketApp(
            "ws://127.0.0.1:5000/",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()
    
    def sendMessage(self,message):
        print("Sending...")
        self.ws.send(message)
        
    def on_message(self,ws,message):
        print("SIGNAL",message)
        self.threadSignalMain.emit(message)

    def on_open(self,ws):
        print("open")
        ws.send("Ping")

    def on_error(self,ws,error):
        print("error")

    def on_close(self,ws, close_status_code, close_msg):
        print("close")
    
        
        
        
