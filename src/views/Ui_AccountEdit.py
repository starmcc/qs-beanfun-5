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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_AccountEdit(object):
    def setupUi(self, AccountEdit):
        if not AccountEdit.objectName():
            AccountEdit.setObjectName(u"AccountEdit")
        AccountEdit.resize(372, 210)
        AccountEdit.setMinimumSize(QSize(372, 210))
        self.verticalLayout = QVBoxLayout(AccountEdit)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.frame_form = QFrame(AccountEdit)
        self.frame_form.setObjectName(u"frame_form")
        self.frame_form.setFrameShape(QFrame.StyledPanel)
        self.frame_form.setFrameShadow(QFrame.Raised)
        self.frame_form.setStyleSheet(u"QFrame#frame_form {\n"
"    background-color: rgba(255, 255, 255, 0.92);\n"
"    border: 1px solid #e6e6e6;\n"
"    border-radius: 8px;\n"
"}\n"
"QLabel#label_title {\n"
"    color: #333333;\n"
"    font-size: 14pt;\n"
"    font-weight: 600;\n"
"}\n"
"QLabel#label_subtitle {\n"
"    color: #7a7a7a;\n"
"    font-size: 9pt;\n"
"}\n"
"QLabel[class=\"fieldLabel\"] {\n"
"    color: #555555;\n"
"    font-size: 10pt;\n"
"    font-weight: 500;\n"
"}\n"
"QRadioButton {\n"
"    spacing: 6px;\n"
"    color: #444444;\n"
"}\n"
"QRadioButton::indicator {\n"
"    width: 14px;\n"
"    height: 14px;\n"
"}\n"
"QPushButton#pushButton_save {\n"
"    min-width: 92px;\n"
"    min-height: 28px;\n"
"    background-color: #f57c00;\n"
"    color: white;\n"
"    border: 1px solid #f57c00;\n"
"    border-radius: 4px;\n"
"    padding: 4px 14px;\n"
"}\n"
"QPushButton#pushButton_save:hover {\n"
"    background-color: #ff922b;\n"
"    color: white;\n"
"}\n"
"QPushButton#pushButton_save:pressed {\n"
"    background-color: #e06f00;\n"
"}")
        self.verticalLayout_card = QVBoxLayout(self.frame_form)
        self.verticalLayout_card.setSpacing(12)
        self.verticalLayout_card.setObjectName(u"verticalLayout_card")
        self.verticalLayout_card.setContentsMargins(16, 14, 16, 14)
        self.verticalLayout_header = QVBoxLayout()
        self.verticalLayout_header.setSpacing(2)
        self.verticalLayout_header.setObjectName(u"verticalLayout_header")
        self.verticalLayout_header.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_form)
        self.label_title.setObjectName(u"label_title")

        self.verticalLayout_header.addWidget(self.label_title)

        self.label_subtitle = QLabel(self.frame_form)
        self.label_subtitle.setObjectName(u"label_subtitle")

        self.verticalLayout_header.addWidget(self.label_subtitle)


        self.verticalLayout_card.addLayout(self.verticalLayout_header)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(10)
        self.label_2 = QLabel(self.frame_form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEdit_account = QLineEdit(self.frame_form)
        self.lineEdit_account.setObjectName(u"lineEdit_account")
        self.lineEdit_account.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.lineEdit_account, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frame_form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.lineEdit_password = QLineEdit(self.frame_form)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setMinimumSize(QSize(0, 30))
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.lineEdit_password, 1, 1, 1, 1)

        self.label = QLabel(self.frame_form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.lineEdit_desc = QLineEdit(self.frame_form)
        self.lineEdit_desc.setObjectName(u"lineEdit_desc")
        self.lineEdit_desc.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.lineEdit_desc, 2, 1, 1, 1)


        self.verticalLayout_card.addLayout(self.gridLayout)

        self.horizontalLayout_btn = QHBoxLayout()
        self.horizontalLayout_btn.setSpacing(12)
        self.horizontalLayout_btn.setObjectName(u"horizontalLayout_btn")
        self.horizontalLayout_btn.setContentsMargins(0, 0, 0, 0)
        self.radioButton_hk = QRadioButton(self.frame_form)
        self.radioButton_hk.setObjectName(u"radioButton_hk")

        self.horizontalLayout_btn.addWidget(self.radioButton_hk)

        self.radioButton_tw = QRadioButton(self.frame_form)
        self.radioButton_tw.setObjectName(u"radioButton_tw")

        self.horizontalLayout_btn.addWidget(self.radioButton_tw)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_btn.addItem(self.horizontalSpacer)

        self.pushButton_save = QPushButton(self.frame_form)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout_btn.addWidget(self.pushButton_save)


        self.verticalLayout_card.addLayout(self.horizontalLayout_btn)


        self.verticalLayout.addWidget(self.frame_form)

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
        self.label_title.setText(QCoreApplication.translate("AccountEdit", u"\u7f16\u8f91\u8d26\u53f7", None))
        self.label_subtitle.setText(QCoreApplication.translate("AccountEdit", u"\u8bf7\u586b\u5199\u8d26\u53f7\u4fe1\u606f\u5e76\u9009\u62e9\u767b\u5f55\u5730\u533a", None))
        self.label_2.setText(QCoreApplication.translate("AccountEdit", u"\u8d26\u53f7", None))
        self.label_2.setProperty(u"class", QCoreApplication.translate("AccountEdit", u"fieldLabel", None))
        self.lineEdit_account.setPlaceholderText(QCoreApplication.translate("AccountEdit", u"\u8bf7\u8f93\u5165\u8d26\u53f7", None))
        self.label_3.setText(QCoreApplication.translate("AccountEdit", u"\u5bc6\u7801", None))
        self.label_3.setProperty(u"class", QCoreApplication.translate("AccountEdit", u"fieldLabel", None))
        self.lineEdit_password.setPlaceholderText(QCoreApplication.translate("AccountEdit", u"\u8bf7\u8f93\u5165\u5bc6\u7801", None))
        self.label.setText(QCoreApplication.translate("AccountEdit", u"\u5907\u6ce8", None))
        self.label.setProperty(u"class", QCoreApplication.translate("AccountEdit", u"fieldLabel", None))
        self.lineEdit_desc.setPlaceholderText(QCoreApplication.translate("AccountEdit", u"\u53ef\u9009\uff0c\u7528\u4e8e\u533a\u5206\u8d26\u53f7", None))
        self.radioButton_hk.setText(QCoreApplication.translate("AccountEdit", u"\u9999\u6e2f", None))
        self.radioButton_tw.setText(QCoreApplication.translate("AccountEdit", u"\u53f0\u6e7e", None))
        self.pushButton_save.setText(QCoreApplication.translate("AccountEdit", u"\u4fdd\u5b58", None))
    # retranslateUi

