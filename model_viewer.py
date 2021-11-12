import sys
from model_window import ModelWindow
from PyQt5.QtWidgets import QApplication
from file_model import FileModel

def main(model):
    app = QApplication(sys.argv)
    gui = ModelWindow(model)
    gui.show()
    sys.exit(app.exec_())

if(__name__ == "__main__"):
    main(None)
