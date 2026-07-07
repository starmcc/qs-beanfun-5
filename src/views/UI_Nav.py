# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_Nav.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Nav(object):
    def setupUi(self, Nav):
        if not Nav.objectName():
            Nav.setObjectName(u"Nav")
        Nav.resize(400, 400)
        Nav.setMinimumSize(QSize(400, 400))
        Nav.setMaximumSize(QSize(400, 400))
        self.verticalLayout = QVBoxLayout(Nav)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.header = QWidget(Nav)
        self.header.setObjectName(u"header")
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_search = QLineEdit(self.header)
        self.lineEdit_search.setObjectName(u"lineEdit_search")

        self.horizontalLayout.addWidget(self.lineEdit_search)

        self.checkBox_outer = QCheckBox(self.header)
        self.checkBox_outer.setObjectName(u"checkBox_outer")

        self.horizontalLayout.addWidget(self.checkBox_outer)

        self.pushButton_refresh = QPushButton(self.header)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")

        self.horizontalLayout.addWidget(self.pushButton_refresh)


        self.verticalLayout.addWidget(self.header)

        self.scrollArea = QScrollArea(Nav)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 392, 369))
        self.verticalLayout_content = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_content.setSpacing(8)
        self.verticalLayout_content.setObjectName(u"verticalLayout_content")
        self.verticalLayout_content.setContentsMargins(4, 4, 4, 4)
        self.container = QWidget(self.scrollAreaWidgetContents)
        self.container.setObjectName(u"container")
        self.verticalLayout_groups = QVBoxLayout(self.container)
        self.verticalLayout_groups.setSpacing(8)
        self.verticalLayout_groups.setObjectName(u"verticalLayout_groups")
        self.verticalLayout_groups.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_content.addWidget(self.container)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_content.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Nav)

        QMetaObject.connectSlotsByName(Nav)
    # setupUi

    def retranslateUi(self, Nav):
        Nav.setWindowTitle(QCoreApplication.translate("Nav", u"\u4fbf\u6377\u5bfc\u822a", None))
        self.lineEdit_search.setPlaceholderText(QCoreApplication.translate("Nav", u"\u641c\u7d22...", None))
        self.checkBox_outer.setText(QCoreApplication.translate("Nav", u"\u9ed8\u8ba4\u6d4f\u89c8\u5668", None))
        self.pushButton_refresh.setText(QCoreApplication.translate("Nav", u"\u5237\u65b0", None))
    # retranslateUi

