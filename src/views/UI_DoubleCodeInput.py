# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_DoubleCodeInput.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_DoubleCodeInput(object):
    def setupUi(self, DoubleCodeInput):
        if not DoubleCodeInput.objectName():
            DoubleCodeInput.setObjectName(u"DoubleCodeInput")
        DoubleCodeInput.resize(360, 220)
        DoubleCodeInput.setMinimumSize(QSize(360, 220))
        DoubleCodeInput.setMaximumSize(QSize(360, 220))
        DoubleCodeInput.setStyleSheet(u"QDialog#DoubleCodeInput {\n"
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
"QPushButton#pushButton_enter {\n"
"    min-width: 88px;\n"
"    background-color: #f57c00;\n"
"    color: white;\n"
"    border: 1px solid #f57c00;\n"
"}\n"
"QPushButton#pushButton_enter:hover {\n"
"    background-color: #ff922b;\n"
"    color: white;\n"
"}\n"
"QPushButton#pushButton_enter:pressed {\n"
"    background-color: #e06f00;\n"
"}")
        self.verticalLayout_root = QVBoxLayout(DoubleCodeInput)
        self.verticalLayout_root.setSpacing(12)
        self.verticalLayout_root.setObjectName(u"verticalLayout_root")
        self.verticalLayout_root.setContentsMargins(16, 16, 16, 16)
        self.frame_main = QFrame(DoubleCodeInput)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_main = QVBoxLayout(self.frame_main)
        self.verticalLayout_main.setSpacing(12)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(16, 16, 16, 16)
        self.label_title = QLabel(self.frame_main)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_main.addWidget(self.label_title)

        self.label_desc = QLabel(self.frame_main)
        self.label_desc.setObjectName(u"label_desc")
        self.label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_main.addWidget(self.label_desc)

        self.lineEdit_code = QLineEdit(self.frame_main)
        self.lineEdit_code.setObjectName(u"lineEdit_code")
        self.lineEdit_code.setMinimumSize(QSize(0, 34))
        self.lineEdit_code.setClearButtonEnabled(True)

        self.verticalLayout_main.addWidget(self.lineEdit_code)

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setSpacing(10)
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer)

        self.pushButton_out = QPushButton(self.frame_main)
        self.pushButton_out.setObjectName(u"pushButton_out")
        self.pushButton_out.setMinimumSize(QSize(88, 30))

        self.horizontalLayout_buttons.addWidget(self.pushButton_out)

        self.pushButton_enter = QPushButton(self.frame_main)
        self.pushButton_enter.setObjectName(u"pushButton_enter")
        self.pushButton_enter.setEnabled(False)
        self.pushButton_enter.setMinimumSize(QSize(90, 30))

        self.horizontalLayout_buttons.addWidget(self.pushButton_enter)


        self.verticalLayout_main.addLayout(self.horizontalLayout_buttons)


        self.verticalLayout_root.addWidget(self.frame_main)


        self.retranslateUi(DoubleCodeInput)

        QMetaObject.connectSlotsByName(DoubleCodeInput)
    # setupUi

    def retranslateUi(self, DoubleCodeInput):
        DoubleCodeInput.setWindowTitle(QCoreApplication.translate("DoubleCodeInput", u"\u53cc\u91cd\u9a8c\u8bc1", None))
        self.label_title.setText(QCoreApplication.translate("DoubleCodeInput", u"\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801", None))
        self.label_desc.setText(QCoreApplication.translate("DoubleCodeInput", u"\u8bf7\u8f93\u5165\u6388\u6743\u9a8c\u8bc1\u5668\u4e2d\u7684\u6570\u5b57\u9a8c\u8bc1\u7801", None))
        self.lineEdit_code.setPlaceholderText(QCoreApplication.translate("DoubleCodeInput", u"\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801", None))
        self.pushButton_out.setText(QCoreApplication.translate("DoubleCodeInput", u"\u53d6\u6d88", None))
        self.pushButton_enter.setText(QCoreApplication.translate("DoubleCodeInput", u"\u786e\u5b9a", None))
    # retranslateUi

