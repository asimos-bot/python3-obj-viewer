from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QGroupBox
from PyQt5.QtCore import QPoint, Qt
from model_canvas import ModelCanvas
from file_model import FileModel

from base_model import BaseModel

class ModelWindow(QWidget):

    def __init__(self, model : BaseModel):
        super(ModelWindow, self).__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Model Viewer")

        self.canvas = ModelCanvas()

        self.canvas.set_model(model)

        # interactive widgets
        self.interactive_widgets = QGroupBox()
        self.label = QLabel("filename:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.input = QLineEdit()
        self.input.setText("teapot.obj")
        self.render_button = QPushButton("Render")

        self.group_box = QVBoxLayout()
        self.group_box.addWidget
        self.group_box.addWidget(self.label)
        self.group_box.addWidget(self.input)
        self.group_box.addWidget(self.render_button)
        self.interactive_widgets.setLayout(self.group_box)
        self.interactive_widgets.setFixedSize(self.group_box.sizeHint())

        # main layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.interactive_widgets)

        self.setLayout(self.vbox)
        self.drag_reference : QPoint = QPoint(0, 0)

        self.render_button.clicked.connect(self.load_model)

    def load_model(self):
        
        try:
            model = FileModel(self.input.text())
            self.canvas.set_model(model)
            self.input.setStyleSheet("border: 1px solid gray")
        except FileNotFoundError:
            self.input.setStyleSheet("border: 1px solid red")
