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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(420, 520)
        About.setMinimumSize(QSize(420, 520))
        About.setStyleSheet(u"QDialog#About {\n"
"    background: #F5F7FB;\n"
"    color: #2B2F38;\n"
"    font-family: \"Microsoft YaHei\", \"Segoe UI\", Arial, sans-serif;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"QFrame#cardFrame {\n"
"    background: #FFFFFF;\n"
"    border: 1px solid #E6EAF2;\n"
"    border-radius: 18px;\n"
"}\n"
"\n"
"QFrame#headerFrame {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
"        stop:0 #FF8A65,\n"
"        stop:0.55 #FFB74D,\n"
"        stop:1 #FFD54F);\n"
"    border-radius: 16px;\n"
"}\n"
"\n"
"QLabel#titleLabel {\n"
"    color: #FFFFFF;\n"
"    font-size: 22px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 1px;\n"
"}\n"
"\n"
"QLabel#subtitleLabel {\n"
"    color: rgba(255, 255, 255, 215);\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QLabel.sectionTitle {\n"
"    color: #2B2F38;\n"
"    font-size: 14px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QFrame#noticeFrame {\n"
"    background: #FFF7ED;\n"
"    border: 1px solid #FED7AA;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QLabe"
                        "l.noticeText {\n"
"    color: #C2410C;\n"
"    font-size: 12px;\n"
"    line-height: 18px;\n"
"}\n"
"\n"
"QFrame#supportFrame {\n"
"    background: #F0FDF4;\n"
"    border: 1px solid #BBF7D0;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QLabel#supportTitleLabel {\n"
"    color: #15803D;\n"
"    font-size: 16px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#supportDescLabel {\n"
"    color: #4B5563;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QLabel#label_image {\n"
"    background: #FFFFFF;\n"
"    border: 1px solid #DDE7F0;\n"
"    border-radius: 12px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QFrame#infoFrame {\n"
"    background: #F8FAFC;\n"
"    border: 1px solid #E2E8F0;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QLabel.infoName {\n"
"    color: #64748B;\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"QLabel.infoValue {\n"
"    color: #1F2937;\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"QLabel#label_version,\n"
"QLabel#label_qq {\n"
"    color: #2563EB;\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"QLabel#label_version:hover,\n"
""
                        "QLabel#label_qq:hover {\n"
"    color: #F57C00;\n"
"}\n"
"\n"
"QLabel#footerLabel {\n"
"    color: #94A3B8;\n"
"    font-size: 11px;\n"
"}")
        self.mainLayout = QVBoxLayout(About)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(18, 18, 18, 18)
        self.cardFrame = QFrame(About)
        self.cardFrame.setObjectName(u"cardFrame")
        self.cardFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.cardFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.cardLayout = QVBoxLayout(self.cardFrame)
        self.cardLayout.setSpacing(14)
        self.cardLayout.setObjectName(u"cardLayout")
        self.cardLayout.setContentsMargins(18, 18, 18, 16)
        self.headerFrame = QFrame(self.cardFrame)
        self.headerFrame.setObjectName(u"headerFrame")
        self.headerFrame.setMinimumSize(QSize(0, 96))
        self.headerFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.headerFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.headerLayout = QVBoxLayout(self.headerFrame)
        self.headerLayout.setSpacing(6)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(18, 16, 18, 16)
        self.headerTopSpacer = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.headerLayout.addItem(self.headerTopSpacer)

        self.titleLabel = QLabel(self.headerFrame)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.headerLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(self.headerFrame)
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        self.subtitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.headerLayout.addWidget(self.subtitleLabel)

        self.headerBottomSpacer = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.headerLayout.addItem(self.headerBottomSpacer)


        self.cardLayout.addWidget(self.headerFrame)

        self.noticeFrame = QFrame(self.cardFrame)
        self.noticeFrame.setObjectName(u"noticeFrame")
        self.noticeFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.noticeFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.noticeLayout = QVBoxLayout(self.noticeFrame)
        self.noticeLayout.setSpacing(8)
        self.noticeLayout.setObjectName(u"noticeLayout")
        self.noticeLayout.setContentsMargins(14, 12, 14, 12)
        self.noticeTitleLabel = QLabel(self.noticeFrame)
        self.noticeTitleLabel.setObjectName(u"noticeTitleLabel")
        self.noticeTitleLabel.setStyleSheet(u"color: #9A3412; font-size: 14px; font-weight: 700;")
        self.noticeTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.noticeLayout.addWidget(self.noticeTitleLabel)

        self.label = QLabel(self.noticeFrame)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"QLabel { color: #C2410C; font-size: 12px; }")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        self.noticeLayout.addWidget(self.label)

        self.label_2 = QLabel(self.noticeFrame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"QLabel { color: #C2410C; font-size: 12px; }")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(True)

        self.noticeLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.noticeFrame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"QLabel { color: #C2410C; font-size: 12px; }")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setWordWrap(True)

        self.noticeLayout.addWidget(self.label_3)

        self.label_4 = QLabel(self.noticeFrame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"QLabel { color: #DB2777; font-size: 12px; font-weight: 600; }")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setWordWrap(True)

        self.noticeLayout.addWidget(self.label_4)


        self.cardLayout.addWidget(self.noticeFrame)

        self.supportFrame = QFrame(self.cardFrame)
        self.supportFrame.setObjectName(u"supportFrame")
        self.supportFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.supportFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.supportLayout = QVBoxLayout(self.supportFrame)
        self.supportLayout.setSpacing(10)
        self.supportLayout.setObjectName(u"supportLayout")
        self.supportLayout.setContentsMargins(14, 12, 14, 14)
        self.label_7 = QLabel(self.supportFrame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"QLabel { color: #15803D; font-size: 16px; font-weight: 700; }")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.supportLayout.addWidget(self.label_7)

        self.supportDescLabel = QLabel(self.supportFrame)
        self.supportDescLabel.setObjectName(u"supportDescLabel")
        self.supportDescLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.supportLayout.addWidget(self.supportDescLabel)

        self.imageLayout = QHBoxLayout()
        self.imageLayout.setSpacing(0)
        self.imageLayout.setObjectName(u"imageLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.imageLayout.addItem(self.horizontalSpacer)

        self.label_image = QLabel(self.supportFrame)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setMinimumSize(QSize(132, 132))
        self.label_image.setMaximumSize(QSize(132, 132))
        self.label_image.setScaledContents(True)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imageLayout.addWidget(self.label_image)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.imageLayout.addItem(self.horizontalSpacer_2)


        self.supportLayout.addLayout(self.imageLayout)


        self.cardLayout.addWidget(self.supportFrame)

        self.infoFrame = QFrame(self.cardFrame)
        self.infoFrame.setObjectName(u"infoFrame")
        self.infoFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.infoFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout = QGridLayout(self.infoFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(14, 12, 14, 12)
        self.label_9 = QLabel(self.infoFrame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"QLabel { color: #64748B; font-weight: 600; }")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_version = QLabel(self.infoFrame)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setStyleSheet(u"QLabel { color: #2563EB; font-weight: 600; } QLabel:hover { color: #F57C00; }")
        self.label_version.setOpenExternalLinks(True)
        self.label_version.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_version, 0, 1, 1, 1)

        self.label_11 = QLabel(self.infoFrame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"QLabel { color: #64748B; font-weight: 600; }")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.label_qq = QLabel(self.infoFrame)
        self.label_qq.setObjectName(u"label_qq")
        self.label_qq.setStyleSheet(u"QLabel { color: #2563EB; font-weight: 600; } QLabel:hover { color: #F57C00; }")
        self.label_qq.setOpenExternalLinks(True)
        self.label_qq.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.label_qq, 1, 1, 1, 1)


        self.cardLayout.addWidget(self.infoFrame)

        self.footerLabel = QLabel(self.cardFrame)
        self.footerLabel.setObjectName(u"footerLabel")
        self.footerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cardLayout.addWidget(self.footerLabel)


        self.mainLayout.addWidget(self.cardFrame)


        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"\u5173\u4e8e", None))
        self.titleLabel.setText(QCoreApplication.translate("About", u"QsBeanfun", None))
        self.subtitleLabel.setText(QCoreApplication.translate("About", u"\u5173\u4e8e\u672c\u7a0b\u5e8f\u4e0e\u4f7f\u7528\u8bf4\u660e", None))
        self.noticeTitleLabel.setText(QCoreApplication.translate("About", u"\u91cd\u8981\u63d0\u793a", None))
        self.label.setText(QCoreApplication.translate("About", u"\u672c\u7a0b\u5f0f\u4e0d\u662f\u6e38\u620f\u6a58\u5b50\u6570\u4f4d\u79d1\u6280\u5f00\u53d1\u7684\u5ba2\u6237\u7aef\u7a0b\u5e8f", None))
        self.label_2.setText(QCoreApplication.translate("About", u"\u4f7f\u7528\u672c\u7a0b\u5f0f\u8bf7\u786e\u4fdd\u4e0b\u8f7d\u9014\u5f84\u662f\u5426\u4e3a\u4f5c\u8005\u63d0\u4f9b\u7684\u4e0b\u8f7d\u9014\u5f84", None))
        self.label_3.setText(QCoreApplication.translate("About", u"\u4f7f\u7528\u672c\u7a0b\u5f0f\u9020\u6210\u7684\u4e00\u5207\u540e\u679c\u7531\u4f7f\u7528\u8005\u627f\u62c5", None))
        self.label_4.setText(QCoreApplication.translate("About", u"\u6240\u6709\u4e0d\u6000\u597d\u610f\u7684\u6307\u8d23...\u90fd\u9700\u8981\u65f6\u95f4\u53bb\u9a8c\u8bc1\uff01", None))
        self.label_7.setText(QCoreApplication.translate("About", u"\u5982\u679c\u60a8\u6761\u4ef6\u5141\u8bb8\uff0c\u671b\u541b\u8d5e\u8d4f", None))
        self.supportDescLabel.setText(QCoreApplication.translate("About", u"\u60a8\u7684\u652f\u6301\u662f\u6301\u7eed\u7ef4\u62a4\u4e0e\u4f18\u5316\u7684\u52a8\u529b", None))
        self.label_9.setText(QCoreApplication.translate("About", u"Version", None))
        self.label_version.setText(QCoreApplication.translate("About", u"0.0.0", None))
        self.label_11.setText(QCoreApplication.translate("About", u"\u4f5c\u8005 QQ", None))
        self.label_qq.setText(QCoreApplication.translate("About", u"1140526018", None))
        self.footerLabel.setText(QCoreApplication.translate("About", u"Thank you for using QsBeanfun", None))
    # retranslateUi

