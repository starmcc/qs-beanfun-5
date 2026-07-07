# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_AccountInfo.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_AccountInfo(object):
    def setupUi(self, AccountInfo):
        if not AccountInfo.objectName():
            AccountInfo.setObjectName(u"AccountInfo")
        AccountInfo.resize(244, 236)
        AccountInfo.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(AccountInfo)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_edit = QPushButton(AccountInfo)
        self.pushButton_edit.setObjectName(u"pushButton_edit")
        self.pushButton_edit.setMaximumSize(QSize(64, 16777215))

        self.gridLayout.addWidget(self.pushButton_edit, 2, 2, 1, 1)

        self.label_5 = QLabel(AccountInfo)
        self.label_5.setObjectName(u"label_5")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(48, 0))
        self.label_5.setMaximumSize(QSize(48, 16777215))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_name = QLabel(AccountInfo)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_name.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_name, 2, 1, 1, 1)

        self.label_number = QLabel(AccountInfo)
        self.label_number.setObjectName(u"label_number")
        self.label_number.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_number.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_number, 1, 1, 1, 1)

        self.label = QLabel(AccountInfo)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(48, 0))
        self.label.setMaximumSize(QSize(48, 16777215))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_account = QLabel(AccountInfo)
        self.label_account.setObjectName(u"label_account")
        self.label_account.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_account.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_account, 0, 1, 1, 1)

        self.label_status = QLabel(AccountInfo)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_status.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_status, 3, 1, 1, 1)

        self.label_7 = QLabel(AccountInfo)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(48, 0))
        self.label_7.setMaximumSize(QSize(48, 16777215))
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.label_2 = QLabel(AccountInfo)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(48, 0))
        self.label_2.setMaximumSize(QSize(48, 16777215))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)

        self.verticalLayout.addLayout(self.gridLayout)

        self.label_3 = QLabel(AccountInfo)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_3)

        self.label_day = QLabel(AccountInfo)
        self.label_day.setObjectName(u"label_day")
        sizePolicy1.setHeightForWidth(self.label_day.sizePolicy().hasHeightForWidth())
        self.label_day.setSizePolicy(sizePolicy1)
        self.label_day.setStyleSheet(u"color: blue;")
        self.label_day.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_day)

        self.label_6 = QLabel(AccountInfo)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_6)

        self.label_createTme = QLabel(AccountInfo)
        self.label_createTme.setObjectName(u"label_createTme")
        sizePolicy1.setHeightForWidth(self.label_createTme.sizePolicy().hasHeightForWidth())
        self.label_createTme.setSizePolicy(sizePolicy1)
        self.label_createTme.setStyleSheet(u"color: red;")
        self.label_createTme.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_createTme)

        self.verticalLayout.setStretch(0, 10)

        self.retranslateUi(AccountInfo)

        QMetaObject.connectSlotsByName(AccountInfo)
    # setupUi

    def retranslateUi(self, AccountInfo):
        AccountInfo.setWindowTitle(QCoreApplication.translate("AccountInfo", u"\u8d26\u53f7\u8be6\u60c5", None))
        self.pushButton_edit.setText(QCoreApplication.translate("AccountInfo", u"\u7f16\u8f91", None))
        self.label_5.setText(QCoreApplication.translate("AccountInfo", u"\u540d\u79f0", None))
        self.label.setText(QCoreApplication.translate("AccountInfo", u"\u8d26\u53f7", None))
        self.label_7.setText(QCoreApplication.translate("AccountInfo", u"\u72c0\u614b", None))
        self.label_2.setText(QCoreApplication.translate("AccountInfo", u"\u7f16\u53f7", None))
        self.label_3.setText(QCoreApplication.translate("AccountInfo", u"\u60a8\u7684\u8d26\u53f7\u5df2\u5efa\u7acb\u4e86", None))
        self.label_day.setText(QCoreApplication.translate("AccountInfo", u"0", None))
        self.label_6.setText(QCoreApplication.translate("AccountInfo", u"\u5929", None))
    # retranslateUi

