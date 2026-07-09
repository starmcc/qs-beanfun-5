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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_TwAdv(object):
    def setupUi(self, TwAdv):
        if not TwAdv.objectName():
            TwAdv.setObjectName(u"TwAdv")
        TwAdv.resize(360, 350)
        TwAdv.setMinimumSize(QSize(360, 350))
        TwAdv.setMaximumSize(QSize(360, 356))
        TwAdv.setStyleSheet(u"QDialog#TwAdv {\n"
"    background-color: #f7f7f7;\n"
"}\n"
"QFrame#frame_main {\n"
"    background-color: rgba(255, 255, 255, 0.94);\n"
"    border: 1px solid #e6e6e6;\n"
"    border-radius: 8px;\n"
"}\n"
"QLabel#label_title {\n"
"    color: #333333;\n"
"    font-size: 14pt;\n"
"    font-weight: 600;\n"
"}\n"
"QLabel#label_desc {\n"
"    color: #7a7a7a;\n"
"    font-size: 9pt;\n"
"}\n"
"QLabel[class=\"fieldLabel\"] {\n"
"    color: #5f5f5f;\n"
"    font-size: 10pt;\n"
"    font-weight: 500;\n"
"}\n"
"QLabel#label_tips {\n"
"    color: #1967d2;\n"
"    background-color: #f5f9ff;\n"
"    border: 1px solid #dbe9ff;\n"
"    border-radius: 4px;\n"
"    padding: 6px 8px;\n"
"}\n"
"QLabel#label_verifyCode {\n"
"    background-color: #fafafa;\n"
"    border: 1px dashed #d8d8d8;\n"
"    border-radius: 6px;\n"
"    padding: 0px;\n"
"}\n"
"QLabel#label_verifyHint {\n"
"    color: #8a8a8a;\n"
"    font-size: 9pt;\n"
"}\n"
"QPushButton#pushButton_send {\n"
"    min-height: 32px;\n"
"    background-color: #f57c00;\n"
"    "
                        "color: white;\n"
"    border: 1px solid #f57c00;\n"
"    border-radius: 4px;\n"
"    padding: 4px 14px;\n"
"}\n"
"QPushButton#pushButton_send:hover {\n"
"    background-color: #ff922b;\n"
"    color: white;\n"
"}\n"
"QPushButton#pushButton_send:pressed {\n"
"    background-color: #e06f00;\n"
"}")
        self.verticalLayout = QVBoxLayout(TwAdv)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.frame_main = QFrame(TwAdv)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_main = QVBoxLayout(self.frame_main)
        self.verticalLayout_main.setSpacing(12)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(16, 14, 16, 16)
        self.verticalLayout_header = QVBoxLayout()
        self.verticalLayout_header.setSpacing(2)
        self.verticalLayout_header.setObjectName(u"verticalLayout_header")
        self.label_title = QLabel(self.frame_main)
        self.label_title.setObjectName(u"label_title")

        self.verticalLayout_header.addWidget(self.label_title)

        self.label_desc = QLabel(self.frame_main)
        self.label_desc.setObjectName(u"label_desc")

        self.verticalLayout_header.addWidget(self.label_desc)


        self.verticalLayout_main.addLayout(self.verticalLayout_header)

        self.horizontalLayout_top = QHBoxLayout()
        self.horizontalLayout_top.setSpacing(12)
        self.horizontalLayout_top.setObjectName(u"horizontalLayout_top")
        self.label_verifyCode = QLabel(self.frame_main)
        self.label_verifyCode.setObjectName(u"label_verifyCode")
        self.label_verifyCode.setMinimumSize(QSize(200, 45))
        self.label_verifyCode.setMaximumSize(QSize(200, 45))
        self.label_verifyCode.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.label_verifyCode.setStyleSheet(u"padding:0px;border:0px;")
        self.label_verifyCode.setScaledContents(True)
        self.label_verifyCode.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_top.addWidget(self.label_verifyCode)

        self.verticalLayout_verifyHint = QVBoxLayout()
        self.verticalLayout_verifyHint.setSpacing(4)
        self.verticalLayout_verifyHint.setObjectName(u"verticalLayout_verifyHint")
        self.label_verifyHint = QLabel(self.frame_main)
        self.label_verifyHint.setObjectName(u"label_verifyHint")
        self.label_verifyHint.setWordWrap(True)

        self.verticalLayout_verifyHint.addWidget(self.label_verifyHint)


        self.horizontalLayout_top.addLayout(self.verticalLayout_verifyHint)


        self.verticalLayout_main.addLayout(self.horizontalLayout_top)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.frame_main)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.lineEdit_verifyCode = QLineEdit(self.frame_main)
        self.lineEdit_verifyCode.setObjectName(u"lineEdit_verifyCode")
        self.lineEdit_verifyCode.setMinimumSize(QSize(0, 32))
        font = QFont()
        font.setPointSize(11)
        self.lineEdit_verifyCode.setFont(font)
        self.lineEdit_verifyCode.setMaxLength(18)
        self.lineEdit_verifyCode.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_verifyCode, 0, 1, 1, 1)

        self.label_5 = QLabel(self.frame_main)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing)

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_tips = QLabel(self.frame_main)
        self.label_tips.setObjectName(u"label_tips")
        self.label_tips.setMinimumSize(QSize(0, 36))
        self.label_tips.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_tips.setWordWrap(True)

        self.gridLayout.addWidget(self.label_tips, 1, 1, 1, 1)

        self.label_4 = QLabel(self.frame_main)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEdit_phone = QLineEdit(self.frame_main)
        self.lineEdit_phone.setObjectName(u"lineEdit_phone")
        self.lineEdit_phone.setMinimumSize(QSize(0, 32))
        self.lineEdit_phone.setFont(font)
        self.lineEdit_phone.setMaxLength(33)
        self.lineEdit_phone.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_phone, 2, 1, 1, 1)


        self.verticalLayout_main.addLayout(self.gridLayout)

        self.horizontalLayout_button = QHBoxLayout()
        self.horizontalLayout_button.setSpacing(0)
        self.horizontalLayout_button.setObjectName(u"horizontalLayout_button")
        self.horizontalSpacer_button = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_button.addItem(self.horizontalSpacer_button)

        self.pushButton_send = QPushButton(self.frame_main)
        self.pushButton_send.setObjectName(u"pushButton_send")
        self.pushButton_send.setMinimumSize(QSize(132, 42))

        self.horizontalLayout_button.addWidget(self.pushButton_send)


        self.verticalLayout_main.addLayout(self.horizontalLayout_button)


        self.verticalLayout.addWidget(self.frame_main)

        QWidget.setTabOrder(self.lineEdit_verifyCode, self.lineEdit_phone)
        QWidget.setTabOrder(self.lineEdit_phone, self.pushButton_send)

        self.retranslateUi(TwAdv)

        QMetaObject.connectSlotsByName(TwAdv)
    # setupUi

    def retranslateUi(self, TwAdv):
        TwAdv.setWindowTitle(QCoreApplication.translate("TwAdv", u"\u767b\u5f55\u9a8c\u8bc1", None))
        self.label_title.setText(QCoreApplication.translate("TwAdv", u"\u53f0\u670d\u8fdb\u9636\u9a8c\u8bc1", None))
        self.label_desc.setText(QCoreApplication.translate("TwAdv", u"\u8bf7\u586b\u5199\u56fe\u5f62\u9a8c\u8bc1\u7801\u4e0e\u624b\u673a\u53f7\u7801\u540e\u7ee7\u7eed\u767b\u5f55", None))
        self.label_verifyCode.setText("")
        self.label_verifyHint.setText(QCoreApplication.translate("TwAdv", u"\u70b9\u51fb\u56fe\u7247\u5237\u65b0", None))
        self.label_3.setText(QCoreApplication.translate("TwAdv", u"\u56fe\u5f62\u9a8c\u8bc1\u7801", None))
        self.label_3.setProperty(u"class", QCoreApplication.translate("TwAdv", u"fieldLabel", None))
        self.lineEdit_verifyCode.setPlaceholderText(QCoreApplication.translate("TwAdv", u"\u8bf7\u8f93\u5165\u56fe\u5f62\u9a8c\u8bc1\u7801", None))
        self.label_5.setText(QCoreApplication.translate("TwAdv", u"\u63d0\u793a\u8d44\u6599", None))
        self.label_5.setProperty(u"class", QCoreApplication.translate("TwAdv", u"fieldLabel", None))
        self.label_tips.setText(QCoreApplication.translate("TwAdv", u"XXXXXXXXXXXX", None))
        self.label_4.setText(QCoreApplication.translate("TwAdv", u"\u624b\u673a\u53f7\u7801", None))
        self.label_4.setProperty(u"class", QCoreApplication.translate("TwAdv", u"fieldLabel", None))
        self.lineEdit_phone.setPlaceholderText(QCoreApplication.translate("TwAdv", u"\u8bf7\u8f93\u5165\u624b\u673a\u53f7\u7801", None))
        self.pushButton_send.setText(QCoreApplication.translate("TwAdv", u"\u786e\u8ba4\u9001\u51fa", None))
    # retranslateUi

