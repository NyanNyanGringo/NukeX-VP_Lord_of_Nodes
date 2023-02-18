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
        creatorWidget.resize(257, 151)
        self.verticalLayout = QVBoxLayout(creatorWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(creatorWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(100, 0))
        self.label_6.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.label_6)

        self.ui_comboBox_input_node = QComboBox(creatorWidget)
        self.ui_comboBox_input_node.setObjectName(u"ui_comboBox_input_node")

        self.horizontalLayout.addWidget(self.ui_comboBox_input_node)

        self.ui_comboBox_output_node = QComboBox(creatorWidget)
        self.ui_comboBox_output_node.setObjectName(u"ui_comboBox_output_node")

        self.horizontalLayout.addWidget(self.ui_comboBox_output_node)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(creatorWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(100, 0))
        self.label_7.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.label_7)

        self.ui_lineEdit_name = QLineEdit(creatorWidget)
        self.ui_lineEdit_name.setObjectName(u"ui_lineEdit_name")

        self.horizontalLayout_3.addWidget(self.ui_lineEdit_name)

        self.ui_comboBox_names = QComboBox(creatorWidget)
        self.ui_comboBox_names.setObjectName(u"ui_comboBox_names")
        self.ui_comboBox_names.setEditable(False)

        self.horizontalLayout_3.addWidget(self.ui_comboBox_names)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ui_checkBox_ctrl_hotkey = QCheckBox(creatorWidget)
        self.ui_checkBox_ctrl_hotkey.setObjectName(u"ui_checkBox_ctrl_hotkey")

        self.horizontalLayout_2.addWidget(self.ui_checkBox_ctrl_hotkey)

        self.label = QLabel(creatorWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.ui_checkBox_shift_hotkey = QCheckBox(creatorWidget)
        self.ui_checkBox_shift_hotkey.setObjectName(u"ui_checkBox_shift_hotkey")

        self.horizontalLayout_2.addWidget(self.ui_checkBox_shift_hotkey)

        self.label_2 = QLabel(creatorWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.ui_checkBox_alt_hotkey = QCheckBox(creatorWidget)
        self.ui_checkBox_alt_hotkey.setObjectName(u"ui_checkBox_alt_hotkey")

        self.horizontalLayout_2.addWidget(self.ui_checkBox_alt_hotkey)

        self.label_3 = QLabel(creatorWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.ui_lineEdit_hotkey = QLineEdit(creatorWidget)
        self.ui_lineEdit_hotkey.setObjectName(u"ui_lineEdit_hotkey")

        self.horizontalLayout_2.addWidget(self.ui_lineEdit_hotkey)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(creatorWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(100, 0))
        self.label_5.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_6.addWidget(self.label_5)

        self.ui_comboBox_show_panel = QComboBox(creatorWidget)
        self.ui_comboBox_show_panel.setObjectName(u"ui_comboBox_show_panel")

        self.horizontalLayout_6.addWidget(self.ui_comboBox_show_panel)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.ui_pushButton_create = QPushButton(creatorWidget)
        self.ui_pushButton_create.setObjectName(u"ui_pushButton_create")

        self.horizontalLayout_5.addWidget(self.ui_pushButton_create)

        self.ui_pushButton_delete = QPushButton(creatorWidget)
        self.ui_pushButton_delete.setObjectName(u"ui_pushButton_delete")

        self.horizontalLayout_5.addWidget(self.ui_pushButton_delete)

        self.ui_pushButton_cancel = QPushButton(creatorWidget)
        self.ui_pushButton_cancel.setObjectName(u"ui_pushButton_cancel")

        self.horizontalLayout_5.addWidget(self.ui_pushButton_cancel)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(creatorWidget)

        QMetaObject.connectSlotsByName(creatorWidget)
    # setupUi

    def retranslateUi(self, creatorWidget):
        creatorWidget.setWindowTitle(QCoreApplication.translate("creatorWidget", u"HotKey Manager Creator", None))
        self.label_6.setText(QCoreApplication.translate("creatorWidget", u"Input/Output:", None))
        self.label_7.setText(QCoreApplication.translate("creatorWidget", u"Preset Name:", None))
        self.ui_checkBox_ctrl_hotkey.setText(QCoreApplication.translate("creatorWidget", u"ctrl", None))
        self.label.setText(QCoreApplication.translate("creatorWidget", u"+", None))
        self.ui_checkBox_shift_hotkey.setText(QCoreApplication.translate("creatorWidget", u"shift", None))
        self.label_2.setText(QCoreApplication.translate("creatorWidget", u"+", None))
        self.ui_checkBox_alt_hotkey.setText(QCoreApplication.translate("creatorWidget", u"alt", None))
        self.label_3.setText(QCoreApplication.translate("creatorWidget", u"+", None))
        self.label_5.setText(QCoreApplication.translate("creatorWidget", u"Show Panel for:", None))
        self.ui_pushButton_create.setText(QCoreApplication.translate("creatorWidget", u"Create", None))
        self.ui_pushButton_delete.setText(QCoreApplication.translate("creatorWidget", u"Delete", None))
        self.ui_pushButton_cancel.setText(QCoreApplication.translate("creatorWidget", u"Cancel", None))
    # retranslateUi

