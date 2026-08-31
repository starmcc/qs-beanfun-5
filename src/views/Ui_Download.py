# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Download.ui'
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
    QProgressBar, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Download(object):
    def setupUi(self, Download):
        if not Download.objectName():
            Download.setObjectName(u"Download")
        Download.resize(420, 300)
        Download.setMinimumSize(QSize(420, 300))
        Download.setMaximumSize(QSize(420, 300))
        Download.setStyleSheet(u"QDialog#Download {\n"
"    background: #F5F7FB;\n"
"    color: #2B2F38;\n"
"    font-family: \"Microsoft YaHei\", \"Segoe UI\", Arial, sans-serif;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"QLabel#titleLabel {\n"
"    color: #2C333A;\n"
"    font-size: 16px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#percentLabel {\n"
"    color: #4287F5;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"QLabel#speedLabel {\n"
"    color: #8A94A6;\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"QLabel#statusLabel {\n"
"    color: #8A94A6;\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"QProgressBar#progressBar {\n"
"    background-color: #EEF1F5;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    min-height: 10px;\n"
"    max-height: 10px;\n"
"}\n"
"\n"
"QProgressBar#progressBar::chunk {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #4287F5, stop:1 #6AA9FF);\n"
"    border-radius: 5px;\n"
"}")
        self.verticalLayout = QVBoxLayout(Download)
        self.verticalLayout.setSpacing(14)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(30, 24, 30, 24)
        self.titleLabel = QLabel(Download)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.titleLabel)

        self.animLayout = QHBoxLayout()
        self.animLayout.setObjectName(u"animLayout")
        self.animLeftSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.animLayout.addItem(self.animLeftSpacer)

        self.animFrame = QWidget(Download)
        self.animFrame.setObjectName(u"animFrame")
        self.animFrame.setMinimumSize(QSize(72, 72))
        self.animFrame.setMaximumSize(QSize(72, 72))

        self.animLayout.addWidget(self.animFrame)

        self.animRightSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.animLayout.addItem(self.animRightSpacer)


        self.verticalLayout.addLayout(self.animLayout)

        self.progressBar = QProgressBar(Download)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 10))
        self.progressBar.setMaximumSize(QSize(16777215, 10))
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.verticalLayout.addWidget(self.progressBar)

        self.infoLayout = QHBoxLayout()
        self.infoLayout.setObjectName(u"infoLayout")
        self.percentLabel = QLabel(Download)
        self.percentLabel.setObjectName(u"percentLabel")

        self.infoLayout.addWidget(self.percentLabel)

        self.infoSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.infoLayout.addItem(self.infoSpacer)

        self.speedLabel = QLabel(Download)
        self.speedLabel.setObjectName(u"speedLabel")

        self.infoLayout.addWidget(self.speedLabel)


        self.verticalLayout.addLayout(self.infoLayout)

        self.statusLabel = QLabel(Download)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.statusLabel)


        self.retranslateUi(Download)

        QMetaObject.connectSlotsByName(Download)
    # setupUi

    def retranslateUi(self, Download):
        Download.setWindowTitle(QCoreApplication.translate("Download", u"\u4e0b\u8f7d", None))
        self.titleLabel.setText(QCoreApplication.translate("Download", u"\u6b63\u5728\u4e0b\u8f7d...", None))
        self.percentLabel.setText(QCoreApplication.translate("Download", u"0%", None))
        self.speedLabel.setText("")
        self.statusLabel.setText(QCoreApplication.translate("Download", u"\u6b63\u5728\u8fde\u63a5\u670d\u52a1\u5668...", None))
    # retranslateUi

