# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Login.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(350, 230)
        self.verticalLayout_2 = QVBoxLayout(Login)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_logoView = QLabel(Login)
        self.label_logoView.setObjectName(u"label_logoView")
        self.label_logoView.setMaximumSize(QSize(16777215, 80))
        self.label_logoView.setStyleSheet(u"padding:0px;border:0px;background:#40444F;")
        self.label_logoView.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_logoView)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(18, -1, 18, 5)
        self.widget_one = QWidget(Login)
        self.widget_one.setObjectName(u"widget_one")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_one)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_forgotPassword = QLabel(self.widget_one)
        self.label_forgotPassword.setObjectName(u"label_forgotPassword")
        self.label_forgotPassword.setStyleSheet(u"QLabel {color:black;}QLabel:hover {color: #F57C00;}")

        self.horizontalLayout_2.addWidget(self.label_forgotPassword)

        self.label_register = QLabel(self.widget_one)
        self.label_register.setObjectName(u"label_register")
        self.label_register.setStyleSheet(u"QLabel {color:black;}QLabel:hover {color: #F57C00;}")
        self.label_register.setAlignment(Qt.AlignCenter)
        self.label_register.setOpenExternalLinks(True)

        self.horizontalLayout_2.addWidget(self.label_register)

        self.horizontalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_qrCode = QLabel(self.widget_one)
        self.label_qrCode.setObjectName(u"label_qrCode")
        self.label_qrCode.setMinimumSize(QSize(32, 32))
        self.label_qrCode.setMaximumSize(QSize(32, 32))
        self.label_qrCode.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.label_qrCode.setScaledContents(True)
        self.label_qrCode.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_qrCode)

        self.radioButton_tw = QRadioButton(self.widget_one)
        self.radioButton_tw.setObjectName(u"radioButton_tw")
        self.radioButton_tw.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_2.addWidget(self.radioButton_tw)

        self.radioButton_hk = QRadioButton(self.widget_one)
        self.radioButton_hk.setObjectName(u"radioButton_hk")
        self.radioButton_hk.setFocusPolicy(Qt.NoFocus)
        self.radioButton_hk.setChecked(True)

        self.horizontalLayout_2.addWidget(self.radioButton_hk)


        self.verticalLayout.addWidget(self.widget_one)

        self.widget_two = QWidget(Login)
        self.widget_two.setObjectName(u"widget_two")
        self.gridLayout = QGridLayout(self.widget_two)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setContentsMargins(0, 0, 0, 3)
        self.label = QLabel(self.widget_two)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.checkBox_remember = QCheckBox(self.widget_two)
        self.checkBox_remember.setObjectName(u"checkBox_remember")
        self.checkBox_remember.setFocusPolicy(Qt.NoFocus)

        self.gridLayout.addWidget(self.checkBox_remember, 1, 3, 1, 1)

        self.label_5 = QLabel(self.widget_two)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.lineEdit_account = QLineEdit(self.widget_two)
        self.lineEdit_account.setObjectName(u"lineEdit_account")
        self.lineEdit_account.setMinimumSize(QSize(0, 28))

        self.gridLayout.addWidget(self.lineEdit_account, 0, 1, 1, 1)

        self.lineEdit_password = QLineEdit(self.widget_two)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setMinimumSize(QSize(0, 28))
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.lineEdit_password, 1, 1, 1, 1)

        self.pushButton_actManager = QPushButton(self.widget_two)
        self.pushButton_actManager.setObjectName(u"pushButton_actManager")
        self.pushButton_actManager.setFocusPolicy(Qt.NoFocus)

        self.gridLayout.addWidget(self.pushButton_actManager, 0, 3, 1, 1)


        self.verticalLayout.addWidget(self.widget_two)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_login = QPushButton(Login)
        self.pushButton_login.setObjectName(u"pushButton_login")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_login.sizePolicy().hasHeightForWidth())
        self.pushButton_login.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_login)

        self.pushButton_web = QPushButton(Login)
        self.pushButton_web.setObjectName(u"pushButton_web")
        sizePolicy.setHeightForWidth(self.pushButton_web.sizePolicy().hasHeightForWidth())
        self.pushButton_web.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_web)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        QWidget.setTabOrder(self.pushButton_actManager, self.checkBox_remember)
        QWidget.setTabOrder(self.checkBox_remember, self.radioButton_tw)
        QWidget.setTabOrder(self.radioButton_tw, self.radioButton_hk)

        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"QsBeanfun", None))
        self.label_logoView.setText("")
        self.label_forgotPassword.setText(QCoreApplication.translate("Login", u"\u5fd8\u8bb0\u5bc6\u7801", None))
        self.label_register.setText(QCoreApplication.translate("Login", u"\u6ce8\u518c\u8d26\u53f7", None))
        self.label_qrCode.setText("")
        self.radioButton_tw.setText(QCoreApplication.translate("Login", u"\u53f0\u6e7e", None))
        self.radioButton_hk.setText(QCoreApplication.translate("Login", u"\u9999\u6e2f", None))
        self.label.setText(QCoreApplication.translate("Login", u"\u8d26\u53f7", None))
        self.checkBox_remember.setText(QCoreApplication.translate("Login", u"\u8bf7\u8bb0\u4f4f\u6211", None))
        self.label_5.setText(QCoreApplication.translate("Login", u"\u5bc6\u7801", None))
        self.pushButton_actManager.setText(QCoreApplication.translate("Login", u"\u8d26\u53f7\u7ba1\u7406", None))
        self.pushButton_login.setText(QCoreApplication.translate("Login", u"\u767b\u5f55", None))
        self.pushButton_web.setText(QCoreApplication.translate("Login", u"\u5b98\u7f51\u767b\u5165", None))
    # retranslateUi

