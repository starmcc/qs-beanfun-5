from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie, QMoveEvent
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget


class LoadMask(QMainWindow):

    def __init__(self, parent=None):
        super(LoadMask, self).__init__(parent)
        parent.installEventFilter(self)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.label_image = QLabel()

        self.movie = QMovie(":/images/loading")
        self.label_image.setMovie(self.movie)
        self.label_image.setFixedSize(QSize(160, 160))
        self.label_image.setScaledContents(True)
        self.movie.start()
        self.layout.addWidget(self.label_image)

        widget = QWidget()
        widget.setLayout(self.layout)

        self.setCentralWidget(widget)
        self.setWindowOpacity(0.96)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        if parent:
            self.setFixedSize(QSize(parent.geometry().width(), parent.geometry().height()))

        self.show()

    def eventFilter(self, widget, event):
        if widget == self.parent() and type(event) == QMoveEvent:
            self.moveWithParent()
            return True
        return super(LoadMask, self).eventFilter(widget, event)

    def moveWithParent(self):
        if self.isVisible():
            self.move(self.parent().geometry().x(), self.parent().geometry().y())
            self.setFixedSize(QSize(self.parent().geometry().width(), self.parent().geometry().height()))
