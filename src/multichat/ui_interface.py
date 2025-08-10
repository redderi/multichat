# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1246, 612)
        MainWindow.setStyleSheet(u"\n"
"    QMainWindow {\n"
"        background-color: #17212B;\n"
"    }\n"
"    QMenuBar {\n"
"        background-color: #1A252F;\n"
"        color: #E6ECEF;\n"
"        font-family: Roboto, Arial, sans-serif;\n"
"        font-size: 12pt;\n"
"        padding: 5px;\n"
"    }\n"
"    QMenuBar::item {\n"
"        background-color: #1A252F;\n"
"        color: #E6ECEF;\n"
"        padding: 5px 10px;\n"
"    }\n"
"    QMenuBar::item:selected {\n"
"        background-color: #5288C1;\n"
"    }\n"
"    QMenu {\n"
"        background-color: #1A252F;\n"
"        color: #E6ECEF;\n"
"        font-family: Roboto, Arial, sans-serif;\n"
"        font-size: 11pt;\n"
"        border: 1px solid #3F4B5A;\n"
"    }\n"
"    QMenu::item {\n"
"        padding: 5px 20px;\n"
"    }\n"
"    QMenu::item:selected {\n"
"        background-color: #5288C1;\n"
"        color: #FFFFFF;\n"
"    }\n"
"    QLabel {\n"
"        font-family: Roboto, Arial, sans-serif;\n"
"        font-size: 12pt;\n"
"        color: #E6ECEF;\n"
"    }\n"
"    QTextE"
                        "dit {\n"
"        font-family: Roboto, Arial, sans-serif;\n"
"        font-size: 12pt;\n"
"        color: #E6ECEF;\n"
"        background-color: #2B3743;\n"
"        border: 1px solid #3F4B5A;\n"
"        border-radius: 5px;\n"
"        padding: 5px;\n"
"    }\n"
"    QLineEdit {\n"
"        font-family: Roboto, Arial, sans-serif;\n"
"        font-size: 12pt;\n"
"        background-color: #2B3743;\n"
"        color: #E6ECEF;\n"
"        border: 1px solid #3F4B5A;\n"
"        border-radius: 5px;\n"
"        padding: 5px;\n"
"    }\n"
"    QLineEdit:focus {\n"
"        border: 1px solid #5288C1;\n"
"    }\n"
"    QLineEdit::placeholder {\n"
"        color: #6A7886;\n"
"    }\n"
"    QPushButton {\n"
"        font-family: Roboto, Arial, sans-serif;\n"
"        font-size: 10pt;\n"
"        background-color: #5288C1;\n"
"        color: #FFFFFF;\n"
"        border: none;\n"
"        padding: 8px;\n"
"        border-radius: 5px;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: #6A9ED1;\n"
"    }\n"
""
                        "    QPushButton:pressed {\n"
"        background-color: #3F6A9B;\n"
"    }\n"
"    QPushButton#sendButton {\n"
"        min-width: 50px;\n"
"    }\n"
"    QListWidget {\n"
"        font-family: Roboto, Arial, sans-serif;\n"
"        font-size: 11pt;\n"
"        background-color: #2B3743;\n"
"        color: #E6ECEF;\n"
"        border: 1px solid #3F4B5A;\n"
"        border-radius: 5px;\n"
"        padding: 5px;\n"
"    }\n"
"    QListWidget::item {\n"
"        padding: 5px;\n"
"    }\n"
"    QListWidget::item:selected {\n"
"        background-color: #5288C1;\n"
"        color: #FFFFFF;\n"
"    }\n"
"    QStatusBar {\n"
"        font-family: Roboto, Arial, sans-serif;\n"
"        font-size: 10pt;\n"
"        color: #E6ECEF;\n"
"        background-color: #1A252F;\n"
"    }\n"
"   ")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionLeaveGroup = QAction(MainWindow)
        self.actionLeaveGroup.setObjectName(u"actionLeaveGroup")
        self.actionJoinGroup = QAction(MainWindow)
        self.actionJoinGroup.setObjectName(u"actionJoinGroup")
        self.actionPeersBroadcast = QAction(MainWindow)
        self.actionPeersBroadcast.setObjectName(u"actionPeersBroadcast")
        self.actionPeersMulticast = QAction(MainWindow)
        self.actionPeersMulticast.setObjectName(u"actionPeersMulticast")
        self.actionPeersIgnore = QAction(MainWindow)
        self.actionPeersIgnore.setObjectName(u"actionPeersIgnore")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(6)
        self.mainLayout.setObjectName(u"mainLayout")
        self.sidebarLayout = QVBoxLayout()
        self.sidebarLayout.setSpacing(6)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.peersLabel = QLabel(self.centralwidget)
        self.peersLabel.setObjectName(u"peersLabel")
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(12)
        font.setBold(True)
        self.peersLabel.setFont(font)
        self.peersLabel.setStyleSheet(u"color: #E6ECEF; padding: 5px;")

        self.sidebarLayout.addWidget(self.peersLabel)

        self.peersList = QListWidget(self.centralwidget)
        self.peersList.setObjectName(u"peersList")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.peersList.sizePolicy().hasHeightForWidth())
        self.peersList.setSizePolicy(sizePolicy)

        self.sidebarLayout.addWidget(self.peersList)

        self.modeButtonsLayout = QHBoxLayout()
        self.modeButtonsLayout.setObjectName(u"modeButtonsLayout")
        self.broadcastButton = QPushButton(self.centralwidget)
        self.broadcastButton.setObjectName(u"broadcastButton")

        self.modeButtonsLayout.addWidget(self.broadcastButton)

        self.multicastButton = QPushButton(self.centralwidget)
        self.multicastButton.setObjectName(u"multicastButton")

        self.modeButtonsLayout.addWidget(self.multicastButton)

        self.sharedButton = QPushButton(self.centralwidget)
        self.sharedButton.setObjectName(u"sharedButton")

        self.modeButtonsLayout.addWidget(self.sharedButton)


        self.sidebarLayout.addLayout(self.modeButtonsLayout)

        self.clearButton = QPushButton(self.centralwidget)
        self.clearButton.setObjectName(u"clearButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.clearButton.setIcon(icon)
        self.clearButton.setIconSize(QSize(30, 30))

        self.sidebarLayout.addWidget(self.clearButton)

        self.infoButton = QPushButton(self.centralwidget)
        self.infoButton.setObjectName(u"infoButton")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout))
        self.infoButton.setIcon(icon1)
        self.infoButton.setIconSize(QSize(30, 30))

        self.sidebarLayout.addWidget(self.infoButton)


        self.mainLayout.addLayout(self.sidebarLayout)

        self.chatLayout = QVBoxLayout()
        self.chatLayout.setSpacing(10)
        self.chatLayout.setObjectName(u"chatLayout")
        self.chatLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.chatLayout.setContentsMargins(8, 8, 8, 8)
        self.chatDisplay = QTextEdit(self.centralwidget)
        self.chatDisplay.setObjectName(u"chatDisplay")
        self.chatDisplay.setReadOnly(True)

        self.chatLayout.addWidget(self.chatDisplay)

        self.inputLayout = QHBoxLayout()
        self.inputLayout.setObjectName(u"inputLayout")
        self.messageInput = QLineEdit(self.centralwidget)
        self.messageInput.setObjectName(u"messageInput")

        self.inputLayout.addWidget(self.messageInput)

        self.sendButton = QPushButton(self.centralwidget)
        self.sendButton.setObjectName(u"sendButton")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailSend))
        self.sendButton.setIcon(icon2)
        self.sendButton.setIconSize(QSize(16, 16))

        self.inputLayout.addWidget(self.sendButton)


        self.chatLayout.addLayout(self.inputLayout)


        self.mainLayout.addLayout(self.chatLayout)


        self.verticalLayout.addLayout(self.mainLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1246, 39))
        self.menubar.setStyleSheet(u"background-color: #1A252F; color: #E6ECEF;")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuCommands = QMenu(self.menubar)
        self.menuCommands.setObjectName(u"menuCommands")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCommands.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuCommands.addAction(self.actionLeaveGroup)
        self.menuCommands.addAction(self.actionJoinGroup)
        self.menuCommands.addAction(self.actionPeersBroadcast)
        self.menuCommands.addAction(self.actionPeersMulticast)
        self.menuCommands.addAction(self.actionPeersIgnore)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Multichat", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit (/exit)", None))
        self.actionLeaveGroup.setText(QCoreApplication.translate("MainWindow", u"Leave Group (/leave_group)", None))
        self.actionJoinGroup.setText(QCoreApplication.translate("MainWindow", u"Join Group (/join_group)", None))
        self.actionPeersBroadcast.setText(QCoreApplication.translate("MainWindow", u"Show Broadcast Peers (/peers_broadcast)", None))
        self.actionPeersMulticast.setText(QCoreApplication.translate("MainWindow", u"Show Multicast Peers (/peers_multicast)", None))
        self.actionPeersIgnore.setText(QCoreApplication.translate("MainWindow", u"Show Ignored Peers (/peers_ignore)", None))
        self.peersLabel.setText(QCoreApplication.translate("MainWindow", u"\u0413\u0440\u0443\u043f\u043f\u044b", None))
        self.broadcastButton.setText(QCoreApplication.translate("MainWindow", u"Broadcast-\u0440\u0435\u0436\u0438\u043c", None))
        self.multicastButton.setText(QCoreApplication.translate("MainWindow", u"Multicast-\u0440\u0435\u0436\u0438\u043c", None))
        self.sharedButton.setText(QCoreApplication.translate("MainWindow", u"Shared-\u0440\u0435\u0436\u0438\u043c", None))
        self.clearButton.setText("")
        self.infoButton.setText("")
        self.chatDisplay.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Roboto','Arial','sans-serif'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.messageInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 \u0438\u043b\u0438 \u043a\u043e\u043c\u0430\u043d\u0434\u0443...", None))
        self.sendButton.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuCommands.setTitle(QCoreApplication.translate("MainWindow", u"Commands", None))
    # retranslateUi

