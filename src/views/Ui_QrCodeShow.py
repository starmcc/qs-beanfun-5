# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_QrCodeShow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_QrCodeShow(object):
    def setupUi(self, QrCodeShow):
        if not QrCodeShow.objectName():
            QrCodeShow.setObjectName(u"QrCodeShow")
        QrCodeShow.resize(400, 400)
        QrCodeShow.setMinimumSize(QSize(400, 400))
        QrCodeShow.setMaximumSize(QSize(400, 400))
        self.verticalLayout = QVBoxLayout(QrCodeShow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_qrCode = QLabel(QrCodeShow)
        self.label_qrCode.setObjectName(u"label_qrCode")
        self.label_qrCode.setScaledContents(True)
        self.label_qrCode.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_qrCode)


        self.retranslateUi(QrCodeShow)

        QMetaObject.connectSlotsByName(QrCodeShow)
    # setupUi

    def retranslateUi(self, QrCodeShow):
        pass
    # retranslateUi

