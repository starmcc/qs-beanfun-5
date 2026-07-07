# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_AccountEdit.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_AccountEdit(object):
    def setupUi(self, AccountEdit):
        if not AccountEdit.objectName():
            AccountEdit.setObjectName(u"AccountEdit")
        AccountEdit.resize(242, 124)
        self.verticalLayout = QVBoxLayout(AccountEdit)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 5, 3, 5)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.label_3 = QLabel(AccountEdit)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.lineEdit_password = QLineEdit(AccountEdit)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.lineEdit_password, 1, 4, 1, 1)

        self.label_2 = QLabel(AccountEdit)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label = QLabel(AccountEdit)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.lineEdit_desc = QLineEdit(AccountEdit)
        self.lineEdit_desc.setObjectName(u"lineEdit_desc")

        self.gridLayout.addWidget(self.lineEdit_desc, 2, 4, 1, 1)

        self.lineEdit_account = QLineEdit(AccountEdit)
        self.lineEdit_account.setObjectName(u"lineEdit_account")

        self.gridLayout.addWidget(self.lineEdit_account, 0, 4, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_btn = QHBoxLayout()
        self.horizontalLayout_btn.setObjectName(u"horizontalLayout_btn")
        self.horizontalLayout_btn.setContentsMargins(3, 3, 3, 3)
        self.radioButton_hk = QRadioButton(AccountEdit)
        self.radioButton_hk.setObjectName(u"radioButton_hk")

        self.horizontalLayout_btn.addWidget(self.radioButton_hk)

        self.radioButton_tw = QRadioButton(AccountEdit)
        self.radioButton_tw.setObjectName(u"radioButton_tw")

        self.horizontalLayout_btn.addWidget(self.radioButton_tw)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_btn.addItem(self.horizontalSpacer)

        self.pushButton_save = QPushButton(AccountEdit)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout_btn.addWidget(self.pushButton_save)


        self.verticalLayout.addLayout(self.horizontalLayout_btn)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        QWidget.setTabOrder(self.lineEdit_account, self.lineEdit_password)
        QWidget.setTabOrder(self.lineEdit_password, self.lineEdit_desc)
        QWidget.setTabOrder(self.lineEdit_desc, self.radioButton_hk)
        QWidget.setTabOrder(self.radioButton_hk, self.radioButton_tw)
        QWidget.setTabOrder(self.radioButton_tw, self.pushButton_save)

        self.retranslateUi(AccountEdit)

        QMetaObject.connectSlotsByName(AccountEdit)
    # setupUi

    def retranslateUi(self, AccountEdit):
        AccountEdit.setWindowTitle(QCoreApplication.translate("AccountEdit", u"\u8d26\u53f7", None))
        self.label_3.setText(QCoreApplication.translate("AccountEdit", u"\u5bc6\u7801", None))
        self.label_2.setText(QCoreApplication.translate("AccountEdit", u"\u8d26\u53f7", None))
        self.label.setText(QCoreApplication.translate("AccountEdit", u"\u5907\u6ce8", None))
        self.radioButton_hk.setText(QCoreApplication.translate("AccountEdit", u"\u9999\u6e2f", None))
        self.radioButton_tw.setText(QCoreApplication.translate("AccountEdit", u"\u53f0\u6e7e", None))
        self.pushButton_save.setText(QCoreApplication.translate("AccountEdit", u"\u4fdd\u5b58", None))
    # retranslateUi

