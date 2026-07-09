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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_AccountInfo(object):
    def setupUi(self, AccountInfo):
        if not AccountInfo.objectName():
            AccountInfo.setObjectName(u"AccountInfo")
        AccountInfo.resize(360, 286)
        AccountInfo.setMinimumSize(QSize(360, 286))
        AccountInfo.setStyleSheet(u"QDialog#AccountInfo {\n"
"    background-color: #f7f7f7;\n"
"}\n"
"QFrame#frame_infoCard, QFrame#frame_statCard {\n"
"    background-color: rgba(255, 255, 255, 0.94);\n"
"    border: 1px solid #e6e6e6;\n"
"    border-radius: 8px;\n"
"}\n"
"QLabel#label_headerTitle {\n"
"    color: #333333;\n"
"    font-size: 14pt;\n"
"    font-weight: 600;\n"
"}\n"
"QLabel#label_headerDesc {\n"
"    color: #7a7a7a;\n"
"    font-size: 9pt;\n"
"}\n"
"QLabel[class=\"infoKey\"] {\n"
"    color: #6a6a6a;\n"
"    font-size: 10pt;\n"
"    font-weight: 500;\n"
"}\n"
"QLabel[class=\"infoValue\"] {\n"
"    color: #2f2f2f;\n"
"    font-size: 10pt;\n"
"    padding: 2px 0;\n"
"}\n"
"QLabel#label_day {\n"
"    color: #1967d2;\n"
"    font-size: 24pt;\n"
"    font-weight: 700;\n"
"}\n"
"QLabel#label_3, QLabel#label_6 {\n"
"    color: #6a6a6a;\n"
"    font-size: 10pt;\n"
"}\n"
"QLabel#label_createTme {\n"
"    color: #f57c00;\n"
"    font-size: 10pt;\n"
"    font-weight: 500;\n"
"}\n"
"QPushButton#pushButton_edit {\n"
"    min-width: 84px;\n"
""
                        "    min-height: 28px;\n"
"    background-color: #f57c00;\n"
"    color: white;\n"
"    border: 1px solid #f57c00;\n"
"    border-radius: 4px;\n"
"    padding: 4px 14px;\n"
"}\n"
"QPushButton#pushButton_edit:hover {\n"
"    background-color: #ff922b;\n"
"    color: white;\n"
"}\n"
"QPushButton#pushButton_edit:pressed {\n"
"    background-color: #e06f00;\n"
"}")
        self.verticalLayout = QVBoxLayout(AccountInfo)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.frame_infoCard = QFrame(AccountInfo)
        self.frame_infoCard.setObjectName(u"frame_infoCard")
        self.frame_infoCard.setFrameShape(QFrame.StyledPanel)
        self.frame_infoCard.setFrameShadow(QFrame.Raised)
        self.verticalLayout_infoCard = QVBoxLayout(self.frame_infoCard)
        self.verticalLayout_infoCard.setSpacing(12)
        self.verticalLayout_infoCard.setObjectName(u"verticalLayout_infoCard")
        self.verticalLayout_infoCard.setContentsMargins(16, 14, 16, 14)
        self.horizontalLayout_header = QHBoxLayout()
        self.horizontalLayout_header.setSpacing(8)
        self.horizontalLayout_header.setObjectName(u"horizontalLayout_header")
        self.verticalLayout_header = QVBoxLayout()
        self.verticalLayout_header.setSpacing(2)
        self.verticalLayout_header.setObjectName(u"verticalLayout_header")
        self.label_headerTitle = QLabel(self.frame_infoCard)
        self.label_headerTitle.setObjectName(u"label_headerTitle")

        self.verticalLayout_header.addWidget(self.label_headerTitle)

        self.label_headerDesc = QLabel(self.frame_infoCard)
        self.label_headerDesc.setObjectName(u"label_headerDesc")

        self.verticalLayout_header.addWidget(self.label_headerDesc)


        self.horizontalLayout_header.addLayout(self.verticalLayout_header)

        self.horizontalSpacer_header = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_header.addItem(self.horizontalSpacer_header)

        self.pushButton_edit = QPushButton(self.frame_infoCard)
        self.pushButton_edit.setObjectName(u"pushButton_edit")
        self.pushButton_edit.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_header.addWidget(self.pushButton_edit)


        self.verticalLayout_infoCard.addLayout(self.horizontalLayout_header)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(10)
        self.label = QLabel(self.frame_infoCard)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(54, 0))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_account = QLabel(self.frame_infoCard)
        self.label_account.setObjectName(u"label_account")
        self.label_account.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_account.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_account, 0, 1, 1, 1)

        self.label_2 = QLabel(self.frame_infoCard)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(54, 0))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_number = QLabel(self.frame_infoCard)
        self.label_number.setObjectName(u"label_number")
        self.label_number.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_number.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_number, 1, 1, 1, 1)

        self.label_5 = QLabel(self.frame_infoCard)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(54, 0))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_name = QLabel(self.frame_infoCard)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_name.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_name, 2, 1, 1, 1)

        self.label_7 = QLabel(self.frame_infoCard)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(54, 0))
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.label_status = QLabel(self.frame_infoCard)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.label_status.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_status, 3, 1, 1, 1)


        self.verticalLayout_infoCard.addLayout(self.gridLayout)


        self.verticalLayout.addWidget(self.frame_infoCard)

        self.frame_statCard = QFrame(AccountInfo)
        self.frame_statCard.setObjectName(u"frame_statCard")
        self.frame_statCard.setFrameShape(QFrame.StyledPanel)
        self.frame_statCard.setFrameShadow(QFrame.Raised)
        self.verticalLayout_statCard = QVBoxLayout(self.frame_statCard)
        self.verticalLayout_statCard.setSpacing(4)
        self.verticalLayout_statCard.setObjectName(u"verticalLayout_statCard")
        self.verticalLayout_statCard.setContentsMargins(16, 16, 16, 16)
        self.label_3 = QLabel(self.frame_statCard)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_statCard.addWidget(self.label_3)

        self.label_day = QLabel(self.frame_statCard)
        self.label_day.setObjectName(u"label_day")
        self.label_day.setAlignment(Qt.AlignCenter)

        self.verticalLayout_statCard.addWidget(self.label_day)

        self.label_6 = QLabel(self.frame_statCard)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_statCard.addWidget(self.label_6)

        self.label_createTme = QLabel(self.frame_statCard)
        self.label_createTme.setObjectName(u"label_createTme")
        self.label_createTme.setAlignment(Qt.AlignCenter)

        self.verticalLayout_statCard.addWidget(self.label_createTme)


        self.verticalLayout.addWidget(self.frame_statCard)


        self.retranslateUi(AccountInfo)

        QMetaObject.connectSlotsByName(AccountInfo)
    # setupUi

    def retranslateUi(self, AccountInfo):
        AccountInfo.setWindowTitle(QCoreApplication.translate("AccountInfo", u"\u8d26\u53f7\u8be6\u60c5", None))
        self.label_headerTitle.setText(QCoreApplication.translate("AccountInfo", u"\u6e38\u620f\u8d26\u53f7\u4fe1\u606f", None))
        self.label_headerDesc.setText(QCoreApplication.translate("AccountInfo", u"\u4ee5\u4e0b\u5185\u5bb9\u53ef\u590d\u5236\u67e5\u770b\uff0c\u540d\u79f0\u53ef\u76f4\u63a5\u7f16\u8f91", None))
        self.pushButton_edit.setText(QCoreApplication.translate("AccountInfo", u"\u7f16\u8f91\u540d\u79f0", None))
        self.label.setText(QCoreApplication.translate("AccountInfo", u"\u8d26\u53f7", None))
        self.label.setProperty(u"class", QCoreApplication.translate("AccountInfo", u"infoKey", None))
        self.label_account.setText("")
        self.label_account.setProperty(u"class", QCoreApplication.translate("AccountInfo", u"infoValue", None))
        self.label_2.setText(QCoreApplication.translate("AccountInfo", u"\u7f16\u53f7", None))
        self.label_2.setProperty(u"class", QCoreApplication.translate("AccountInfo", u"infoKey", None))
        self.label_number.setText("")
        self.label_number.setProperty(u"class", QCoreApplication.translate("AccountInfo", u"infoValue", None))
        self.label_5.setText(QCoreApplication.translate("AccountInfo", u"\u540d\u79f0", None))
        self.label_5.setProperty(u"class", QCoreApplication.translate("AccountInfo", u"infoKey", None))
        self.label_name.setText("")
        self.label_name.setProperty(u"class", QCoreApplication.translate("AccountInfo", u"infoValue", None))
        self.label_7.setText(QCoreApplication.translate("AccountInfo", u"\u72b6\u6001", None))
        self.label_7.setProperty(u"class", QCoreApplication.translate("AccountInfo", u"infoKey", None))
        self.label_status.setText("")
        self.label_status.setProperty(u"class", QCoreApplication.translate("AccountInfo", u"infoValue", None))
        self.label_3.setText(QCoreApplication.translate("AccountInfo", u"\u60a8\u7684\u8d26\u53f7\u5df2\u5efa\u7acb\u4e86", None))
        self.label_day.setText(QCoreApplication.translate("AccountInfo", u"0", None))
        self.label_6.setText(QCoreApplication.translate("AccountInfo", u"\u5929", None))
        self.label_createTme.setText("")
    # retranslateUi

