# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_About.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(300, 280)
        self.vboxLayout = QVBoxLayout(About)
        self.vboxLayout.setSpacing(6)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.vboxLayout.setContentsMargins(3, 3, 3, 3)
        self.label = QLabel(About)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet(u"color: red;")
        self.label.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.label)

        self.label_2 = QLabel(About)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(u"color: red;")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.label_2)

        self.label_3 = QLabel(About)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setStyleSheet(u"color: red;")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.label_3)

        self.label_4 = QLabel(About)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setStyleSheet(u"color: rgb(255, 44, 227)")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.label_4)

        self.label_7 = QLabel(About)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(u"color: green;")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.label_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_image = QLabel(About)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setMinimumSize(QSize(120, 120))
        self.label_image.setMaximumSize(QSize(120, 120))
        self.label_image.setScaledContents(True)
        self.label_image.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_image)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.vboxLayout.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_version = QLabel(About)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setStyleSheet(u"QLabel {color:black;}QLabel:hover {color: #F57C00;}")
        self.label_version.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.label_version, 0, 1, 1, 1)

        self.label_9 = QLabel(About)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_11 = QLabel(About)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.label_qq = QLabel(About)
        self.label_qq.setObjectName(u"label_qq")
        self.label_qq.setStyleSheet(u"QLabel {color:black;}QLabel:hover {color: #F57C00;}")
        self.label_qq.setOpenExternalLinks(True)
        self.label_qq.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

        self.gridLayout.addWidget(self.label_qq, 1, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)

        self.vboxLayout.addLayout(self.gridLayout)


        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"\u5173\u4e8e..", None))
        self.label.setText(QCoreApplication.translate("About", u"\u672c\u7a0b\u5f0f\u4e0d\u662f\u6e38\u620f\u6a58\u5b50\u6570\u4f4d\u79d1\u6280\u5f00\u53d1\u7684\u5ba2\u6237\u7aef\u7a0b\u5e8f", None))
        self.label_2.setText(QCoreApplication.translate("About", u"\u4f7f\u7528\u672c\u7a0b\u5f0f\u8bf7\u786e\u4fdd\u4e0b\u8f7d\u9014\u5f84\u662f\u5426\u4e3a\u4f5c\u8005\u63d0\u4f9b\u7684\u4e0b\u8f7d\u9014\u5f84", None))
        self.label_3.setText(QCoreApplication.translate("About", u"\u4f7f\u7528\u672c\u7a0b\u5f0f\u9020\u6210\u7684\u4e00\u5207\u540e\u679c\u7531\u4f7f\u7528\u8005\u627f\u62c5", None))
        self.label_4.setText(QCoreApplication.translate("About", u"\u6240\u6709\u4e0d\u6000\u597d\u610f\u7684\u6307\u8d23...\u90fd\u9700\u8981\u65f6\u95f4\u53bb\u9a8c\u8bc1\uff01", None))
        self.label_7.setText(QCoreApplication.translate("About", u"\u5982\u679c\u60a8\u6761\u4ef6\u5141\u8bb8,\u671b\u541b\u8d5e\u8d4f", None))
        self.label_version.setText(QCoreApplication.translate("About", u"0.0.0", None))
        self.label_9.setText(QCoreApplication.translate("About", u"Version:", None))
        self.label_11.setText(QCoreApplication.translate("About", u"\u4f5c\u8005QQ:", None))
        self.label_qq.setText(QCoreApplication.translate("About", u"1140526018", None))
    # retranslateUi

