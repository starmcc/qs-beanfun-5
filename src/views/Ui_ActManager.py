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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHeaderView,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_ActManager(object):
    def setupUi(self, ActManager):
        if not ActManager.objectName():
            ActManager.setObjectName(u"ActManager")
        ActManager.resize(600, 300)
        self.verticalLayout = QVBoxLayout(ActManager)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.tableWidget = QTableWidget(ActManager)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)

        self.verticalLayout.addWidget(self.tableWidget)


        self.retranslateUi(ActManager)

        QMetaObject.connectSlotsByName(ActManager)
    # setupUi

    def retranslateUi(self, ActManager):
        ActManager.setWindowTitle(QCoreApplication.translate("ActManager", u"\u8d26\u53f7\u7ba1\u7406 - \u53cc\u51fb\u53ef\u9009\u62e9\u5bf9\u5e94\u8d26\u53f7\u5e94\u7528", None))
    # retranslateUi

