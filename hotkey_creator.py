import nuke
import os
import re

from PySide2.QtWidgets import QWidget, QCompleter, QApplication
from PySide2.QtCore import QSize
if nuke.NUKE_VERSION_MAJOR == 12:
    from PySide2.QtCore import Qt
elif nuke.NUKE_VERSION_MAJOR >= 13:
    from PySide2.QtGui import Qt

from widgets import creatorWidget

import helper_config
import helper_hotkey_manager as helper
import hotkey_manager_settings as settings


class HotkeyCreatorWidget(QWidget, creatorWidget.Ui_creatorWidget):
    """
    The main Class of Hotkey Manager that helps to create Hotkeys.
    It works with nuke.selectedNodes() as default parameter.
    """
    def __init__(self, parent=None):
        super(HotkeyCreatorWidget, self).__init__(parent, Qt.Window)

        # VARIABLES
        self._not_show_panel_name = "None"

        self.parent = parent
        self.selected = nuke.selectedNodes()

        # SETUP UI
        self.setupUi(self)
        self.setParent(self.parent)
        self.setWindowFlags(Qt.Tool)

        self.setWindowTitle(settings.creator_widget_menu_title)
        self.setFixedSize(QSize(0, 0))
        self.ui_pushButton_delete.hide()

        # CONSTRUCT
        self.construct()

        # CONNECTS
        self.make_connects_for_autofill()
        self.make_connects_for_autofix()
        self.make_connects_for_main_buttons()

    # CONSTRUCT

    def construct(self):
        """
        Fill values, set some settings for widgets
        :return: None
        """
        self.autofill_input_node()
        self.autofill_output_node()
        self.autofill_name()
        self.autofill_show_panel()
        self.autofill_names()

        self.setup_completer()

        self.ui_lineEdit_hotkey.setMaximumWidth(24)
        self.ui_comboBox_names.setMaximumWidth(24)
        self.ui_lineEdit_hotkey.setAlignment(Qt.AlignCenter)

    def setup_completer(self):
        """
        Setup completer for "name" widget. While printing completer show other toolset names
        with the same start
        :return: None
        """
        completer = QCompleter(sorted([file for file in helper.get_list_of_toolsets()]))
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.ui_lineEdit_name.setCompleter(completer)

    # CONNECTS

    def make_connects_for_autofill(self):
        """
        Connects design to make user-widget-fill experience easier
        :return: None
        """
        self.ui_comboBox_input_node.currentIndexChanged.connect(self.autofill_name)
        self.ui_comboBox_input_node.currentIndexChanged.connect(self.autofill_output_node)
        self.ui_comboBox_names.currentIndexChanged.connect(
            lambda: self.ui_lineEdit_name.setText(self.ui_comboBox_names.currentText())
        )

    def make_connects_for_autofix(self):
        """
        Connects design to fix some user inputs
        :return: None
        """
        self.ui_lineEdit_hotkey.textChanged.connect(self.autofix_hotkey)
        self.ui_lineEdit_name.textChanged.connect(self.autofix_name)

    def make_connects_for_main_buttons(self):
        """
        Connects the same as accept or reject
        :return: None
        """
        self.ui_pushButton_create.clicked.connect(self.start_create_hotkey)
        self.ui_pushButton_cancel.clicked.connect(self.close)

    # AUTOFILL

    def autofill_input_node(self):
        """
        Fills toolset input widget with [None + selected nodes classes].
        Find topnode of selection and set it as widget default parameter.
        :return: None
        """
        self.ui_comboBox_input_node.addItem(self._not_show_panel_name)
        i = 1
        for selected_node in self.selected:
            self.ui_comboBox_input_node.addItem(selected_node.name())
            self.ui_comboBox_input_node.setItemData(i, selected_node, 32)
            i += 1

        topnode = self.get_topnode_from_selected()
        index = self.ui_comboBox_input_node.findText(topnode.name(), Qt.MatchFixedString)
        self.ui_comboBox_input_node.setCurrentIndex(index)

    def autofill_output_node(self):
        """
        Fills toolset output widget with [None + selected nodes classes].
        Set default parameter as toolset input widget has.
        :return: None
        """
        self.ui_comboBox_output_node.clear()
        self.ui_comboBox_output_node.addItem(self._not_show_panel_name)
        i = 1
        for selected_node in self.selected:
            self.ui_comboBox_output_node.addItem(selected_node.name())
            self.ui_comboBox_output_node.setItemData(i, selected_node, 32)
            i += 1

        index = self.ui_comboBox_input_node.currentIndex()
        self.ui_comboBox_output_node.setCurrentIndex(index)

    def autofill_name(self):
        """
        Fills toolset name widget with class of toolset input widget node
        :return: None
        """
        if not self.ui_comboBox_input_node.currentText() == self._not_show_panel_name:
            node_class = self.ui_comboBox_input_node.currentData(32).Class()
            node_class_no_digits = ''.join([symbol for symbol in node_class if not symbol.isdigit()])
            self.ui_lineEdit_name.setText(node_class_no_digits)
            self.autofix_name()

    def autofill_names(self):
        """
        Fills toolset names widget with all toolset names
        :return: None
        """
        self.ui_comboBox_names.addItem("")
        self.ui_comboBox_names.addItems(helper.get_list_of_toolsets())

    def autofill_show_panel(self):
        """
        Fills toolset show panel widget with [None + selected nodes classes].
        Set default parameter as None
        :return: None
        """
        self.ui_comboBox_show_panel.addItem(self._not_show_panel_name)
        i = 1
        for selected_node in self.selected:
            self.ui_comboBox_show_panel.addItem(selected_node.name())
            self.ui_comboBox_show_panel.setItemData(i, selected_node, 32)
            i += 1

        self.ui_comboBox_show_panel.setCurrentIndex(0)

    def autofix_hotkey(self):
        """
        Check any user hotkey input. If input is correct - fill only one last symbol to
        toolset hotkey widget
        :return: None
        """
        find_all_letters_or_number = re.findall(r"\w", self.ui_lineEdit_hotkey.text())
        find_all_english = [s for s in find_all_letters_or_number if helper.check_symbol_is_english(s)]
        if find_all_english:
            self.ui_lineEdit_hotkey.setText(find_all_english[-1].lower())
            return
        self.ui_lineEdit_hotkey.setText("")

    def autofix_name(self):
        """
        Check any user toolset name input. If some symbols aren't correct - deletes it
        :return: None
        """
        corrected_text = (re.findall(r"\w", self.ui_lineEdit_name.text()))
        corrected_text = ''.join([s for s in corrected_text if helper.check_symbol_is_english(s)])
        if corrected_text:
            self.ui_lineEdit_name.setText(corrected_text)

    # CREATE HOTKEY

    def start_create_hotkey(self):
        """
        The main method with creating hotkey
        :return: None
        """
        if self.check_before_start_create_hotkey():
            self.set_input_output_show_panel_info_to_nodes()
            self.create_toolset()
            helper.delete_extra_knobs_from_toolset_nodes(self.selected)
            self.write_config_about_toolset()
            helper.add_hotkey_to_menu_by_toolset_name(self.ui_lineEdit_name.text())
            self.close()
            nuke.message(settings.finish_message)

    def set_input_output_show_panel_info_to_nodes(self):
        """
        Set some knobs for selected nodes. When Nuke will create toolset -
        it will understand what node should be input, output and for what
        node need to show panel
        :return: None
        """
        input_node = self.ui_comboBox_input_node.currentData(32)
        input_node.addKnob(nuke.String_Knob("HK_input_node"))

        output_node = self.ui_comboBox_output_node.currentData(32)
        output_node.addKnob(nuke.String_Knob("HK_output_node"))

        show_panel_node = None
        if self.ui_comboBox_show_panel.currentText() != self._not_show_panel_name:
            show_panel_node = self.ui_comboBox_show_panel.currentData(32)
            show_panel_node.addKnob(nuke.String_Knob("HK_show_panel_node"))

        for node in self.selected:
            if node not in [input_node, output_node, show_panel_node]:
                node.addKnob(nuke.String_Knob("HK_other_node"))

    def create_toolset(self):
        """
        Create toolset from selected nodes
        :return: None
        """
        [node.setSelected(False) for node in nuke.allNodes()]
        [node.setSelected(True) for node in self.selected]
        nuke.createToolset(filename=self.ui_lineEdit_name.text(),
                           overwrite=True,
                           rootPath=helper.get_current_path())

        # Delete first three strings in Toolset file, so it won't be connected to version of Nuke
        toolset_path = os.path.join(helper.get_current_path(), "ToolSets", self.ui_lineEdit_name.text() + ".nk")
        lines_without_version = []
        with open(toolset_path, "r") as file:
            for index, line in enumerate(file):
                if index == 1 and "version " in line:
                    continue
                else:
                    lines_without_version.append(line)
        with open(toolset_path, "w") as file:
            for line in lines_without_version:
                file.write(line)

    def write_config_about_toolset(self):
        """
        Write to config file name of created toolset, and it's hotkey
        :return: None
        """
        helper_config.write_config(key=self.ui_lineEdit_name.text(),
                                   conf={"hotkey": self.get_hotkey()})

    # CHECKERS

    def check_before_start_create_hotkey(self):
        """
        The main method to check everything before start creating hotkey
        :return: bool
        """
        if self.check_preset_name_is_not_empty():
            if self.check_hotkey_is_not_empty():
                if not self.check_preset_with_same_name_exists():
                    if not self.check_hotkey_already_exists():
                        if self.check_input_output_is_not_none():
                            if self.ask_if_global_hotkey_already_exists():
                                return True
        return False

    def check_preset_name_is_not_empty(self):
        if self.ui_lineEdit_name.text().replace(" ", "") == "":
            nuke.message("Field 'Preset Name' can't be empty!")
            return False
        return True

    def check_hotkey_is_not_empty(self):
        if self.ui_lineEdit_hotkey.text().replace(" ", "") == "":
            nuke.message("Field 'HotKey' can't be empty!")
            return False
        return True

    def check_preset_with_same_name_exists(self):
        if (self.ui_lineEdit_name.text() + ".nk") in os.listdir(helper.get_toolset_path()):
            nuke.message("Preset with name " + self.ui_lineEdit_name.text() + " already exists!")
            return True
        return False

    def check_hotkey_already_exists(self):
        """
        Check if hotkey from toolsets already exists
        :return: bool
        """
        if os.path.exists(helper_config.get_user_config_path()):
            for toolset_name, dict_of_values in helper_config.read_config().items():
                if self.get_hotkey() == dict_of_values["hotkey"]:
                    nuke.message("Hotkey " + self.get_hotkey() + " already exist in preset " + toolset_name)
                    return True
        return False

    def check_input_output_is_not_none(self):
        if self.ui_comboBox_input_node.currentIndex() == 0 or self.ui_comboBox_output_node.currentIndex() == 0:
            nuke.message("Input or Output can't be " + self._not_show_panel_name)
            return False
        return True

    def ask_if_global_hotkey_already_exists(self):
        """
        Check if hotkey from all panels except toolsets already exists
        :return: bool
        """
        for menu in ("Nodes", "Nuke", "Viewer", "Node Graph"):
            menu = nuke.menu(menu)
            menu_items = helper.get_items_in_menu(menu)
            for menu_item in menu_items:
                hotkey = menu_item.action().shortcut().toString().replace(" ", "").lower()
                self_hotkey = self.get_hotkey().replace(" ", "").lower()
                if hotkey == self_hotkey:
                    if hotkey.lower() not in helper.get_toolsets_hotkeys_list():
                        if nuke.ask("Hotkey " + hotkey + " already used in " + menu_item.name() + "\n\nReplace?"):
                            return True
                        return False
        return True

    # EVENTS

    def closeEvent(self, event):
        """When close - enable Nuke back"""
        self.parent.setEnabled(True)

    # HELPERS

    def get_topnode_from_selected(self):
        """
        Return the topnode from selected nodes using x and y position in NodeGraph
        :return: Node
        """
        if len(self.selected) == 1:
            return self.selected[0]

        node_and_ypos_dict = {}
        for selected_node in self.selected:
            node_and_ypos_dict[selected_node] = selected_node.ypos()

        sorted_node_and_ypos_dict = {k: v for k, v in sorted(node_and_ypos_dict.items(), key=lambda item: item[1])}

        highest_ypos = list(sorted_node_and_ypos_dict.values())[0]

        topnodes = []
        for node, y_position in sorted_node_and_ypos_dict.items():
            if y_position == highest_ypos:
                topnodes.append(node)

        for topnode in topnodes:

            if len(topnodes) == 1:
                return topnodes[0]

            if topnode.Class() in ["Roto", "RotoPaint", "Bezier", "Dot"]:
                topnodes.remove(topnode)

        return topnodes[0]

    def get_hotkey(self):
        """
        Return string representation of hotkey
        :return: str
        """
        hotkey = str()
        if self.ui_checkBox_ctrl_hotkey.isChecked():
            hotkey += "ctrl+"
        if self.ui_checkBox_shift_hotkey.isChecked():
            hotkey += "shift+"
        if self.ui_checkBox_alt_hotkey.isChecked():
            hotkey += "alt+"
        hotkey += self.ui_lineEdit_hotkey.text()

        return hotkey


def check_before_start():
    """
    Check before start create hotkey for selected nodes
    :return: bool
    """
    if not nuke.selectedNodes():
        nuke.message("To create hotkey select at least one node!")
        return False
    if "Viewer" in [node.Class() for node in nuke.selectedNodes()]:
        nuke.message("Viewer can't be in hotkeys!")
        return False
    if any([helper.check_node_is_gizmo_or_contains_gizmo(node) for node in nuke.selectedNodes()]):
        nuke.message("Only Groups supported!\nYou can't add Hotkey for Gizmo or for Group that contains Gizmo!")
        return False
    if helper.check_editor_in_nodegraph():
        nuke.message("Please close " + settings.edit_node_graph_menu_name + " first!")
        return False
    if helper.find_edit_node_graph_action().isChecked():
        nuke.message("Please uncheck " + settings.edit_node_graph_menu_name + " first!")
        return False
    if helper.check_hotkey_manager_creator_is_opened():
        return False
    return True


def start():
    """
    Start create hotkey for selected nodes
    :return: None
    """
    if check_before_start():
        nuke_main_window = helper.get_nuke_main_window()
        nuke_main_window.setEnabled(False)
        creator_widget = HotkeyCreatorWidget(nuke_main_window)
        creator_widget.show()
