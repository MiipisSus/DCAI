# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_configs.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(536, 729)
        Form.setMinimumSize(QSize(400, 700))
        Form.setStyleSheet(u"QWidget\n"
"{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton\n"
"{\n"
"	background-color: transparent;\n"
"	border: 1px solid rgb(30, 48, 80);\n"
"	padding: 3px;\n"
"	border-radius: 3px;\n"
"}\n"
"QPushButton::hover\n"
"{\n"
"	background-color: rgb(222, 221, 218);\n"
"}\n"
"QPushButton::pressed\n"
"{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(30, 48, 80);\n"
"}\n"
"QCheckBox::indicator:!checked\n"
"{\n"
"	border-image: url(:/images/images/checkBox.svg)1 0 1 0;\n"
"}\n"
"QCheckBox::indicator:checked\n"
"{\n"
"	border-image: url(:/images/images/checkBox_checked.svg) 1 0 1 0;\n"
"}\n"
"QLineEdit:enabled\n"
"{\n"
"	border: 1px solid rgb(30, 48, 80);\n"
"	border-radius: 3px;\n"
"	padding: 1px 0px 1px 0px;\n"
"}\n"
"QTextEdit:enabled\n"
"{\n"
"	border: 1px solid rgb(30, 48, 80);\n"
"	border-radius: 3px;\n"
"	padding: 1px 0px 1px 0px;\n"
"}\n"
"QComboBox\n"
"{\n"
"	border: 1px solid rgb(30, 48, 80);\n"
"	border-radius: 3px;\n"
"	combobox-popup:0;\n"
"}\n"
"QComboBox::drop-down\n"
"{\n"
""
                        "	border: 0px;\n"
"}\n"
"QComboBox::down-arrow\n"
"{\n"
"	image: url(:/images/images/down_arrow.svg);\n"
"}\n"
"QComboBox::down-arrow:on\n"
"{\n"
"	image: url(:/images/images/up_arrow.svg);\n"
"}\n"
"QComboBox QAbstractItemView\n"
"{\n"
"	border: 1px solid rgb(30, 48, 80);\n"
"	border-radius: 3px;\n"
"}")
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.importConfigButton = QPushButton(Form)
        self.importConfigButton.setObjectName(u"importConfigButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importConfigButton.sizePolicy().hasHeightForWidth())
        self.importConfigButton.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.importConfigButton, 0, 1, 1, 1)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget::tab\n"
"{\n"
"	background-color: rgb(30, 48, 80);\n"
"}")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.colorCodeLabel = QLabel(self.tab)
        self.colorCodeLabel.setObjectName(u"colorCodeLabel")
        self.colorCodeLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.colorCodeLabel, 8, 1, 1, 1)

        self.characterAITokenLineEdit = QLineEdit(self.tab)
        self.characterAITokenLineEdit.setObjectName(u"characterAITokenLineEdit")
        self.characterAITokenLineEdit.setStyleSheet(u"QLineEdit[state = \"red\"]\n"
"{\n"
"	border: 2px solid rgb(224, 27, 36);\n"
"	border-radius: 3px;\n"
"	padding: 1px 0px 1px 0px;\n"
"}")

        self.gridLayout_2.addWidget(self.characterAITokenLineEdit, 1, 0, 1, 3)

        self.widget = QWidget(self.tab)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.widget.setMinimumSize(QSize(0, 40))
        self.horizontalLayout_5 = QHBoxLayout(self.widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.ExportHintLabel = QLabel(self.widget)
        self.ExportHintLabel.setObjectName(u"ExportHintLabel")
        self.ExportHintLabel.setStyleSheet(u"QLabel[state = \"red\"]\n"
"{\n"
"	color: rgb(224, 27, 36);\n"
"	font-weight: bold;\n"
"}\n"
"QLabel[state = \"green\"]\n"
"{\n"
"	color: rgb(38, 162, 105);\n"
"	font-weight: bold;\n"
"}")
        self.ExportHintLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.ExportHintLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.gridLayout_2.addWidget(self.widget, 13, 0, 1, 3)

        self.chooseColorPushButton = QPushButton(self.tab)
        self.chooseColorPushButton.setObjectName(u"chooseColorPushButton")
        sizePolicy.setHeightForWidth(self.chooseColorPushButton.sizePolicy().hasHeightForWidth())
        self.chooseColorPushButton.setSizePolicy(sizePolicy)
        self.chooseColorPushButton.setMaximumSize(QSize(21, 21))
        self.chooseColorPushButton.setStyleSheet(u"QPushButton\n"
"{\n"
"	background-color: transparent;\n"
"	border: 1px solid rgb(30, 48, 80);\n"
"	border-radius: 3px;\n"
"}\n"
"QPushButton::hover\n"
"{\n"
"	background-color: rgb(222, 221, 218);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/images/images/chooseColorPushButton.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.chooseColorPushButton.setIcon(icon)

        self.gridLayout_2.addWidget(self.chooseColorPushButton, 8, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.exportConfigButton = QPushButton(self.tab)
        self.exportConfigButton.setObjectName(u"exportConfigButton")
        self.exportConfigButton.setMinimumSize(QSize(85, 0))
        self.exportConfigButton.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.exportConfigButton)

        self.clearPushButton = QPushButton(self.tab)
        self.clearPushButton.setObjectName(u"clearPushButton")
        sizePolicy.setHeightForWidth(self.clearPushButton.sizePolicy().hasHeightForWidth())
        self.clearPushButton.setSizePolicy(sizePolicy)
        self.clearPushButton.setMinimumSize(QSize(85, 0))
        self.clearPushButton.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.clearPushButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.gridLayout_2.addLayout(self.horizontalLayout, 14, 0, 1, 3)

        self.enableTranslaterCheckBox = QCheckBox(self.tab)
        self.enableTranslaterCheckBox.setObjectName(u"enableTranslaterCheckBox")

        self.gridLayout_2.addWidget(self.enableTranslaterCheckBox, 6, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_11.addWidget(self.label_7)

        self.characterIDHintPushButton = QPushButton(self.tab)
        self.characterIDHintPushButton.setObjectName(u"characterIDHintPushButton")
        sizePolicy.setHeightForWidth(self.characterIDHintPushButton.sizePolicy().hasHeightForWidth())
        self.characterIDHintPushButton.setSizePolicy(sizePolicy)
        self.characterIDHintPushButton.setMaximumSize(QSize(20, 20))
        self.characterIDHintPushButton.setStyleSheet(u"QPushButton\n"
"{\n"
"	background-color: transparent;\n"
"	border: 1px solid rgb(30, 48, 80);\n"
"	border-radius: 3px;\n"
"}\n"
"QPushButton::hover\n"
"{\n"
"	background-color: rgb(222, 221, 218);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/images/images/HintPushButton.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.characterIDHintPushButton.setIcon(icon1)
        self.characterIDHintPushButton.setIconSize(QSize(16, 16))

        self.horizontalLayout_11.addWidget(self.characterIDHintPushButton)

        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_11.addWidget(self.label_10)

        self.characterNameLabel = QLabel(self.tab)
        self.characterNameLabel.setObjectName(u"characterNameLabel")

        self.horizontalLayout_11.addWidget(self.characterNameLabel)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_18)


        self.gridLayout_2.addLayout(self.horizontalLayout_11, 4, 0, 1, 3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.characterAITokenHintPushButton = QPushButton(self.tab)
        self.characterAITokenHintPushButton.setObjectName(u"characterAITokenHintPushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.characterAITokenHintPushButton.sizePolicy().hasHeightForWidth())
        self.characterAITokenHintPushButton.setSizePolicy(sizePolicy2)
        self.characterAITokenHintPushButton.setMaximumSize(QSize(20, 20))
        self.characterAITokenHintPushButton.setStyleSheet(u"QPushButton\n"
"{\n"
"	background-color: transparent;\n"
"	border: 1px solid rgb(30, 48, 80);\n"
"	border-radius: 3px;\n"
"}\n"
"QPushButton::hover\n"
"{\n"
"	background-color: rgb(222, 221, 218);\n"
"}")
        self.characterAITokenHintPushButton.setIcon(icon1)
        self.characterAITokenHintPushButton.setIconSize(QSize(14, 16))

        self.horizontalLayout_3.addWidget(self.characterAITokenHintPushButton)

        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_3.addWidget(self.label_9)

        self.createrIDLabel = QLabel(self.tab)
        self.createrIDLabel.setObjectName(u"createrIDLabel")

        self.horizontalLayout_3.addWidget(self.createrIDLabel)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_10)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 3)

        self.GroupChannelChatCheckBox = QCheckBox(self.tab)
        self.GroupChannelChatCheckBox.setObjectName(u"GroupChannelChatCheckBox")

        self.gridLayout_2.addWidget(self.GroupChannelChatCheckBox, 10, 0, 1, 1)

        self.translateConfigWidget = QWidget(self.tab)
        self.translateConfigWidget.setObjectName(u"translateConfigWidget")
        self.translateConfigWidget.setEnabled(True)
        self.translateConfigWidget.setStyleSheet(u"QWidget:!enabled\n"
"{\n"
"	background-color: rgb(246, 245, 244);\n"
"}")
        self.gridLayout = QGridLayout(self.translateConfigWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.translateConfigWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.APIKeyLineEdit = QLineEdit(self.translateConfigWidget)
        self.APIKeyLineEdit.setObjectName(u"APIKeyLineEdit")

        self.gridLayout.addWidget(self.APIKeyLineEdit, 3, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_5 = QLabel(self.translateConfigWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_8.addWidget(self.label_5)

        self.translateModeComboBox = QComboBox(self.translateConfigWidget)
        self.translateModeComboBox.addItem("")
        self.translateModeComboBox.addItem("")
        self.translateModeComboBox.addItem("")
        self.translateModeComboBox.setObjectName(u"translateModeComboBox")

        self.horizontalLayout_8.addWidget(self.translateModeComboBox)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 3)

        self.gridLayout.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(self.translateConfigWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.targetLanguageComboBox = QComboBox(self.translateConfigWidget)
        self.targetLanguageComboBox.addItem("")
        self.targetLanguageComboBox.addItem("")
        self.targetLanguageComboBox.setObjectName(u"targetLanguageComboBox")

        self.horizontalLayout_7.addWidget(self.targetLanguageComboBox)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 3)

        self.gridLayout.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)

        self.APIKeyDescriptionTextEdit = QTextEdit(self.translateConfigWidget)
        self.APIKeyDescriptionTextEdit.setObjectName(u"APIKeyDescriptionTextEdit")
        self.APIKeyDescriptionTextEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.APIKeyDescriptionTextEdit, 4, 0, 1, 1)


        self.gridLayout_2.addWidget(self.translateConfigWidget, 7, 0, 1, 3)

        self.DiscordBotTokenLineEdit = QLineEdit(self.tab)
        self.DiscordBotTokenLineEdit.setObjectName(u"DiscordBotTokenLineEdit")
        self.DiscordBotTokenLineEdit.setStyleSheet(u"QLineEdit[state = \"red\"]\n"
"{\n"
"	border: 2px solid rgb(224, 27, 36);\n"
"	border-radius: 3px;\n"
"	padding: 1px 0px 1px 0px;\n"
"}")

        self.gridLayout_2.addWidget(self.DiscordBotTokenLineEdit, 3, 0, 1, 3)

        self.characterIDLineEdit = QLineEdit(self.tab)
        self.characterIDLineEdit.setObjectName(u"characterIDLineEdit")
        self.characterIDLineEdit.setStyleSheet(u"QLineEdit[state = \"red\"]\n"
"{\n"
"	border: 2px solid rgb(224, 27, 36);\n"
"	border-radius: 3px;\n"
"	padding: 1px 0px 1px 0px;\n"
"}")

        self.gridLayout_2.addWidget(self.characterIDLineEdit, 5, 0, 1, 3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.DiscordBotTokenHintPushButton = QPushButton(self.tab)
        self.DiscordBotTokenHintPushButton.setObjectName(u"DiscordBotTokenHintPushButton")
        sizePolicy.setHeightForWidth(self.DiscordBotTokenHintPushButton.sizePolicy().hasHeightForWidth())
        self.DiscordBotTokenHintPushButton.setSizePolicy(sizePolicy)
        self.DiscordBotTokenHintPushButton.setMaximumSize(QSize(20, 20))
        self.DiscordBotTokenHintPushButton.setStyleSheet(u"QPushButton\n"
"{\n"
"	background-color: transparent;\n"
"	border: 1px solid rgb(30, 48, 80);\n"
"	border-radius: 3px;\n"
"}\n"
"QPushButton::hover\n"
"{\n"
"	background-color: rgb(222, 221, 218);\n"
"}")
        self.DiscordBotTokenHintPushButton.setIcon(icon1)
        self.DiscordBotTokenHintPushButton.setIconSize(QSize(16, 16))

        self.horizontalLayout_4.addWidget(self.DiscordBotTokenHintPushButton)

        self.label_11 = QLabel(self.tab)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_4.addWidget(self.label_11)

        self.discordBotStatusLabel = QLabel(self.tab)
        self.discordBotStatusLabel.setObjectName(u"discordBotStatusLabel")
        self.discordBotStatusLabel.setStyleSheet(u"QLabel[state = \"red\"]\n"
"{\n"
"	color: rgb(224, 27, 36);\n"
"	font-weight: bold;\n"
"}\n"
"QLabel[state = \"green\"]\n"
"{\n"
"	color: rgb(38, 162, 105);\n"
"	font-weight: bold;\n"
"}")

        self.horizontalLayout_4.addWidget(self.discordBotStatusLabel)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_11)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 0, 1, 3)

        self.DMChannelChatCheckBox = QCheckBox(self.tab)
        self.DMChannelChatCheckBox.setObjectName(u"DMChannelChatCheckBox")

        self.gridLayout_2.addWidget(self.DMChannelChatCheckBox, 9, 0, 1, 1)

        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 8, 0, 1, 1)

        self.BotChatCheckBox = QCheckBox(self.tab)
        self.BotChatCheckBox.setObjectName(u"BotChatCheckBox")

        self.gridLayout_2.addWidget(self.BotChatCheckBox, 11, 0, 1, 1)

        self.changeAvatarCheckBox = QCheckBox(self.tab)
        self.changeAvatarCheckBox.setObjectName(u"changeAvatarCheckBox")

        self.gridLayout_2.addWidget(self.changeAvatarCheckBox, 12, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_3 = QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.refreshAdminPushButton = QPushButton(self.tab_2)
        self.refreshAdminPushButton.setObjectName(u"refreshAdminPushButton")

        self.gridLayout_3.addWidget(self.refreshAdminPushButton, 0, 0, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(268, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_13, 0, 1, 1, 1)

        self.adminInfoTableWidget = QTableWidget(self.tab_2)
        if (self.adminInfoTableWidget.columnCount() < 3):
            self.adminInfoTableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.adminInfoTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.adminInfoTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.adminInfoTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.adminInfoTableWidget.setObjectName(u"adminInfoTableWidget")

        self.gridLayout_3.addWidget(self.adminInfoTableWidget, 1, 0, 1, 2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_8)

        self.updateAdminPushButton = QPushButton(self.tab_2)
        self.updateAdminPushButton.setObjectName(u"updateAdminPushButton")
        self.updateAdminPushButton.setMinimumSize(QSize(85, 0))

        self.horizontalLayout_10.addWidget(self.updateAdminPushButton)

        self.restoreAdminPushButton = QPushButton(self.tab_2)
        self.restoreAdminPushButton.setObjectName(u"restoreAdminPushButton")
        self.restoreAdminPushButton.setMinimumSize(QSize(85, 0))

        self.horizontalLayout_10.addWidget(self.restoreAdminPushButton)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_9)


        self.gridLayout_3.addLayout(self.horizontalLayout_10, 3, 0, 1, 2)

        self.widget_2 = QWidget(self.tab_2)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.widget_2.setMinimumSize(QSize(0, 40))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.updateAdminHintLabel = QLabel(self.widget_2)
        self.updateAdminHintLabel.setObjectName(u"updateAdminHintLabel")
        self.updateAdminHintLabel.setStyleSheet(u"QLabel[state = \"red\"]\n"
"{\n"
"	color: rgb(224, 27, 36);\n"
"	font-weight: bold;\n"
"}\n"
"QLabel[state = \"green\"]\n"
"{\n"
"	color: rgb(38, 162, 105);\n"
"	font-weight: bold;\n"
"}")

        self.horizontalLayout_2.addWidget(self.updateAdminHintLabel)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)


        self.gridLayout_3.addWidget(self.widget_2, 2, 0, 1, 2)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_5 = QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.importVocabPushButton = QPushButton(self.tab_3)
        self.importVocabPushButton.setObjectName(u"importVocabPushButton")

        self.gridLayout_5.addWidget(self.importVocabPushButton, 0, 0, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(271, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_12, 0, 1, 1, 1)

        self.vocabInfoTableWidget = QTableWidget(self.tab_3)
        if (self.vocabInfoTableWidget.columnCount() < 2):
            self.vocabInfoTableWidget.setColumnCount(2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.vocabInfoTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.vocabInfoTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        self.vocabInfoTableWidget.setObjectName(u"vocabInfoTableWidget")

        self.gridLayout_5.addWidget(self.vocabInfoTableWidget, 1, 0, 1, 2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_14 = QSpacerItem(77, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_14)

        self.refreshVocabPushButton = QPushButton(self.tab_3)
        self.refreshVocabPushButton.setObjectName(u"refreshVocabPushButton")
        self.refreshVocabPushButton.setMinimumSize(QSize(85, 0))

        self.horizontalLayout_9.addWidget(self.refreshVocabPushButton)

        self.restoreVocabPushButton = QPushButton(self.tab_3)
        self.restoreVocabPushButton.setObjectName(u"restoreVocabPushButton")
        self.restoreVocabPushButton.setMinimumSize(QSize(85, 0))

        self.horizontalLayout_9.addWidget(self.restoreVocabPushButton)

        self.horizontalSpacer_15 = QSpacerItem(78, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_15)


        self.gridLayout_5.addLayout(self.horizontalLayout_9, 3, 0, 1, 2)

        self.widget_3 = QWidget(self.tab_3)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy1.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy1)
        self.widget_3.setMinimumSize(QSize(0, 40))
        self.horizontalLayout_6 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_16)

        self.updateVocabHintLabel = QLabel(self.widget_3)
        self.updateVocabHintLabel.setObjectName(u"updateVocabHintLabel")
        self.updateVocabHintLabel.setStyleSheet(u"QLabel[state = \"red\"]\n"
"{\n"
"	color: rgb(224, 27, 36);\n"
"	font-weight: bold;\n"
"}\n"
"QLabel[state = \"green\"]\n"
"{\n"
"	color: rgb(38, 162, 105);\n"
"	font-weight: bold;\n"
"}")

        self.horizontalLayout_6.addWidget(self.updateVocabHintLabel)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_17)


        self.gridLayout_5.addWidget(self.widget_3, 2, 0, 1, 2)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout_4.addWidget(self.tabWidget, 1, 1, 1, 4)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 0, 2, 1, 1)

        self.botNameLabel = QLabel(Form)
        self.botNameLabel.setObjectName(u"botNameLabel")
        self.botNameLabel.setStyleSheet(u"QLabel[state = \"green\"]\n"
"{\n"
"	color: rgb(38, 162, 105);\n"
"	font-weight: bold;\n"
"}")
        self.botNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.botNameLabel, 0, 3, 1, 2)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.importConfigButton.setText(QCoreApplication.translate("Form", u"\u532f\u5165\u8a2d\u5b9a", None))
        self.colorCodeLabel.setText("")
        self.ExportHintLabel.setText(QCoreApplication.translate("Form", u"\u5df2\u6210\u529f\u532f\u51fa\uff01", None))
        self.chooseColorPushButton.setText("")
        self.exportConfigButton.setText(QCoreApplication.translate("Form", u"\u532f\u51fa\u4e26\u5957\u7528", None))
        self.clearPushButton.setText(QCoreApplication.translate("Form", u"\u6e05\u7a7a", None))
        self.enableTranslaterCheckBox.setText(QCoreApplication.translate("Form", u"\u7ffb\u8b6f\u5668", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Character ID", None))
        self.characterIDHintPushButton.setText("")
        self.label_10.setText(QCoreApplication.translate("Form", u"Name: ", None))
        self.characterNameLabel.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"Character AI  TOKEN", None))
        self.characterAITokenHintPushButton.setText("")
        self.label_9.setText(QCoreApplication.translate("Form", u"Creator ID: ", None))
        self.createrIDLabel.setText("")
        self.GroupChannelChatCheckBox.setText(QCoreApplication.translate("Form", u"\u591a\u4eba\u6587\u5b57\u983b\u9053\u804a\u5929\u529f\u80fd", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"API KEY", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u7ffb\u8b6fAPI", None))
        self.translateModeComboBox.setItemText(0, QCoreApplication.translate("Form", u"Google Translate\uff08\u5efa\u8b70\uff09", None))
        self.translateModeComboBox.setItemText(1, QCoreApplication.translate("Form", u"OpenAI", None))
        self.translateModeComboBox.setItemText(2, QCoreApplication.translate("Form", u"Azure AI Translate", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"\u76ee\u6a19\u8a9e\u8a00", None))
        self.targetLanguageComboBox.setItemText(0, QCoreApplication.translate("Form", u"\u7e41\u9ad4\u4e2d\u6587\uff08\u9ed8\u8a8d\uff09", None))
        self.targetLanguageComboBox.setItemText(1, QCoreApplication.translate("Form", u"English", None))

        self.label_2.setText(QCoreApplication.translate("Form", u"Discord Bot TOKEN", None))
        self.DiscordBotTokenHintPushButton.setText("")
        self.label_11.setText(QCoreApplication.translate("Form", u"Status: ", None))
        self.discordBotStatusLabel.setText("")
        self.DMChannelChatCheckBox.setText(QCoreApplication.translate("Form", u"\u79c1\u4eba\u983b\u9053\u804a\u5929\u529f\u80fd", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Embed \u984f\u8272", None))
        self.BotChatCheckBox.setText(QCoreApplication.translate("Form", u"\u6a5f\u5668\u4eba\u4e00\u5c0d\u4e00\u804a\u5929\u529f\u80fd", None))
        self.changeAvatarCheckBox.setText(QCoreApplication.translate("Form", u"\u4ee5Character AI \u982d\u50cf\u4ee3\u66ff\u6a5f\u5668\u4eba\u982d\u50cf", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"\u65b0\u589e/\u4fee\u6539\u6a5f\u5668\u4eba", None))
        self.refreshAdminPushButton.setText(QCoreApplication.translate("Form", u"\u5237\u65b0", None))
        ___qtablewidgetitem = self.adminInfoTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"User ID", None));
        ___qtablewidgetitem1 = self.adminInfoTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"User Name", None));
        self.updateAdminPushButton.setText(QCoreApplication.translate("Form", u"\u66f4\u65b0", None))
        self.restoreAdminPushButton.setText(QCoreApplication.translate("Form", u"\u5fa9\u539f", None))
        self.updateAdminHintLabel.setText(QCoreApplication.translate("Form", u"\u5df2\u66f4\u65b0\u5b8c\u6210\uff01", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"\u7ba1\u7406\u54e1\u5217\u8868", None))
        self.importVocabPushButton.setText(QCoreApplication.translate("Form", u"\u532f\u5165csv\u6a94", None))
        ___qtablewidgetitem2 = self.vocabInfoTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u76ee\u6a19\u8a9e\u8a00", None));
        ___qtablewidgetitem3 = self.vocabInfoTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\u82f1\u6587\u7ffb\u8b6f", None));
        self.refreshVocabPushButton.setText(QCoreApplication.translate("Form", u"\u66f4\u65b0", None))
        self.restoreVocabPushButton.setText(QCoreApplication.translate("Form", u"\u5fa9\u539f", None))
        self.updateVocabHintLabel.setText(QCoreApplication.translate("Form", u"\u5df2\u66f4\u65b0\u5b8c\u6210\uff01", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"\u9801\u9762", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u76ee\u524d\u8a2d\u5b9a", None))
        self.botNameLabel.setText(QCoreApplication.translate("Form", u"\u6a94\u6848\u540d\u7a31", None))
    # retranslateUi

