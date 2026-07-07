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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_DoubleCodeInput(object):
    def setupUi(self, DoubleCodeInput):
        if not DoubleCodeInput.objectName():
            DoubleCodeInput.setObjectName(u"DoubleCodeInput")
        DoubleCodeInput.resize(300, 130)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DoubleCodeInput.sizePolicy().hasHeightForWidth())
        DoubleCodeInput.setSizePolicy(sizePolicy)
        DoubleCodeInput.setMinimumSize(QSize(300, 130))
        DoubleCodeInput.setMaximumSize(QSize(300, 130))
        DoubleCodeInput.setStyleSheet(u"\n"
"    QDialog {\n"
"     background-color: transparent;\n"
"    }\n"
"    #label_title {\n"
"     font-size: 18px;\n"
"     font-weight: 600;\n"
"     color: #333333;\n"
"    }\n"
"    .QLineEdit {\n"
"     font-size: 24px;\n"
"     font-weight: 600;\n"
"     border: 2px solid #e0e0e0;\n"
"     border-radius: 8px;\n"
"     color: #333333;\n"
"     background-color: #f9f9f9;\n"
"     max-length: 1;\n"
"    }\n"
"    .QLineEdit:focus {\n"
"     border-color: #409eff;\n"
"     background-color: #ffffff;\n"
"     outline: none;\n"
"    }")
        self.verticalLayout_2 = QVBoxLayout(DoubleCodeInput)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(DoubleCodeInput)
        self.label_title.setObjectName(u"label_title")
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        self.label_title.setMinimumSize(QSize(280, 38))
        self.label_title.setMaximumSize(QSize(280, 38))
        self.label_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_title)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_1 = QLineEdit(DoubleCodeInput)
        self.lineEdit_1.setObjectName(u"lineEdit_1")
        self.lineEdit_1.setMinimumSize(QSize(38, 38))
        self.lineEdit_1.setMaximumSize(QSize(38, 38))
        self.lineEdit_1.setMaxLength(1)
        self.lineEdit_1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit_1)

        self.lineEdit_2 = QLineEdit(DoubleCodeInput)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(38, 38))
        self.lineEdit_2.setMaximumSize(QSize(38, 38))
        self.lineEdit_2.setMaxLength(1)
        self.lineEdit_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(DoubleCodeInput)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(38, 38))
        self.lineEdit_3.setMaximumSize(QSize(38, 38))
        self.lineEdit_3.setMaxLength(1)
        self.lineEdit_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit_3)

        self.lineEdit_4 = QLineEdit(DoubleCodeInput)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMinimumSize(QSize(38, 38))
        self.lineEdit_4.setMaximumSize(QSize(38, 38))
        self.lineEdit_4.setMaxLength(1)
        self.lineEdit_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit_4)

        self.lineEdit_5 = QLineEdit(DoubleCodeInput)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(38, 38))
        self.lineEdit_5.setMaximumSize(QSize(38, 38))
        self.lineEdit_5.setMaxLength(1)
        self.lineEdit_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit_5)

        self.lineEdit_6 = QLineEdit(DoubleCodeInput)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMinimumSize(QSize(38, 38))
        self.lineEdit_6.setMaximumSize(QSize(38, 38))
        self.lineEdit_6.setMaxLength(1)
        self.lineEdit_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit_6)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_out = QPushButton(DoubleCodeInput)
        self.pushButton_out.setObjectName(u"pushButton_out")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_out.sizePolicy().hasHeightForWidth())
        self.pushButton_out.setSizePolicy(sizePolicy1)
        self.pushButton_out.setMinimumSize(QSize(0, 38))
        self.pushButton_out.setMaximumSize(QSize(16777215, 38))

        self.horizontalLayout_2.addWidget(self.pushButton_out)

        self.pushButton_enter = QPushButton(DoubleCodeInput)
        self.pushButton_enter.setObjectName(u"pushButton_enter")
        self.pushButton_enter.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.pushButton_enter.sizePolicy().hasHeightForWidth())
        self.pushButton_enter.setSizePolicy(sizePolicy1)
        self.pushButton_enter.setMinimumSize(QSize(0, 38))
        self.pushButton_enter.setMaximumSize(QSize(16777215, 38))

        self.horizontalLayout_2.addWidget(self.pushButton_enter)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.retranslateUi(DoubleCodeInput)

        QMetaObject.connectSlotsByName(DoubleCodeInput)
    # setupUi

    def retranslateUi(self, DoubleCodeInput):
        DoubleCodeInput.setWindowTitle(QCoreApplication.translate("DoubleCodeInput", u"\u53cc\u91cd\u9a8c\u8bc1", None))
        self.label_title.setText(QCoreApplication.translate("DoubleCodeInput", u"\u8bf7\u8f93\u51656\u4f4d\u9a8c\u8bc1\u6570\u5b57", None))
        self.pushButton_out.setText(QCoreApplication.translate("DoubleCodeInput", u"\u53d6\u6d88", None))
        self.pushButton_enter.setText(QCoreApplication.translate("DoubleCodeInput", u"\u786e\u8ba4", None))
    # retranslateUi

