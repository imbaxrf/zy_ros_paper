import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from HMI.Ui_HMI import *
#import Ui_untitled 

class HMI(QMainWindow, Ui_MainWindow): 
    def __init__(self, parent=None): 
        super(HMI, self).__init__(parent) 
        self.setupUi(self) 
    def slot1(self):
        self.textEdit.setText("xxx")

if __name__ == '__main__': 
    app = QApplication(sys.argv) 
    myWin = HMI() 
    myWin.show() 
    sys.exit(app.exec_()) 

