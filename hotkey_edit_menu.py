import nuke
import os


from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QTableView, QTableWidgetItem, QMenu,\
    QAction
from PySide2.QtGui import QCursor
if nuke.NUKE_VERSION_MAJOR == 12:
    from PySide2.QtCore import Qt
elif nuke.NUKE_VERSION_MAJOR >= 13:
    from PySide2.QtGui import Qt

import helper_config
import helper_hotkey_manager as helper
import hotkey_manager_settings as settings

import hotkey_creator


class HotkeyEditWidget(hotkey_creator.HotkeyCreatorWidget):
    """
    Modified instance of HotkeyCreatorWidget used to edit exists toolsets
    """
    def __init__(self, parent=None, hotkey_edit_widget=None):
        super(HotkeyEditWidget, self).__init__(parent)

        # VARIABLES
        self.parent = parent
        self.hotkey_edit_widget = hotkey_edit_widget
        self.table = self.hotkey_edit_widget.ui_tableWidget

        self.toolset_name = self.table.selectedItems()[0].text()
        self.toolset_hotkey = self.table.selectedItems()[1].text()
        self.input_node, self.output_node, self.show_panel_node = helper.find_input_output_show_panel_nodes(self.selected)

        # SETUP UI
        self.ui_pushButton_create.setText("Save")

        # CONSTRUCT
        self.construct_if_table()

        # CONNECTS
        self.disconnect_autofill_if_table()
        self.make_connects_for_main_buttons_if_table()

    # CONSTRUCT

    def construct_if_table(self):
        """
        Fill values, set some settings for widgets
        :return: None
        """
        self.autofill_input_node_if_table()
        self.autofill_output_node_if_table()
        self.autofill_name_if_table()
        self.autofill_hotkey_if_table()
        self.autofill_show_panel_if_table()

    # AUTOFILL

    def autofill_input_node_if_table(self):
        """
        Fills toolset input widget with [None + selected nodes classes].
        Find toolset input node and set it as widget default parameter.
        :return: None
        """
        index = self.ui_comboBox_input_node.findText(self.input_node.name(), Qt.MatchFixedString)
        self.ui_comboBox_input_node.setCurrentIndex(index)

    def autofill_output_node_if_table(self):
        """
        Fills toolset output widget with [None + selected nodes classes].
        Find toolset output node and set it as widget default parameter.
        :return: None
        """
        index = self.ui_comboBox_output_node.findText(self.output_node.name(), Qt.MatchFixedString)
        self.ui_comboBox_output_node.setCurrentIndex(index)

    def autofill_name_if_table(self):
        """
        Fills toolset name widget with toolset name
        :return: None
        """
        self.ui_lineEdit_name.setText(self.toolset_name)

    def autofill_hotkey_if_table(self):
        """
        Fill hotkey widgets with toolset hotkey
        :return: None
        """
        if "ctrl" in self.toolset_hotkey:
            self.ui_checkBox_ctrl_hotkey.setChecked(True)
        if "shift" in self.toolset_hotkey:
            self.ui_checkBox_shift_hotkey.setChecked(True)
        if "alt" in self.toolset_hotkey:
            self.ui_checkBox_alt_hotkey.setChecked(True)
        self.ui_lineEdit_hotkey.setText(self.toolset_hotkey[-1])

    def autofill_show_panel_if_table(self):
        """
        Fill show panel widget if toolset has show panel node
        :return: None
        """
        if self.show_panel_node:
            index = self.ui_comboBox_show_panel.findText(self.show_panel_node.name(), Qt.MatchFixedString)
            self.ui_comboBox_show_panel.setCurrentIndex(index)

    # CONNECTS

    def disconnect_autofill_if_table(self):
        self.ui_comboBox_input_node.currentIndexChanged.disconnect()

    def make_connects_for_main_buttons_if_table(self):
        self.ui_pushButton_create.clicked.disconnect()
        self.ui_pushButton_create.clicked.connect(self.start_save_settings)

    # SAVE SETTINGS

    def start_save_settings(self):
        """
        Start save settings to tooltip
        :return: None
        """
        if self.check_before_start_save_settings_if_table():
            helper.delete_toolset_by_name(self.toolset_name)
            self.set_input_output_show_panel_info_to_nodes()
            self.create_toolset()
            self.write_config_about_toolset()
            helper.add_hotkey_to_menu_by_toolset_name(self.ui_lineEdit_name.text())
            self.hotkey_edit_widget.fill_table()
            self.close()
            nuke.message(settings.finish_message)

    # CHECKERS

    def check_before_start_save_settings_if_table(self):
        if self.check_preset_name_is_not_empty():
            if self.check_hotkey_is_not_empty():
                if not self.check_preset_with_same_name_exists_if_table():
                    if not self.check_hotkey_already_exists_if_table():
                        if self.check_input_output_is_not_none():
                            if self.ask_if_global_hotkey_already_exists():
                                return True

    def check_preset_with_same_name_exists_if_table(self):
        if not self.toolset_name == self.ui_lineEdit_name.text():
            if (self.ui_lineEdit_name.text() + ".nk") in os.listdir(helper.get_toolset_path()):
                nuke.message("Preset with name " + self.ui_lineEdit_name.text() + " already exists!")
                return True
        return False

    def check_hotkey_already_exists_if_table(self):
        if os.path.exists(helper_config.get_user_config_path()):
            for toolset_name, dict_of_values in helper_config.read_config().items():
                if self.get_hotkey() == dict_of_values["hotkey"] and self.get_hotkey() != self.toolset_hotkey:
                    nuke.message("Hotkey " + self.get_hotkey() + " already exist in preset " + toolset_name)
                    return True
            return False
        else:
            nuke.message("No config in path: " + helper_config.get_user_config_path())
            return False

    # HELPERS

    # REGENERATE ACCEPT / REGECT

    def closeEvent(self, event):
        self.delete_toolset_nodes()
        self.hotkey_edit_widget.setEnabled(True)

    def delete_toolset_nodes(self):
        for toolset_node in self.selected:
            if toolset_node:
                nuke.delete(toolset_node)


class HotkeyEditMenuWidget(QWidget):
    """
    QWidget of Edit Hotkeys Menu. Shows all toolsets, and it's hotkeys.
    Has functions to delete or edit toolsets
    """
    def __init__(self, parent=None):
        super(HotkeyEditMenuWidget, self).__init__(parent, Qt.Window)

        # VARIABLES
        self.parent = parent

        # SETUP UI
        self.setupUi()
        self.setParent(self.parent)
        self.setWindowFlags(Qt.Tool)

        # CONSTRUCT
        self.construct()

    # CONSTRUCT

    def setupUi(self):
        self.setWindowTitle(u"HotKey Manager Edit Menu")

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.ui_tableWidget = QTableWidget()
        self.layout.addWidget(self.ui_tableWidget)

    def construct(self):
        """
        Fill values, set some settings for widgets
        :return: None
        """
        self.set_table_settings()
        self.fill_table()

    # TABLE

    def set_table_settings(self):
        """
        Set settings for table with toolsets
        :return: None
        """
        self.ui_tableWidget.setColumnCount(2)
        self.ui_tableWidget.verticalHeader().hide()
        self.ui_tableWidget.setHorizontalHeaderLabels(["Present Name:", "HotKey"])
        self.ui_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.ui_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui_tableWidget.setShowGrid(False)
        self.ui_tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui_tableWidget.customContextMenuRequested.connect(self.table_context_menu)
        self.ui_tableWidget.setSelectionBehavior(QTableView.SelectRows)

    def fill_table(self):
        """
        Fill table with toolsets and hotkeys
        :return: None
        """
        self.ui_tableWidget.sortItems(0, Qt.AscendingOrder)

        selected_items_text = [item.text() for item in self.ui_tableWidget.selectedItems() if item.column() == 0]

        self.ui_tableWidget.clearContents()
        self.ui_tableWidget.setRowCount(0)

        for toolset_name, dict_of_values in helper_config.read_config().items():
            self.ui_tableWidget.setRowCount(self.ui_tableWidget.rowCount() + 1)

            item = QTableWidgetItem()
            item.setData(Qt.EditRole, toolset_name)
            item.setToolTip(helper.get_string_of_all_nodes_of_toolset(toolset_name))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.ui_tableWidget.setItem(self.ui_tableWidget.rowCount() - 1, 0, item)

            item = QTableWidgetItem()
            item.setData(Qt.EditRole, dict_of_values["hotkey"])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setTextAlignment(Qt.AlignCenter)
            self.ui_tableWidget.setItem(self.ui_tableWidget.rowCount() - 1, 1, item)

        for selected_item_text in selected_items_text:
            for item in self.ui_tableWidget.findItems(selected_item_text, Qt.MatchExactly):
                item_row = item.row()
                for column in range(0, self.ui_tableWidget.columnCount()):
                    self.ui_tableWidget.item(item_row, column).setSelected(True)

        self.ui_tableWidget.sortItems(0, Qt.AscendingOrder)
        self.ui_tableWidget.resizeColumnsToContents()

    def table_context_menu(self):
        """
        Setup table context menu
        :return: None
        """
        menu = QMenu(parent=self)

        edit_action = QAction("Edit", parent=self)
        delete_action = QAction("Delete", parent=self)

        menu.addAction(edit_action)
        menu.addAction(delete_action)

        if self.ui_tableWidget.selectedItems():
            action = menu.exec_(QCursor.pos())
            if action == edit_action:
                self.start_edit_action()
            elif action == delete_action:
                self.start_delete_action()

    def start_edit_action(self):
        """
        Open instance of HotkeyCreatorWidget to Edit already existing toolset (hotkey)
        :return:
        """
        if len(self.ui_tableWidget.selectedItems()) == self.ui_tableWidget.columnCount():
            if not helper.check_hotkey_manager_creator_is_opened():
                nuke_main_window = helper.get_nuke_main_window()
                self.setEnabled(False)
                self.create_toolset_nodes_and_select_it()
                edit_widget = HotkeyEditWidget(nuke_main_window, self)
                edit_widget.show()
        else:
            nuke.message("Please select only one item!")

    def start_delete_action(self):
        """
        Delete selected toolsets
        :return: bool
        """
        to_delete = []
        for item in self.ui_tableWidget.selectedItems():
            if item.column() == 0:
                to_delete.append(item.text())

        if nuke.ask("Are you sure - you want to delete " + str(len(to_delete)) + " presets?"):
            [helper.delete_toolset_by_name(toolset) for toolset in to_delete]
            self.fill_table()
            return True
        return False

    # EVENTS

    def closeEvent(self, event):
        # Enable NukeX
        self.parent.setEnabled(True)

    # HELPERS

    def create_toolset_nodes_and_select_it(self):
        """
        Disalect all nodes, create toolset and select these nodes
        :return: None
        """
        toolset_name = self.ui_tableWidget.selectedItems()[0].text()
        toolset_path = os.path.join(helper.get_toolset_path(), toolset_name + ".nk").replace("\\", "/")

        if not os.path.exists(toolset_path):
            raise Exception("No toolset found with name: " + self.toolset_name)

        all_nodes = nuke.allNodes()

        [node.setSelected(False) for node in all_nodes]

        nuke.loadToolset(toolset_path)
        toolset_nodes = [node for node in nuke.allNodes() if node not in all_nodes]

        [node.setSelected(True) for node in all_nodes if node in toolset_nodes]


def check_before_start():
    """
    Check before start opening Edit Hotkeys Menu
    :return: bool
    """
    if helper.check_editor_in_nodegraph():
        nuke.message("Please close" + settings.edit_node_graph_menu_name + " first!")
        return False
    if helper.find_edit_node_graph_action().isChecked():
        nuke.message("Please uncheck " + settings.edit_node_graph_menu_name + " first!")
        return False
    if not helper.get_list_of_toolsets():
        nuke.message("No Hotkeys exists!")
        return False
    return True


def start():
    """
    Start opening Edit Hotkeys Menu
    :return: None
    """
    if check_before_start():
        nuke_main_window = helper.get_nuke_main_window()
        nuke_main_window.setEnabled(False)
        creator_widget = HotkeyEditMenuWidget(nuke_main_window)
        creator_widget.show()
