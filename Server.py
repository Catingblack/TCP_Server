from PyQt5.QtNetwork import*
from PyQt5.QtCore import*



class Server(QTcpServer):

    clientReadyToRead=pyqtSignal(str)
    clientDisconnected=pyqtSignal()

    def __init__(self, parent=None):
        QTcpServer.__init__(self, parent)
        self.socket=self.makeSocket()

    def makeSocket(self):
        socket=QTcpSocket(self)
        socket.readyRead.connect(self.socketReadyToRead)
        socket.disconnected.connect(self.socketDisconnected)
        return socket

    def socketReadyToRead(self):
        data=self.socket.readAll().__str__()
        self.clientReadyToRead.emit(data)

    def socketDisconnected(self):
        self.clientDisconnected.emit()

    def incomingConnection(self, socketDescriptor):
        self.socket.setSocketDescriptor(socketDescriptor)
        print("correct")








