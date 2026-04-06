from haircardapp import ImageDropWidget
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui

app = QApplication(sys.argv)
app.setStyle('Fusion')
window = ImageDropWidget()
window.setWindowIcon(QtGui.QIcon('C:/Users/Haitam/Downloads/pu02.png'))
window.show()
sys.exit(app.exec_())