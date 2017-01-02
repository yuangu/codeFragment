# -*- coding: utf-8 -*-


from PyQt4 import QtGui,QtCore,QtNetwork
import sys
import locale

def isset(v):
   try :
     type (eval(v))
   except :
     return  0
   else :
     return  1


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        title = QtGui.QLabel(u'IP地址:')
        review = QtGui.QLabel(u'日志:')

        button = QtGui.QPushButton(u"连接")
        self.connect(button, QtCore.SIGNAL( 'clicked()' ), self.onButtonClick)

        titleEdit = QtGui.QLineEdit()
        self.mHostEdit = titleEdit

        reviewEdit = QtGui.QTextBrowser()

        self.mTextBrowser = reviewEdit    

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)
        grid.addWidget(button, 1, 2)

        grid.addWidget(review, 2, 0)
        grid.addWidget(reviewEdit, 2, 1, 5, 2)

        self.setLayout(grid)

        self.resize(800, 600)
        self.center()
        self.setWindowTitle(u'选程调试工具')
        self.show()


    def center(self):  #主窗口居中显示函数
        screen=QtGui.QDesktopWidget().screenGeometry()
        size=self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def onButtonClick(self):
        ip = self.mHostEdit.text()
        serverIP = QtNetwork.QHostAddress()

        if not serverIP.setAddress(ip):
            QtGui.QMessageBox.information( self, u"提示",u"请正确填写设备IP地址" )
            return

        if hasattr(self, 'mTcpSocket') :
            if self.mTcpSocket.isValid():
                self.mTcpSocket.disconnectFromHost()
        else:
            self.mTcpSocket = QtNetwork.QTcpSocket(self)
            self.connect(self.mTcpSocket,QtCore.SIGNAL("connected()"),self.connected)
            self.connect(self.mTcpSocket,QtCore.SIGNAL("disconnected()"),self.disconnected)
            self.connect(self.mTcpSocket,QtCore.SIGNAL("readyRead()"),self.dataReceived)

        self.mTcpSocket.connectToHost(serverIP.toString(), 1818)

    def connected(self):
        self.mTextBrowser.append(u"连接成功")

    def disconnected(self):
        self.mTextBrowser.append(u"连接断开")

    def dataReceived(self):
        while self.mTcpSocket.bytesAvailable() > 0:
            length = self.mTcpSocket.bytesAvailable()
            msg = QtCore.QString(self.mTcpSocket.read(length))
            msg = msg.fromUtf8(msg)
            self.mTextBrowser.append(msg.fromUtf8(msg))

def main():
    app = QtGui.QApplication(sys.argv)

    mycode = locale.getpreferredencoding()
    #mycode = 'utf8'
    reload(sys)
    sys.setdefaultencoding(mycode)

    code = QtCore.QTextCodec.codecForName(mycode)
    QtCore.QTextCodec.setCodecForLocale(code)
    QtCore.QTextCodec.setCodecForTr(code)
    QtCore.QTextCodec.setCodecForCStrings(code)


    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
