import pyside, sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
w = pyside.CWidget()
w.show()
sys.exit(app.exec_())
