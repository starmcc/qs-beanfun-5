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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Nav(object):
    def setupUi(self, Nav):
        if not Nav.objectName():
            Nav.setObjectName(u"Nav")
        Nav.resize(480, 560)
        Nav.setMinimumSize(QSize(440, 480))
        Nav.setStyleSheet(u"QDialog#Nav {\n"
"    background-color: #f7f7f7;\n"
"}\n"
"QFrame#frame_search, QScrollArea {\n"
"    background-color: rgba(255, 255, 255, 0.94);\n"
"    border: 1px solid #e6e6e6;\n"
"    border-radius: 8px;\n"
"}\n"
"QScrollArea > QWidget > QWidget {\n"
"    background-color: transparent;\n"
"}\n"
"QCheckBox {\n"
"    color: #4a4a4a;\n"
"    spacing: 6px;\n"
"}\n"
"QPushButton#pushButton_refresh {\n"
"    min-width: 72px;\n"
"    background-color: #f57c00;\n"
"    color: white;\n"
"    border: 1px solid #f57c00;\n"
"}\n"
"QPushButton#pushButton_refresh:hover {\n"
"    background-color: #ff922b;\n"
"    color: white;\n"
"}\n"
"QPushButton#pushButton_refresh:pressed {\n"
"    background-color: #e06f00;\n"
"}\n"
"QGroupBox {\n"
"    border: 1px solid #e6e6e6;\n"
"    border-radius: 8px;\n"
"    margin-top: 12px;\n"
"    padding-top: 12px;\n"
"    background-color: #ffffff;\n"
"    font-weight: 600;\n"
"    color: #444444;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 12px;\n"
" "
                        "   padding: 0 4px;\n"
"}\n"
"QLabel {\n"
"    color: #555555;\n"
"}\n"
"QScrollBar:vertical {\n"
"    width: 10px;\n"
"    background: transparent;\n"
"    margin: 4px 0 4px 0;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #d0d0d0;\n"
"    border-radius: 5px;\n"
"    min-height: 24px;\n"
"}\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #b7b7b7;\n"
"}\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: transparent;\n"
"}")
        self.verticalLayout = QVBoxLayout(Nav)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.frame_search = QFrame(Nav)
        self.frame_search.setObjectName(u"frame_search")
        self.frame_search.setFrameShape(QFrame.StyledPanel)
        self.frame_search.setFrameShadow(QFrame.Raised)
        self.verticalLayout_searchCard = QVBoxLayout(self.frame_search)
        self.verticalLayout_searchCard.setSpacing(10)
        self.verticalLayout_searchCard.setObjectName(u"verticalLayout_searchCard")
        self.verticalLayout_searchCard.setContentsMargins(14, 14, 14, 14)
        self.verticalLayout_headline = QVBoxLayout()
        self.verticalLayout_headline.setSpacing(2)
        self.verticalLayout_headline.setObjectName(u"verticalLayout_headline")
        self.label_title = QLabel(self.frame_search)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setStyleSheet(u"color: #333333; font-size: 14pt; font-weight: 600;")

        self.verticalLayout_headline.addWidget(self.label_title)

        self.label_desc = QLabel(self.frame_search)
        self.label_desc.setObjectName(u"label_desc")
        self.label_desc.setStyleSheet(u"color: #7a7a7a; font-size: 9pt;")

        self.verticalLayout_headline.addWidget(self.label_desc)


        self.verticalLayout_searchCard.addLayout(self.verticalLayout_headline)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_search = QLineEdit(self.frame_search)
        self.lineEdit_search.setObjectName(u"lineEdit_search")
        self.lineEdit_search.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.lineEdit_search)

        self.checkBox_outer = QCheckBox(self.frame_search)
        self.checkBox_outer.setObjectName(u"checkBox_outer")

        self.horizontalLayout.addWidget(self.checkBox_outer)

        self.pushButton_refresh = QPushButton(self.frame_search)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")
        self.pushButton_refresh.setMinimumSize(QSize(72, 30))

        self.horizontalLayout.addWidget(self.pushButton_refresh)


        self.verticalLayout_searchCard.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.frame_search)

        self.scrollArea = QScrollArea(Nav)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 444, 464))
        self.verticalLayout_content = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_content.setSpacing(10)
        self.verticalLayout_content.setObjectName(u"verticalLayout_content")
        self.verticalLayout_content.setContentsMargins(10, 10, 10, 10)
        self.container = QWidget(self.scrollAreaWidgetContents)
        self.container.setObjectName(u"container")
        self.verticalLayout_groups = QVBoxLayout(self.container)
        self.verticalLayout_groups.setSpacing(10)
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
        self.label_title.setText(QCoreApplication.translate("Nav", u"\u6e38\u620f\u5e38\u7528\u5bfc\u822a", None))
        self.label_desc.setText(QCoreApplication.translate("Nav", u"\u652f\u6301\u641c\u7d22\u7b5b\u9009\uff0c\u70b9\u51fb\u6309\u94ae\u53ef\u5feb\u901f\u6253\u5f00\u7ad9\u70b9\u6216\u4e8c\u7ef4\u7801", None))
        self.lineEdit_search.setPlaceholderText(QCoreApplication.translate("Nav", u"\u8f93\u5165\u5173\u952e\u5b57\u641c\u7d22\u529f\u80fd\u5165\u53e3...", None))
        self.checkBox_outer.setText(QCoreApplication.translate("Nav", u"\u9ed8\u8ba4\u6d4f\u89c8\u5668", None))
        self.pushButton_refresh.setText(QCoreApplication.translate("Nav", u"\u5237\u65b0", None))
    # retranslateUi

