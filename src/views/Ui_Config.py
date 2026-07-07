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
    QGroupBox, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Config(object):
    def setupUi(self, Config):
        if not Config.objectName():
            Config.setObjectName(u"Config")
        Config.resize(280, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Config.sizePolicy().hasHeightForWidth())
        Config.setSizePolicy(sizePolicy)
        Config.setMinimumSize(QSize(280, 150))
        Config.setMaximumSize(QSize(280, 150))
        Config.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(Config)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_normal = QGroupBox(Config)
        self.groupBox_normal.setObjectName(u"groupBox_normal")
        self.gridLayout = QGridLayout(self.groupBox_normal)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 2, -1, 2)
        self.checkBox_stopUpdate = QCheckBox(self.groupBox_normal)
        self.checkBox_stopUpdate.setObjectName(u"checkBox_stopUpdate")

        self.gridLayout.addWidget(self.checkBox_stopUpdate, 0, 0, 1, 1)

        self.checkBox_closeStartWindow = QCheckBox(self.groupBox_normal)
        self.checkBox_closeStartWindow.setObjectName(u"checkBox_closeStartWindow")

        self.gridLayout.addWidget(self.checkBox_closeStartWindow, 0, 1, 1, 1)

        self.checkBox_passInput = QCheckBox(self.groupBox_normal)
        self.checkBox_passInput.setObjectName(u"checkBox_passInput")

        self.gridLayout.addWidget(self.checkBox_passInput, 2, 0, 1, 1)

        self.checkBox_appCheckUpdate = QCheckBox(self.groupBox_normal)
        self.checkBox_appCheckUpdate.setObjectName(u"checkBox_appCheckUpdate")

        self.gridLayout.addWidget(self.checkBox_appCheckUpdate, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_normal)

        self.groupBox_gamePath = QGroupBox(Config)
        self.groupBox_gamePath.setObjectName(u"groupBox_gamePath")
        self.horizontalLayout = QHBoxLayout(self.groupBox_gamePath)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, -1, 0)
        self.lineEdit_gamePath = QLineEdit(self.groupBox_gamePath)
        self.lineEdit_gamePath.setObjectName(u"lineEdit_gamePath")
        self.lineEdit_gamePath.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEdit_gamePath)

        self.pushButton_gamePath = QPushButton(self.groupBox_gamePath)
        self.pushButton_gamePath.setObjectName(u"pushButton_gamePath")
        self.pushButton_gamePath.setMinimumSize(QSize(60, 0))
        self.pushButton_gamePath.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_gamePath)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addWidget(self.groupBox_gamePath)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Config)

        QMetaObject.connectSlotsByName(Config)
    # setupUi

    def retranslateUi(self, Config):
        Config.setWindowTitle(QCoreApplication.translate("Config", u"\u8bbe\u7f6e", None))
        self.groupBox_normal.setTitle(QCoreApplication.translate("Config", u"\u5e38\u89c4", None))
        self.checkBox_stopUpdate.setText(QCoreApplication.translate("Config", u"\u963b\u6b62\u6e38\u620f\u66f4\u65b0", None))
        self.checkBox_closeStartWindow.setText(QCoreApplication.translate("Config", u"\u8df3\u8fc7Play\u7a97\u53e3", None))
        self.checkBox_passInput.setText(QCoreApplication.translate("Config", u"\u8df3\u8fc7\u767b\u5f55\u754c\u9762", None))
        self.checkBox_appCheckUpdate.setText(QCoreApplication.translate("Config", u"\u5de5\u5177\u68c0\u67e5\u66f4\u65b0", None))
        self.groupBox_gamePath.setTitle(QCoreApplication.translate("Config", u"\u6e38\u620f\u76ee\u5f55", None))
        self.pushButton_gamePath.setText(QCoreApplication.translate("Config", u"\u9009\u62e9", None))
    # retranslateUi

