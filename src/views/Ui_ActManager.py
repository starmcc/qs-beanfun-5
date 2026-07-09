# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_ActManager.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QHeaderView, QLabel, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_ActManager(object):
    def setupUi(self, ActManager):
        if not ActManager.objectName():
            ActManager.setObjectName(u"ActManager")
        ActManager.resize(760, 420)
        ActManager.setMinimumSize(QSize(760, 420))
        ActManager.setStyleSheet(u"QDialog#ActManager {\n"
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
"QLabel#label_subtitle {\n"
"    color: #7a7a7a;\n"
"    font-size: 9pt;\n"
"}\n"
"QTableWidget {\n"
"    background-color: white;\n"
"    alternate-background-color: #fafafa;\n"
"    border: 1px solid #e3e3e3;\n"
"    border-radius: 6px;\n"
"    gridline-color: #efefef;\n"
"    selection-background-color: #e6f2ff;\n"
"    selection-color: #0052cc;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #f5f7fa;\n"
"    color: #555555;\n"
"    border: none;\n"
"    border-bottom: 1px solid #e3e3e3;\n"
"    padding: 8px;\n"
"    font-weight: 600;\n"
"}\n"
"QTableWidget::item {\n"
"    padding: 6px;\n"
"}\n"
"QTableWidget::item:selected {\n"
"    background-color: #e6f2ff;\n"
"    color: #0052cc;\n"
""
                        "}")
        self.verticalLayout = QVBoxLayout(ActManager)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.frame_main = QFrame(ActManager)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout_mainCard = QVBoxLayout(self.frame_main)
        self.verticalLayout_mainCard.setSpacing(12)
        self.verticalLayout_mainCard.setObjectName(u"verticalLayout_mainCard")
        self.verticalLayout_mainCard.setContentsMargins(16, 14, 16, 16)
        self.verticalLayout_header = QVBoxLayout()
        self.verticalLayout_header.setSpacing(2)
        self.verticalLayout_header.setObjectName(u"verticalLayout_header")
        self.label_title = QLabel(self.frame_main)
        self.label_title.setObjectName(u"label_title")

        self.verticalLayout_header.addWidget(self.label_title)

        self.label_subtitle = QLabel(self.frame_main)
        self.label_subtitle.setObjectName(u"label_subtitle")

        self.verticalLayout_header.addWidget(self.label_subtitle)


        self.verticalLayout_mainCard.addLayout(self.verticalLayout_header)

        self.tableWidget = QTableWidget(self.frame_main)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_mainCard.addWidget(self.tableWidget)


        self.verticalLayout.addWidget(self.frame_main)


        self.retranslateUi(ActManager)

        QMetaObject.connectSlotsByName(ActManager)
    # setupUi

    def retranslateUi(self, ActManager):
        ActManager.setWindowTitle(QCoreApplication.translate("ActManager", u"\u8d26\u53f7\u7ba1\u7406 - \u53cc\u51fb\u53ef\u9009\u62e9\u5bf9\u5e94\u8d26\u53f7\u5e94\u7528", None))
        self.label_title.setText(QCoreApplication.translate("ActManager", u"\u672c\u5730\u8d26\u53f7\u7ba1\u7406", None))
        self.label_subtitle.setText(QCoreApplication.translate("ActManager", u"\u53cc\u51fb\u884c\u53ef\u5feb\u901f\u5e94\u7528\u8d26\u53f7\uff0c\u53f3\u952e\u53ef\u65b0\u589e\u3001\u7f16\u8f91\u3001\u5220\u9664\u6216\u5237\u65b0", None))
    # retranslateUi

