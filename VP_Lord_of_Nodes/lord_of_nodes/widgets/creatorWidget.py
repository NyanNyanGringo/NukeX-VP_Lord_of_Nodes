# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'creatorWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_creatorWidget(object):
    def setupUi(self, creatorWidget):
        if not creatorWidget.objectName():
            creatorWidget.setObjectName(u"creatorWidget")
        creatorWidget.resize(276, 169)
        self.verticalLayout_3 = QVBoxLayout(creatorWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabWidget = QTabWidget(creatorWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.verticalLayout = QVBoxLayout(self.tab_setup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(self.tab_setup)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(100, 0))
        self.label_6.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.label_6)

        self.comboBox_input_node = QComboBox(self.tab_setup)
        self.comboBox_input_node.setObjectName(u"comboBox_input_node")

        self.horizontalLayout.addWidget(self.comboBox_input_node)

        self.comboBox_output_node = QComboBox(self.tab_setup)
        self.comboBox_output_node.setObjectName(u"comboBox_output_node")

        self.horizontalLayout.addWidget(self.comboBox_output_node)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(self.tab_setup)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(100, 0))
        self.label_7.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.label_7)

        self.lineEdit_name = QLineEdit(self.tab_setup)
        self.lineEdit_name.setObjectName(u"lineEdit_name")

        self.horizontalLayout_3.addWidget(self.lineEdit_name)

        self.comboBox_names = QComboBox(self.tab_setup)
        self.comboBox_names.setObjectName(u"comboBox_names")
        self.comboBox_names.setEditable(False)

        self.horizontalLayout_3.addWidget(self.comboBox_names)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_ctrl_hotkey = QCheckBox(self.tab_setup)
        self.checkBox_ctrl_hotkey.setObjectName(u"checkBox_ctrl_hotkey")

        self.horizontalLayout_2.addWidget(self.checkBox_ctrl_hotkey)

        self.label = QLabel(self.tab_setup)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.checkBox_shift_hotkey = QCheckBox(self.tab_setup)
        self.checkBox_shift_hotkey.setObjectName(u"checkBox_shift_hotkey")

        self.horizontalLayout_2.addWidget(self.checkBox_shift_hotkey)

        self.label_2 = QLabel(self.tab_setup)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.checkBox_alt_hotkey = QCheckBox(self.tab_setup)
        self.checkBox_alt_hotkey.setObjectName(u"checkBox_alt_hotkey")

        self.horizontalLayout_2.addWidget(self.checkBox_alt_hotkey)

        self.label_3 = QLabel(self.tab_setup)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit_hotkey = QLineEdit(self.tab_setup)
        self.lineEdit_hotkey.setObjectName(u"lineEdit_hotkey")

        self.horizontalLayout_2.addWidget(self.lineEdit_hotkey)

        self.comboBox_hotkeys_hint = QComboBox(self.tab_setup)#EDITED
        self.comboBox_hotkeys_hint.setObjectName(u"comboBox_hotkeys_hint")#EDITED
        self.comboBox_hotkeys_hint.setEditable(False)#EDITED

        self.horizontalLayout_2.addWidget(self.comboBox_hotkeys_hint)#EDITED

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tabWidget.addTab(self.tab_setup, "")
        self.tab_advanced = QWidget()
        self.tab_advanced.setObjectName(u"tab_advanced")
        self.verticalLayout_2 = QVBoxLayout(self.tab_advanced)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(self.tab_advanced)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(100, 0))
        self.label_5.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_4.addWidget(self.label_5)

        self.comboBox_show_panel = QComboBox(self.tab_advanced)
        self.comboBox_show_panel.setObjectName(u"comboBox_show_panel")

        self.horizontalLayout_4.addWidget(self.comboBox_show_panel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.tab_advanced, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_create = QPushButton(creatorWidget)
        self.pushButton_create.setObjectName(u"pushButton_create")

        self.horizontalLayout_5.addWidget(self.pushButton_create)

        self.pushButton_delete = QPushButton(creatorWidget)
        self.pushButton_delete.setObjectName(u"pushButton_delete")

        self.horizontalLayout_5.addWidget(self.pushButton_delete)

        self.pushButton_cancel = QPushButton(creatorWidget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_5.addWidget(self.pushButton_cancel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.retranslateUi(creatorWidget)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(creatorWidget)
    # setupUi

    def retranslateUi(self, creatorWidget):
        creatorWidget.setWindowTitle(QCoreApplication.translate("creatorWidget", u"HotKey Manager Creator", None))
        self.label_6.setText(QCoreApplication.translate("creatorWidget", u"Input/Output:", None))
        self.label_7.setText(QCoreApplication.translate("creatorWidget", u"Preset Name:", None))
        self.checkBox_ctrl_hotkey.setText(QCoreApplication.translate("creatorWidget", u"ctrl", None))
        self.label.setText(QCoreApplication.translate("creatorWidget", u"+", None))
        self.checkBox_shift_hotkey.setText(QCoreApplication.translate("creatorWidget", u"shift", None))
        self.label_2.setText(QCoreApplication.translate("creatorWidget", u"+", None))
        self.checkBox_alt_hotkey.setText(QCoreApplication.translate("creatorWidget", u"alt", None))
        self.label_3.setText(QCoreApplication.translate("creatorWidget", u"+", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_setup), QCoreApplication.translate("creatorWidget", u"Set Up", None))
        self.label_5.setText(QCoreApplication.translate("creatorWidget", u"Show Panel for:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_advanced), QCoreApplication.translate("creatorWidget", u"Advanced", None))
        self.pushButton_create.setText(QCoreApplication.translate("creatorWidget", u"Create", None))
        self.pushButton_delete.setText(QCoreApplication.translate("creatorWidget", u"Delete", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("creatorWidget", u"Cancel", None))
    # retranslateUi

