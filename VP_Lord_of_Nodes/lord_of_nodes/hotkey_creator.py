import nuke
import os
import re
import string  # EDITED

from PySide2.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QCompleter
from PySide2.QtCore import QSize

if nuke.NUKE_VERSION_MAJOR == 12:
    from PySide2.QtCore import Qt
elif nuke.NUKE_VERSION_MAJOR >= 13:
    from PySide2.QtGui import Qt

from lord_of_nodes.widgets import creatorWidget
from lord_of_nodes.helpers import toolsetsHelper, stringHelper, nukeHelper, hotkeysHelper, osHelper, configHelper, \
    qtHelper
from lord_of_nodes.helpers.CustomWidgets.custom_pulldown_choice import CustomPulldownChoice
import lord_of_nodes.hotkey_manager_settings as settings


class HotkeyCreatorWidget(QWidget):
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
        self.ui = creatorWidget.Ui_creatorWidget()
        self.ui.setupUi(self)

        self.add_custom_widgets()
        self.add_tooltips()
        self.setParent(self.parent)
        self.setWindowFlags(Qt.Tool)
        self.setWindowTitle(settings.creator_widget_menu_title)
        self.setFixedSize(QSize(0, 0))

        self.ui.tabWidget.setCurrentIndex(0)

        self.ui.pushButton_delete.hide()
        self.ui.label_5.hide()  # hide show_panel label
        self.ui.comboBox_show_panel.hide()

        # CONSTRUCT
        self.construct()

        # CONNECTS
        self.make_connects_for_autofill()
        self.make_connects_for_autofix()
        self.make_connects_for_main_buttons()

    # SETUP UI

    def add_custom_widgets(self):
        self.ui_show_panel = CustomPulldownChoice(self, "Show Panel for:")
        self.ui.tab_advanced.layout().addWidget(self.ui_show_panel)

        self.ui_context_sensitive = CustomPulldownChoice(self, "Context-Sensitive for:")
        self.ui.tab_advanced.layout().addWidget(self.ui_context_sensitive)

        self.ui_knob_default = CustomPulldownChoice(self, "Knob Default for:")
        self.ui.tab_advanced.layout().addWidget(self.ui_knob_default)

        self.ui.tab_advanced.layout().addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def add_tooltips(self):
        self.ui.comboBox_input_node.setToolTip(
            stringHelper.auto_enter("When you trigger Hotkey, input of given node will be connected to selection."))

        self.ui.comboBox_output_node.setToolTip(
            stringHelper.auto_enter("When you trigger Hotkey, output of given node will be connected to branch."))

        self.ui.lineEdit_name.setToolTip(
            stringHelper.auto_enter("Name of preset should be unique - you can't create presets with "
                                    "the same name. Recommended to use names of nodes in preset name. "
                                    "For example, if you have Blur and Roto nodes, preset might be called "
                                    "as 'BlurRoto'"))

        for knob in [self.ui.checkBox_ctrl_hotkey, self.ui.checkBox_shift_hotkey, self.ui.checkBox_alt_hotkey,
                     self.ui.lineEdit_hotkey]:
            knob.setToolTip("Hotkeys to create preset.")

        self.ui_show_panel.setToolTip(
            stringHelper.auto_enter("Responsible for which nodes Contol Panel will be shown."))

        self.ui_context_sensitive.setToolTip(
            "Responsible for which nodes will be applied context-sensitive knob values.\n\n"
            "For example, node Transform has 'center' knob. Value of this knob depends\n"
            "on context. If we create Transform out of branch - 'center' knob takes\n"
            "as value width/height of Root format. Else, if we create Transform inside\n"
            "branch - 'center' knob takes as value width/height of input nodes.\n\n"
            "In this version of program next context-sensitive nodes supported:\n"
            "" + stringHelper.auto_enter(" ".join(hotkeysHelper.get_supported_context_sensitive_knobs()))
        )

        self.ui_knob_default.setToolTip(
            stringHelper.auto_enter("Hotkeys works in ToolSet engine - it means every time you trigger Hotkey, "
                                    "Nuke create ToolSet. All knob values inside ToolSet remain "
                                    "the same. If you want to use Knob Default values (that you made using appropriate "
                                    "functional of Lord of Nodes) - you can point out it here."))

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
        self.autofill_hotkeys_hint()  # EDITED
        self.autofill_hotkeys()  # при открытии будет сразу предлагать новый хоткей
        self.autofill_context_sensitive()
        self.autofill_knob_default()

        self.setup_completer()

        self.ui.lineEdit_hotkey.setMaximumWidth(24)
        self.ui.comboBox_names.setMaximumWidth(24)
        self.ui.comboBox_hotkeys_hint.setMaximumWidth(24)  # EDITED
        self.ui.lineEdit_hotkey.setAlignment(Qt.AlignCenter)

    def setup_completer(self):
        """
        Setup completer for "name" widget. While printing completer show other toolset names
        with the same start
        :return: None
        """
        completer = QCompleter(sorted([file for file in toolsetsHelper.get_list_of_toolsets()]))
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.ui.lineEdit_name.setCompleter(completer)

    # CONNECTS

    def make_connects_for_autofill(self):
        """
        Connects design to make user-widget-fill experience easier
        :return: None
        """
        self.ui.comboBox_input_node.currentIndexChanged.connect(self.autofill_name)
        self.ui.comboBox_input_node.currentIndexChanged.connect(self.autofill_output_node)
        self.ui.comboBox_names.currentIndexChanged.connect(
            lambda: self.ui.lineEdit_name.setText(self.ui.comboBox_names.currentText())
        )
        self.ui.comboBox_hotkeys_hint.currentIndexChanged.connect(self.autofill_hotkeys)  # EDITED

    def make_connects_for_autofix(self):
        """
        Connects design to fix some user inputs
        :return: None
        """
        self.ui.lineEdit_hotkey.textChanged.connect(self.autofix_hotkey)
        self.ui.lineEdit_name.textChanged.connect(self.autofix_name)

    def make_connects_for_main_buttons(self):
        """
        Connects the same as accept or reject
        :return: None
        """
        self.ui.pushButton_create.clicked.connect(self.start_create_hotkey)
        self.ui.pushButton_cancel.clicked.connect(self.close)

    # AUTOFILL

    def autofill_input_node(self):
        """
        Fills toolset input widget with [None + selected nodes classes].
        Find topnode of selection and set it as widget default parameter.
        :return: None
        """
        self.ui.comboBox_input_node.addItem(self._not_show_panel_name)
        i = 1
        for selected_node in self.selected:
            self.ui.comboBox_input_node.addItem(selected_node.name())
            self.ui.comboBox_input_node.setItemData(i, selected_node, 32)
            self.ui.comboBox_input_node.setItemData(Qt.Unchecked | Qt.ItemIsUserCheckable, Qt.CheckStateRole)
            i += 1

        topnode = self.get_topnode_from_selected()
        index = self.ui.comboBox_input_node.findText(topnode.name(), Qt.MatchFixedString)
        self.ui.comboBox_input_node.setCurrentIndex(index)

    def autofill_output_node(self):
        """
        Fills toolset output widget with [None + selected nodes classes].
        Set default parameter as toolset input widget has.
        :return: None
        """
        self.ui.comboBox_output_node.clear()
        self.ui.comboBox_output_node.addItem(self._not_show_panel_name)
        i = 1
        for selected_node in self.selected:
            self.ui.comboBox_output_node.addItem(selected_node.name())
            self.ui.comboBox_output_node.setItemData(i, selected_node, 32)
            i += 1

        index = self.ui.comboBox_input_node.currentIndex()
        self.ui.comboBox_output_node.setCurrentIndex(index)

    def autofill_name(self):
        """
        Fills toolset name widget with class of toolset input widget node
        :return: None
        """
        if not self.ui.comboBox_input_node.currentText() == self._not_show_panel_name:
            node_class = self.ui.comboBox_input_node.currentData(32).Class()
            node_class_no_digits = ''.join([symbol for symbol in node_class if not symbol.isdigit()])
            self.ui.lineEdit_name.setText(node_class_no_digits)
            self.autofix_name()

    def autofill_names(self):
        """
        Fills toolset names widget with all toolset names
        :return: None
        """
        self.ui.comboBox_names.addItem("")
        self.ui.comboBox_names.addItems(toolsetsHelper.get_list_of_toolsets())

    def autofill_hotkeys(self):  # EDITED
        hotkey = self.ui.comboBox_hotkeys_hint.currentText()
        self.ui.checkBox_ctrl_hotkey.setChecked('ctrl' in hotkey)
        self.ui.checkBox_shift_hotkey.setChecked('shift' in hotkey)
        self.ui.checkBox_alt_hotkey.setChecked('alt' in hotkey)
        self.ui.lineEdit_hotkey.setText(hotkey[-1])

    def autofill_hotkeys_hint(self):  # EDITED
        hotkey_prefix_order = ['', 'ctrl', 'alt', 'shift', 'ctrl+shift', 'ctrl+alt', 'alt+shift', 'ctrl+alt+shift']

        # возвращает все доступные в нюке хоткеи, логика взята из ask_if_global_hotkey_already_exists
        def get_all_global_hotkeys():
            all_hotkeys_list = []
            for menu in ("Nodes", "Nuke", "Viewer", "Node Graph"):
                menu = nuke.menu(menu)
                menu_items = qtHelper.get_items_in_menu(menu)
                for menu_item in menu_items:
                    hotkey = menu_item.action().shortcut().toString().replace(" ", "").lower()
                    if hotkey != '':
                        all_hotkeys_list.append(hotkey)
            return all_hotkeys_list

        # возвращает список из первых букв имен выбранных нод, нужно чтобы первыми выводить шорткаты содержащие первые буквы выбранных нод
        def get_first_letters_list(nodes):
            letters = []
            for node in nodes:
                if node.name():
                    letter = node.name()[0].lower()
                    if letter.isalpha() and letter not in letters:
                        letters.append(letter)
            return letters

        available_hotkeys_list = []  # запишем сюда доступные хоткеи
        reserved_hotkeys = get_all_global_hotkeys() + toolsetsHelper.get_toolsets_hotkeys_list()  # создаем список из уже занятых хоткеев нюком и lord of nodes
        first_letters_list = get_first_letters_list(
            self.selected)  # попытаемся составить хоткей из первых букв выбранных нод
        all_letters = list(string.ascii_lowercase)  # все буквы английского алфавита
        for letter in first_letters_list:  # удаляем буквы first_letters_list из all_letters, чтоюы поставить их в начало списка
            all_letters.remove(
                letter)  # get_first_letters_list обеспечивает, что элементы не повторяются и что они буквы и есть в all_letters
        for prefix in hotkey_prefix_order:  # сначала составляем список для первых букв выбранных нод
            for letter in first_letters_list:
                hotkey = f'{prefix}+{letter}'.lstrip('+')
                if hotkey not in reserved_hotkeys:
                    available_hotkeys_list.append(hotkey)
        for prefix in hotkey_prefix_order:  # потом составляем список для остальных букв
            for letter in all_letters:
                hotkey = f'{prefix}+{letter}'.lstrip('+')
                if hotkey not in reserved_hotkeys:
                    available_hotkeys_list.append(hotkey)
        if available_hotkeys_list:
            self.ui.comboBox_hotkeys_hint.addItems(available_hotkeys_list)

    def autofill_show_panel(self):
        """
        Fills toolset show panel widget with [None + selected nodes names].
        Set default parameter as None
        :return: None
        """
        for selected_node in self.selected:
            item = self.ui_show_panel.addItem(selected_node.name())
            self.ui_show_panel.setItemData(item, selected_node)

    def autofill_context_sensitive(self):
        """
        Fills toolset context-sensitive widget with selected nodes names.
        :return: None
        """

        for selected_node in self.selected:
            if hotkeysHelper.check_node_has_context_sensitive_knobs(selected_node):
                item = self.ui_context_sensitive.addItem(selected_node.name())
                item.setChecked(True)
                self.ui_context_sensitive.setItemData(item, selected_node)

    def autofill_knob_default(self):
        for selected_node in self.selected:
            item = self.ui_knob_default.addItem(selected_node.name())
            self.ui_knob_default.setItemData(item, selected_node)

    def autofix_hotkey(self):
        """
        Check any user hotkey input. If input is correct - fill only one last symbol to
        toolset hotkey widget
        :return: None
        """
        find_all_letters_or_number = re.findall(r"\w", self.ui.lineEdit_hotkey.text())
        find_all_english = [s for s in find_all_letters_or_number if stringHelper.check_symbol_is_english(s)]
        if find_all_english:
            self.ui.lineEdit_hotkey.setText(find_all_english[-1].lower())
            return
        self.ui.lineEdit_hotkey.setText("")

    def autofix_name(self):
        """
        Check any user toolset name input. If some symbols aren't correct - deletes it
        :return: None
        """
        corrected_text = (re.findall(r"\w", self.ui.lineEdit_name.text()))
        corrected_text = ''.join([s for s in corrected_text if stringHelper.check_symbol_is_english(s)])
        if corrected_text:
            self.ui.lineEdit_name.setText(corrected_text)

    # CREATE HOTKEY

    def start_create_hotkey(self):
        """
        The main method with creating hotkey
        :return: None
        """
        if self.check_before_start_create_hotkey():
            self.set_extra_knobs_to_nodes()
            self.create_toolset()
            hotkeysHelper.get_nodes_by_extra_knobs_and_delete_extra_knobs(self.selected)
            self.write_config_about_toolset()
            hotkeysHelper.add_hotkey_to_menu_by_toolset_name(self.ui.lineEdit_name.text())
            self.close()
            nuke.message(settings.finish_message)

    def set_extra_knobs_to_nodes(self):
        """
        Set some extra knobs for selected nodes. When Nuke will create toolset -
        it will understand what node should be input, output and for what
        node need to show panel
        :return: None
        """
        input_node = self.ui.comboBox_input_node.currentData(32)
        input_node.addKnob(nuke.String_Knob("HK_input_node"))

        output_node = self.ui.comboBox_output_node.currentData(32)
        output_node.addKnob(nuke.String_Knob("HK_output_node"))

        show_panel_nodes = []
        for item in self.ui_show_panel.items(only_checked=True):
            node = self.ui_show_panel.getItemData(item)
            node.addKnob(nuke.String_Knob("HK_show_panel_node"))
            show_panel_nodes.append(node)

        context_sensetive_nodes = []
        for item in self.ui_context_sensitive.items(only_checked=True):
            node = self.ui_context_sensitive.getItemData(item)
            node.addKnob(nuke.String_Knob("HK_context_sensitive"))
            context_sensetive_nodes.append(node)

        knob_default_nodes = []
        for item in self.ui_knob_default.items(only_checked=True):
            node = self.ui_knob_default.getItemData(item)
            node.addKnob(nuke.String_Knob("HK_knob_default"))
            knob_default_nodes.append(node)

        for node in self.selected:
            if node not in [input_node, output_node] + show_panel_nodes + context_sensetive_nodes + knob_default_nodes:
                node.addKnob(nuke.String_Knob("HK_other_node"))

    def create_toolset(self):
        """
        Create toolset from selected nodes
        :return: None
        """
        [node.setSelected(False) for node in nuke.allNodes()]
        [node.setSelected(True) for node in self.selected]
        nuke.createToolset(filename=self.ui.lineEdit_name.text(),
                           overwrite=True,
                           rootPath=osHelper.get_config_path())

        # Delete first three strings in Toolset file, so it won't be connected to version of Nuke
        toolset_path = osHelper.get_toolset_path(toolset_name=self.ui.lineEdit_name.text())
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
        configHelper.write_config(key=self.ui.lineEdit_name.text(),
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
        if self.ui.lineEdit_name.text().replace(" ", "") == "":
            nuke.message("Field 'Preset Name' can't be empty!")
            return False
        return True

    def check_hotkey_is_not_empty(self):
        if self.ui.lineEdit_hotkey.text().replace(" ", "") == "":
            nuke.message("Field 'HotKey' can't be empty!")
            return False
        return True

    def check_preset_with_same_name_exists(self):
        if (self.ui.lineEdit_name.text() + ".nk") in os.listdir(osHelper.get_toolset_path()):
            nuke.message("Preset with name " + self.ui.lineEdit_name.text() + " already exists!")
            return True
        return False

    def check_hotkey_already_exists(self):
        """
        Check if hotkey from toolsets already exists
        :return: bool
        """
        if os.path.exists(configHelper.get_user_config_path()):
            for toolset_name, dict_of_values in configHelper.read_config().items():
                if self.get_hotkey() == dict_of_values["hotkey"]:
                    nuke.message("Hotkey " + self.get_hotkey() + " already exist in preset " + toolset_name)
                    return True
        return False

    def check_input_output_is_not_none(self):
        if self.ui.comboBox_input_node.currentIndex() == 0 or self.ui.comboBox_output_node.currentIndex() == 0:
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
            menu_items = qtHelper.get_items_in_menu(menu)
            for menu_item in menu_items:
                hotkey = menu_item.action().shortcut().toString().replace(" ", "").lower()
                self_hotkey = self.get_hotkey().replace(" ", "").lower()
                if hotkey == self_hotkey:
                    if hotkey.lower() not in toolsetsHelper.get_toolsets_hotkeys_list():
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
        if self.ui.checkBox_ctrl_hotkey.isChecked():
            hotkey += "ctrl+"
        if self.ui.checkBox_shift_hotkey.isChecked():
            hotkey += "shift+"
        if self.ui.checkBox_alt_hotkey.isChecked():
            hotkey += "alt+"
        hotkey += self.ui.lineEdit_hotkey.text()

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
    if "BackdropNode" in [node.Class() for node in nuke.selectedNodes()]:
        nuke.message("I'm sorry, BackdropNode can't be in hotkeys!")
        return False
    if any([nukeHelper.check_node_is_gizmo_or_contains_gizmo(node) for node in nuke.selectedNodes()]):
        nuke.message("Only Groups supported!\nYou can't add Hotkey for Gizmo or for Group that contains Gizmo!")
        return False
    if nukeHelper.check_editor_in_nodegraph():
        nuke.message("Please close " + settings.edit_node_graph_menu_name + " first!")
        return False
    if qtHelper.find_edit_node_graph_action().isChecked():
        nuke.message("Please uncheck " + settings.edit_node_graph_menu_name + " first!")
        return False
    if qtHelper.check_hotkey_manager_creator_is_opened():
        return False
    return True


def start():
    """
    Start create hotkey for selected nodes
    :return: None
    """
    if check_before_start():
        nuke_main_window = qtHelper.get_nuke_main_window()
        nuke_main_window.setEnabled(False)
        creator_widget = HotkeyCreatorWidget(nuke_main_window)
        creator_widget.show()
