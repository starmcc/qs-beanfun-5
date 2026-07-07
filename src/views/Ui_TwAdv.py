# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_TwAdv.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_TwAdv(object):
    def setupUi(self, TwAdv):
        if not TwAdv.objectName():
            TwAdv.setObjectName(u"TwAdv")
        TwAdv.resize(210, 200)
        TwAdv.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(TwAdv)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 3, 5, 3)
        self.label_verifyCode = QLabel(TwAdv)
        self.label_verifyCode.setObjectName(u"label_verifyCode")
        self.label_verifyCode.setMinimumSize(QSize(200, 45))
        self.label_verifyCode.setMaximumSize(QSize(200, 45))
        self.label_verifyCode.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.label_verifyCode.setStyleSheet(u"padding:0px;border:0px;")
        self.label_verifyCode.setScaledContents(True)
        self.label_verifyCode.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_verifyCode)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(TwAdv)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.lineEdit_phone = QLineEdit(TwAdv)
        self.lineEdit_phone.setObjectName(u"lineEdit_phone")
        self.lineEdit_phone.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setPointSize(11)
        self.lineEdit_phone.setFont(font)
        self.lineEdit_phone.setMaxLength(33)
        self.lineEdit_phone.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_phone, 2, 1, 1, 1)

        self.label_5 = QLabel(TwAdv)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.lineEdit_verifyCode = QLineEdit(TwAdv)
        self.lineEdit_verifyCode.setObjectName(u"lineEdit_verifyCode")
        self.lineEdit_verifyCode.setMaximumSize(QSize(16777215, 32))
        self.lineEdit_verifyCode.setFont(font)
        self.lineEdit_verifyCode.setMaxLength(18)
        self.lineEdit_verifyCode.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_verifyCode, 0, 1, 1, 1)

        self.label_4 = QLabel(TwAdv)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_tips = QLabel(TwAdv)
        self.label_tips.setObjectName(u"label_tips")
        self.label_tips.setMaximumSize(QSize(16777215, 17))
        self.label_tips.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_tips, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.pushButton_send = QPushButton(TwAdv)
        self.pushButton_send.setObjectName(u"pushButton_send")
        self.pushButton_send.setMinimumSize(QSize(0, 42))

        self.verticalLayout.addWidget(self.pushButton_send)

        QWidget.setTabOrder(self.lineEdit_verifyCode, self.lineEdit_phone)
        QWidget.setTabOrder(self.lineEdit_phone, self.pushButton_send)

        self.retranslateUi(TwAdv)

        QMetaObject.connectSlotsByName(TwAdv)
    # setupUi

    def retranslateUi(self, TwAdv):
        TwAdv.setWindowTitle(QCoreApplication.translate("TwAdv", u"\u767b\u5f55\u9a8c\u8bc1", None))
        self.label_verifyCode.setText("")
        self.label_3.setText(QCoreApplication.translate("TwAdv", u"\u56fe\u5f62\u9a8c\u8bc1\u7801", None))
        self.label_5.setText(QCoreApplication.translate("TwAdv", u"\u63d0\u793a\u8d44\u6599", None))
        self.label_4.setText(QCoreApplication.translate("TwAdv", u"\u624b\u673a\u53f7\u7801", None))
        self.label_tips.setText(QCoreApplication.translate("TwAdv", u"XXXXXXXXXXXX", None))
        self.pushButton_send.setText(QCoreApplication.translate("TwAdv", u"\u786e\u8ba4\u9001\u51fa", None))
    # retranslateUi

