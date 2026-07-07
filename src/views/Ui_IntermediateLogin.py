# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_IntermediateLogin.ui'
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

class Ui_IntermediateLogin(object):
    def setupUi(self, IntermediateLogin):
        if not IntermediateLogin.objectName():
            IntermediateLogin.setObjectName(u"IntermediateLogin")
        IntermediateLogin.resize(200, 100)
        self.verticalLayout = QVBoxLayout(IntermediateLogin)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_await = QLabel(IntermediateLogin)
        self.label_await.setObjectName(u"label_await")
        self.label_await.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_await)


        self.retranslateUi(IntermediateLogin)

        QMetaObject.connectSlotsByName(IntermediateLogin)
    # setupUi

    def retranslateUi(self, IntermediateLogin):
        IntermediateLogin.setWindowTitle(QCoreApplication.translate("IntermediateLogin", u"Await", None))
        self.label_await.setText(QCoreApplication.translate("IntermediateLogin", u"\u8bf7\u7a0d\u540e...", None))
    # retranslateUi

