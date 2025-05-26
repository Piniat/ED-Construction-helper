# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ed-construction-helpereACPxY.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(928, 801)
        MainWindow.setMinimumSize(QSize(928, 801))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.quit_button = QPushButton(self.centralwidget)
        self.quit_button.setObjectName(u"quit_button")

        self.gridLayout.addWidget(self.quit_button, 1, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(916, 685))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setAcceptDrops(False)
        self.horizontalLayout = QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_5 = QFrame(self.tab)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setAutoFillBackground(True)
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_2 = QFrame(self.frame_5)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.textBrowser_3 = QTextBrowser(self.frame_2)
        self.textBrowser_3.setObjectName(u"textBrowser_3")
        sizePolicy.setHeightForWidth(self.textBrowser_3.sizePolicy().hasHeightForWidth())
        self.textBrowser_3.setSizePolicy(sizePolicy)
        self.textBrowser_3.setMinimumSize(QSize(531, 501))

        self.gridLayout_4.addWidget(self.textBrowser_3, 1, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy1.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy1)
        self.frame_4.setMinimumSize(QSize(531, 61))
        self.frame_4.setMaximumSize(QSize(16777215, 82))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.textBrowser_2 = QTextBrowser(self.frame_4)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setMinimumSize(QSize(551, 61))
        self.textBrowser_2.setMaximumSize(QSize(16777215, 72))

        self.verticalLayout_4.addWidget(self.textBrowser_2)


        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(500, 81))
        self.frame_3.setMaximumSize(QSize(600, 84))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.Percent_display = QTextBrowser(self.frame_3)
        self.Percent_display.setObjectName(u"Percent_display")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Percent_display.sizePolicy().hasHeightForWidth())
        self.Percent_display.setSizePolicy(sizePolicy2)
        self.Percent_display.setMinimumSize(QSize(100, 40))
        self.Percent_display.setMaximumSize(QSize(256, 40))
        self.Percent_display.setMouseTracking(False)
        self.Percent_display.setAcceptDrops(False)
        self.Percent_display.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Percent_display.setOpenLinks(False)

        self.gridLayout_3.addWidget(self.Percent_display, 0, 2, 1, 1)

        self.textBrowser = QTextBrowser(self.frame_3)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy3)
        self.textBrowser.setMinimumSize(QSize(256, 40))
        self.textBrowser.setMaximumSize(QSize(256, 40))
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.gridLayout_3.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.progressBar = QProgressBar(self.frame_3)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy4)
        self.progressBar.setMaximumSize(QSize(16777215, 26))
        self.progressBar.setAutoFillBackground(True)
        self.progressBar.setValue(100)
        self.progressBar.setTextVisible(False)

        self.gridLayout_3.addWidget(self.progressBar, 2, 0, 1, 3)


        self.gridLayout_4.addWidget(self.frame_3, 2, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.frame = QFrame(self.frame_5)
        self.frame.setObjectName(u"frame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy5)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.extra_info = QTextBrowser(self.frame)
        self.extra_info.setObjectName(u"extra_info")

        self.verticalLayout_3.addWidget(self.extra_info)

        self.trip_display = QTextBrowser(self.frame)
        self.trip_display.setObjectName(u"trip_display")
        sizePolicy1.setHeightForWidth(self.trip_display.sizePolicy().hasHeightForWidth())
        self.trip_display.setSizePolicy(sizePolicy1)
        self.trip_display.setMaximumSize(QSize(16777215, 40))
        self.trip_display.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.trip_display.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.verticalLayout_3.addWidget(self.trip_display)

        self.create_shopping = QPushButton(self.frame)
        self.create_shopping.setObjectName(u"create_shopping")

        self.verticalLayout_3.addWidget(self.create_shopping)

        self.copy_list = QPushButton(self.frame)
        self.copy_list.setObjectName(u"copy_list")

        self.verticalLayout_3.addWidget(self.copy_list)

        self.delete_file = QPushButton(self.frame)
        self.delete_file.setObjectName(u"delete_file")

        self.verticalLayout_3.addWidget(self.delete_file)

        self.horizontalSpacer = QSpacerItem(200, 25, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.verticalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy4)
        self.pushButton.setMouseTracking(False)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setCheckable(True)
        self.pushButton.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy4)
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy4.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy4)
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setChecked(False)
        self.pushButton_3.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.pushButton_3)


        self.horizontalLayout_2.addWidget(self.frame)


        self.horizontalLayout.addWidget(self.frame_5)

        self.tabWidget.addTab(self.tab, "")
        self.Inara = QWidget()
        self.Inara.setObjectName(u"Inara")
        self.gridLayout_2 = QGridLayout(self.Inara)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.webEngineView = QWebEngineView(self.Inara)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setUrl(QUrl(u"https://inara.cz/elite/commodities/"))

        self.gridLayout_2.addWidget(self.webEngineView, 0, 0, 1, 1)

        self.tabWidget.addTab(self.Inara, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ED-Construction-helper", None))
        self.quit_button.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; font-weight:700;\">Construction material list</span></p></body></html>", None))
        self.Percent_display.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:700;\">Null</span></p></body></html>", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:700;\">Construction Progress:</span></p></body></html>", None))
        self.trip_display.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.create_shopping.setText(QCoreApplication.translate("MainWindow", u"Create shopping list", None))
#if QT_CONFIG(tooltip)
        self.copy_list.setToolTip(QCoreApplication.translate("MainWindow", u"Copies the delivery list to the shopping list", None))
#endif // QT_CONFIG(tooltip)
        self.copy_list.setText(QCoreApplication.translate("MainWindow", u"Copy lists", None))
        self.delete_file.setText(QCoreApplication.translate("MainWindow", u"Delete progress file", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Construction Tracker", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Shopping List", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Journal Monitor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tracker", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Inara), QCoreApplication.translate("MainWindow", u"Inara", None))
    # retranslateUi

