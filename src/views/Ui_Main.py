# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_Main.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Main(object):
    def setupUi(self, Main):
        if not Main.objectName():
            Main.setObjectName(u"Main")
        Main.resize(350, 310)
        Main.setMinimumSize(QSize(350, 310))
        Main.setMaximumSize(QSize(350, 310))
        self.verticalLayout = QVBoxLayout(Main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_logoView = QLabel(Main)
        self.label_logoView.setObjectName(u"label_logoView")
        self.label_logoView.setMaximumSize(QSize(16777215, 80))
        self.label_logoView.setStyleSheet(u"padding:0px;border:0px;background:#40444F;")
        self.label_logoView.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_logoView)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.widget = QWidget(Main)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setContentsMargins(-1, 1, -1, 1)
        self.label_points = QLabel(self.widget)
        self.label_points.setObjectName(u"label_points")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_points.sizePolicy().hasHeightForWidth())
        self.label_points.setSizePolicy(sizePolicy)
        palette = QPalette()
        brush = QBrush(QColor(255, 108, 23, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.label_points.setPalette(palette)
        self.label_points.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.label_points.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_points, 0, 1, 1, 1)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.comboBox_gameAct = QComboBox(self.widget)
        self.comboBox_gameAct.setObjectName(u"comboBox_gameAct")
        sizePolicy.setHeightForWidth(self.comboBox_gameAct.sizePolicy().hasHeightForWidth())
        self.comboBox_gameAct.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.comboBox_gameAct, 3, 1, 1, 3)

        self.lineEdit_numAct = QLineEdit(self.widget)
        self.lineEdit_numAct.setObjectName(u"lineEdit_numAct")
        sizePolicy.setHeightForWidth(self.lineEdit_numAct.sizePolicy().hasHeightForWidth())
        self.lineEdit_numAct.setSizePolicy(sizePolicy)
        self.lineEdit_numAct.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_numAct.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_numAct, 5, 1, 1, 3)

        self.label_status = QLabel(self.widget)
        self.label_status.setObjectName(u"label_status")
        sizePolicy.setHeightForWidth(self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizePolicy)
        self.label_status.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_status, 0, 3, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 9, 0, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.lineEdit_dynamicPwd = QLineEdit(self.widget)
        self.lineEdit_dynamicPwd.setObjectName(u"lineEdit_dynamicPwd")
        sizePolicy.setHeightForWidth(self.lineEdit_dynamicPwd.sizePolicy().hasHeightForWidth())
        self.lineEdit_dynamicPwd.setSizePolicy(sizePolicy)
        self.lineEdit_dynamicPwd.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_dynamicPwd.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_dynamicPwd, 9, 1, 1, 3)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)


        self.verticalLayout_3.addWidget(self.widget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 1, 9, 1)
        self.pushButton_config = QPushButton(Main)
        self.pushButton_config.setObjectName(u"pushButton_config")
        self.pushButton_config.setMaximumSize(QSize(48, 16777215))

        self.horizontalLayout_2.addWidget(self.pushButton_config)

        self.pushButton_loginOut = QPushButton(Main)
        self.pushButton_loginOut.setObjectName(u"pushButton_loginOut")
        self.pushButton_loginOut.setMaximumSize(QSize(48, 16777215))

        self.horizontalLayout_2.addWidget(self.pushButton_loginOut)

        self.pushButton_createAct = QPushButton(Main)
        self.pushButton_createAct.setObjectName(u"pushButton_createAct")
        self.pushButton_createAct.setMaximumSize(QSize(64, 16777215))

        self.horizontalLayout_2.addWidget(self.pushButton_createAct)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.checkBox_autoInput = QCheckBox(Main)
        self.checkBox_autoInput.setObjectName(u"checkBox_autoInput")
        self.checkBox_autoInput.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox_autoInput)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, -1, 9, -1)
        self.pushButton_start = QPushButton(Main)
        self.pushButton_start.setObjectName(u"pushButton_start")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_start.sizePolicy().hasHeightForWidth())
        self.pushButton_start.setSizePolicy(sizePolicy1)
        self.pushButton_start.setMinimumSize(QSize(0, 36))

        self.horizontalLayout.addWidget(self.pushButton_start)

        self.pushButton_classic = QPushButton(Main)
        self.pushButton_classic.setObjectName(u"pushButton_classic")
        sizePolicy1.setHeightForWidth(self.pushButton_classic.sizePolicy().hasHeightForWidth())
        self.pushButton_classic.setSizePolicy(sizePolicy1)
        self.pushButton_classic.setMinimumSize(QSize(0, 36))

        self.horizontalLayout.addWidget(self.pushButton_classic)

        self.pushButton_dynamicPwd = QPushButton(Main)
        self.pushButton_dynamicPwd.setObjectName(u"pushButton_dynamicPwd")
        sizePolicy1.setHeightForWidth(self.pushButton_dynamicPwd.sizePolicy().hasHeightForWidth())
        self.pushButton_dynamicPwd.setSizePolicy(sizePolicy1)
        self.pushButton_dynamicPwd.setMinimumSize(QSize(0, 36))

        self.horizontalLayout.addWidget(self.pushButton_dynamicPwd)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout.setStretch(0, 1)
        QWidget.setTabOrder(self.comboBox_gameAct, self.lineEdit_numAct)
        QWidget.setTabOrder(self.lineEdit_numAct, self.lineEdit_dynamicPwd)

        self.retranslateUi(Main)

        QMetaObject.connectSlotsByName(Main)
    # setupUi

    def retranslateUi(self, Main):
        Main.setWindowTitle(QCoreApplication.translate("Main", u"QsBeanfun", None))
        self.label_logoView.setText("")
        self.label_points.setText(QCoreApplication.translate("Main", u"0[0]", None))
        self.label_4.setText(QCoreApplication.translate("Main", u"\u6578\u5b57\u8d26\u53f7", None))
        self.label_status.setText(QCoreApplication.translate("Main", u"\u6b63\u5e38", None))
        self.label_2.setText(QCoreApplication.translate("Main", u"\u4e50\u8c46", None))
        self.label_5.setText(QCoreApplication.translate("Main", u"\u52a8\u6001\u5bc6\u4ee4", None))
        self.label.setText(QCoreApplication.translate("Main", u"\u6e38\u620f\u8d26\u53f7", None))
        self.label_3.setText(QCoreApplication.translate("Main", u"\u8d26\u53f7\u72b6\u6001", None))
        self.pushButton_config.setText(QCoreApplication.translate("Main", u"\u8bbe\u7f6e", None))
        self.pushButton_loginOut.setText(QCoreApplication.translate("Main", u"\u767b\u51fa", None))
        self.pushButton_createAct.setText(QCoreApplication.translate("Main", u"\u65b0\u5efa\u8d26\u53f7", None))
        self.checkBox_autoInput.setText(QCoreApplication.translate("Main", u"\u81ea\u52a8\u586b\u5165", None))
        self.pushButton_start.setText(QCoreApplication.translate("Main", u"\u542f\u52a8\u6e38\u620f", None))
        self.pushButton_classic.setText(QCoreApplication.translate("Main", u"\u8fdb\u5165\u7ecf\u5178\u7248", None))
        self.pushButton_dynamicPwd.setText(QCoreApplication.translate("Main", u"\u83b7\u53d6\u5bc6\u4ee4", None))
    # retranslateUi

