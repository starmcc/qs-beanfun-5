# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_QrCodeLogin.ui'
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

class Ui_QrCodeLogin(object):
    def setupUi(self, QrCodeLogin):
        if not QrCodeLogin.objectName():
            QrCodeLogin.setObjectName(u"QrCodeLogin")
        QrCodeLogin.resize(300, 300)
        QrCodeLogin.setMinimumSize(QSize(300, 300))
        QrCodeLogin.setMaximumSize(QSize(300, 300))
        self.verticalLayout = QVBoxLayout(QrCodeLogin)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_qrCode = QLabel(QrCodeLogin)
        self.label_qrCode.setObjectName(u"label_qrCode")
        self.label_qrCode.setScaledContents(True)
        self.label_qrCode.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_qrCode)


        self.retranslateUi(QrCodeLogin)

        QMetaObject.connectSlotsByName(QrCodeLogin)
    # setupUi

    def retranslateUi(self, QrCodeLogin):
        QrCodeLogin.setWindowTitle(QCoreApplication.translate("QrCodeLogin", u"\u4e8c\u7ef4\u7801\u767b\u5165", None))
    # retranslateUi

