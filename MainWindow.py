from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5.QtNetwork import*
from PyQt5.QtWidgets import*
from PyQt5 import uic
from Server import*

def transfer(str):
    try:
        str='-> Cпортсмен, нагрудный номер {} прошёл отсечку {} в {}ч. {}м. {}с.'.format(str[2:6], str[7:9], int(str[10:12]), int(str[13:15]),
        round(float(str[16:22]),1))

    finally: return str


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mainwindow.ui", self)
        self.server=self.makeServer()
        self.makeConnections()


    def writeToLog(self, data):
        self.f=open('log.txt', 'a')
        self.f.write(transfer(data)+'\n')

    def makeServer(self):
        server=Server(self)
        server.clientReadyToRead.connect(self.displayData)
        server.clientReadyToRead.connect(self.writeToLog)
        server.clientDisconnected.connect(self.clientDisconnected)
        return server

    def makeConnections(self):
        self.pushButton.clicked.connect(self.buttonIsPressed)


    def clientDisconnected(self):
        self.f.close()
        QMessageBox.information(self, "OK", "Клиент отключен")


    def displayData(self, data):
        if data[23:25] == '00':
            self.textBrowser.append(transfer(data))

    def buttonIsPressed(self):
        port=self.textEdit.toPlainText()
        if port =='':
            QMessageBox.critical(self, "Ошибка. Введите номер порта!!", "Ошибка")
            return
        port=int(port)
        if self.server.listen(QHostAddress.Any, port):
            QMessageBox.information(self, "OK", "Сервер запущен")
            self.textBrowser.append("Ожидание соединения...")
        else:
            QMessageBox.critical(self, "Ошибка", server.errorString())

