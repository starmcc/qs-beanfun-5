# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Config.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Config(object):
    def setupUi(self, Config):
        if not Config.objectName():
            Config.setObjectName(u"Config")
        Config.resize(350, 260)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Config.sizePolicy().hasHeightForWidth())
        Config.setSizePolicy(sizePolicy)
        Config.setMinimumSize(QSize(350, 260))
        Config.setMaximumSize(QSize(350, 260))
        Config.setStyleSheet(u"QDialog#Config {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"                                stop:0 #f7faff,\n"
"                                stop:1 #eef4ff);\n"
"}\n"
"QGroupBox {\n"
"    font: 9pt \"Microsoft YaHei UI\";\n"
"    font-weight: 600;\n"
"    color: #2d3a4b;\n"
"    border: 1px solid #d9e4f2;\n"
"    border-radius: 12px;\n"
"    margin-top: 12px;\n"
"    background-color: rgba(255, 255, 255, 0.92);\n"
"    padding-top: 8px;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 12px;\n"
"    padding: 6px 6px;\n"
"    color: #4c6fff;\n"
"    background-color: transparent;\n"
"}")
        self.verticalLayout = QVBoxLayout(Config)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        self.groupBox_normal = QGroupBox(Config)
        self.groupBox_normal.setObjectName(u"groupBox_normal")
        self.gridLayout = QGridLayout(self.groupBox_normal)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(14)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(12, 14, 12, 10)
        self.checkBox_stopUpdate = QCheckBox(self.groupBox_normal)
        self.checkBox_stopUpdate.setObjectName(u"checkBox_stopUpdate")

        self.gridLayout.addWidget(self.checkBox_stopUpdate, 0, 0, 1, 1)

        self.checkBox_closeStartWindow = QCheckBox(self.groupBox_normal)
        self.checkBox_closeStartWindow.setObjectName(u"checkBox_closeStartWindow")

        self.gridLayout.addWidget(self.checkBox_closeStartWindow, 0, 1, 1, 1)

        self.checkBox_passInput = QCheckBox(self.groupBox_normal)
        self.checkBox_passInput.setObjectName(u"checkBox_passInput")

        self.gridLayout.addWidget(self.checkBox_passInput, 1, 0, 1, 1)

        self.checkBox_appCheckUpdate = QCheckBox(self.groupBox_normal)
        self.checkBox_appCheckUpdate.setObjectName(u"checkBox_appCheckUpdate")

        self.gridLayout.addWidget(self.checkBox_appCheckUpdate, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_normal)

        self.groupBox_gamePath = QGroupBox(Config)
        self.groupBox_gamePath.setObjectName(u"groupBox_gamePath")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_gamePath)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(12, 14, 12, 12)
        self.label_gamePathHint = QLabel(self.groupBox_gamePath)
        self.label_gamePathHint.setObjectName(u"label_gamePathHint")
        self.label_gamePathHint.setStyleSheet(u"color: #5f6f86; font: 8.5pt \"Microsoft YaHei UI\";")
        self.label_gamePathHint.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_gamePathHint)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_gamePath = QLineEdit(self.groupBox_gamePath)
        self.lineEdit_gamePath.setObjectName(u"lineEdit_gamePath")
        self.lineEdit_gamePath.setMinimumSize(QSize(0, 32))
        self.lineEdit_gamePath.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_gamePath)

        self.pushButton_gamePath = QPushButton(self.groupBox_gamePath)
        self.pushButton_gamePath.setObjectName(u"pushButton_gamePath")
        self.pushButton_gamePath.setMinimumSize(QSize(84, 32))
        self.pushButton_gamePath.setMaximumSize(QSize(108, 16777215))
        self.pushButton_gamePath.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.pushButton_gamePath)

        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 2)

        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox_gamePath)

        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 2)

        self.retranslateUi(Config)

        QMetaObject.connectSlotsByName(Config)
    # setupUi

    def retranslateUi(self, Config):
        Config.setWindowTitle(QCoreApplication.translate("Config", u"\u8bbe\u7f6e", None))
        self.groupBox_normal.setTitle(QCoreApplication.translate("Config", u"\u5e38\u89c4\u8bbe\u7f6e", None))
        self.checkBox_stopUpdate.setText(QCoreApplication.translate("Config", u"\u963b\u6b62\u6e38\u620f\u66f4\u65b0", None))
        self.checkBox_closeStartWindow.setText(QCoreApplication.translate("Config", u"\u8df3\u8fc7 Play \u7a97\u53e3", None))
        self.checkBox_passInput.setText(QCoreApplication.translate("Config", u"\u8df3\u8fc7\u767b\u5f55\u754c\u9762", None))
        self.checkBox_appCheckUpdate.setText(QCoreApplication.translate("Config", u"\u5de5\u5177\u81ea\u52a8\u68c0\u67e5\u66f4\u65b0", None))
        self.groupBox_gamePath.setTitle(QCoreApplication.translate("Config", u"\u6e38\u620f\u76ee\u5f55", None))
        self.label_gamePathHint.setText(QCoreApplication.translate("Config", u"\u8bf7\u9009\u62e9\u65b0\u67ab\u4e4b\u8c37\u6e38\u620f\u5b89\u88c5\u76ee\u5f55", None))
        self.lineEdit_gamePath.setPlaceholderText(QCoreApplication.translate("Config", u"\u5c1a\u672a\u9009\u62e9\u6e38\u620f\u76ee\u5f55", None))
        self.pushButton_gamePath.setText(QCoreApplication.translate("Config", u"\u6d4f\u89c8\u76ee\u5f55", None))
    # retranslateUi

