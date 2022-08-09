import sys
from yeristasyonu1 import Ui_MainWindow 
from PyQt5 import QtWidgets , QtCore , QtGui
import serial.tools.list_ports

class myApp(QtWidgets.QMainWindow): #interface
    
    def __init__(self):

        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #combobox içerikleri
        self.ports = serial.tools.list_ports.comports()
        for i in self.ports:
            self.ui.comboBox.addItem(str(i))
        

        baud = ["300", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "74880", "115200", "230400", "250000",
                "500000", "1000000", "2000000"]
        for i in baud:
            self.ui.comboBox_2.addItem(i)
        self.ui.comboBox_2.setCurrentText(baud[4])

        self.ui.label_3.setText("<font color=red>COM port bağlı değil!!!</font>")
        self.ui.textEdit.setReadOnly(True)

        #seri port bağlantısı

        self.mySerial = serialThreadClass()
        self.mySerial.message.connect(self.messageTextEdit)      #def    
        self.mySerial.start()

        #button
        self.ui.pushButton.clicked.connect(self.serialConnect)             #def
        self.ui.pushButton_2.clicked.connect(self.serialDisconnect)        #def



    #defs

    #bağantı
    def serialConnect(self):  

        self.porttext = self.ui.comboBox.currentText()
        self.port = self.porttext.split()
        self.boudrate = self.ui.comboBox_2.currentText()
        self.mySerial.serialPort.boudrate = int(self.boudrate)
        self.mySerial.serialPort.port = self.port[0]
        
        try:
            self.mySerial.serialPort.open()
        except:
            self.ui.textEdit.append("bağlantı hatası")
        
        if(self.mySerial.serialPort.isOpen()):
            self.ui.label_3.setText("<font color=green>Port bağlandı </font>")
            self.ui.pushButton.setEnabled(False)
            self.ui.comboBox.setEnabled(False)
            self.ui.comboBox_2.setEnabled(False)


    #disconnect
    def serialDisconnect(self):
        if self.mySerial.serialPort.isOpen():
            self.mySerial.serialPort.close()
            if self.mySerial.serialPort.isOpen() == False:
                self.ui.label_3.setText("<font color=red>Bağlantı Kesildi</font>")
                self.ui.pushButton.setEnabled(True)
                self.ui.comboBox.setEnabled(True)
                self.ui.comboBox_2.setEnabled(True)
        else:
            self.ui.textEdit.append("Serial port zaten kapalı")



    #mesajı yazma
    def messageTextEdit (self):
        self.incomingMessage = str(self.mySerial.data.decode())
        self.ui.textEdit.append(self.incomingMessage)
    
        
class serialThreadClass(QtCore.QThread):  # Seri Porttan veri okumak için
    message = QtCore.pyqtSignal(str)

    def __init__(self,parent = None):
        super(serialThreadClass, self).__init__(parent)
        self.serialPort = serial.Serial()
        self.stopflag = False
    
    def stop(self):
        self.stopflag = True
    
    def run(self):
        while True:
            if (self.stopflag):
                self.stopflag = False
                break
            elif(self.serialPort.isOpen()):
                try:
                    self.data = self.serialPort.readline()
                except:
                    print("Hata\n")
                self.message.emit(str(self.data.decode()))

    
def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec())


app()
