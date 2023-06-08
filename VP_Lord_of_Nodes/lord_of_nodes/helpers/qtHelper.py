import nuke

from PySide2.QtWidgets import QApplication, QComboBox
from PySide2.QtCore import Qt

import lord_of_nodes.hotkey_manager_settings as settings


def get_nuke_main_window():
    """
    :return: Nuke main window
    """
    widget = QApplication.instance().activeWindow()
    if widget:
        return widget
    raise Exception("Can't find NukeStudio PySide2.QtWidgets.QMainWindow")


def get_node_graph_widget():
    """
    Return Node Graph widget. Doesn't matter
    if it is active or not.
    """
    import hiero.ui
    for widget in hiero.ui.windowManager().windows():
        if widget.windowTitle() == "Node Graph":
            if widget.metaObject().className() == "Foundry::UI::LinkedView":
                return widget
    raise Exception("Can't find nodegraph!")


def check_node_graph_is_visible_and_not_hidden():
    node_graph_widget = get_node_graph_widget()
    if node_graph_widget.isVisible() and not node_graph_widget.isHidden():
        return True
    return False


def check_hotkey_manager_creator_is_opened():
    for widget in QApplication.allWidgets():
        if widget.windowTitle() == settings.creator_widget_menu_title:
            if widget.isVisible():
                return True
    return False


def set_mouse_tracking_in_nodegraph(value=True):
    """
    After selecting node-buttons in NodeGraph and close
    Creator Widget selection remains. So node-buttons
    calls again. To avoid it we turn off mouse tracking
    in NodeGraph
    :param value: bool
    :return: bool
    """
    node_graph_widget = get_node_graph_widget()
    if node_graph_widget:
        for child in node_graph_widget.children():
            if hasattr(child.__class__, "setMouseTracking"):
                child.setMouseTracking(value)
                return True
    raise Exception("Can't find child to set Mouse Tracking")


def get_items_in_menu(menu):
    """
    Return all items that menu contains (recursively)
    :param menu: QMenu
    :return: list
    """
    items = []
    for item in menu.items():
        if item.__class__.__name__ == "Menu":
            items += get_items_in_menu(item)
        else:
            items.append(item)
    return items


def find_item_in_menu(name, menu):
    """
    Recursively search for item with given name in menu
    :param name: str
    :param menu: QMenu
    :return: QMenu or QMenuItem
    """
    for item in menu.items():
        if item.name() == name:
            return item
        if item.__class__.__name__ == "Menu":
            item_found = find_item_in_menu(name, item)
            if item_found:
                return item_found


def find_edit_node_graph_action():
    """
    Finding in Nuke Menu "Edit Menu" action
    :return: QAction
    """
    return find_item_in_menu(name=settings.edit_node_graph_menu_name, menu=nuke.menu("Nuke")).action()


class CheckableComboBox(QComboBox):
    """
    Copy from: https://learndataanalysis.org/how-to-create-checkable-combobox-widget-pyqt5-tutorial/
    """
    def __init__(self):
        super().__init__()
        self._changed = False

        self.view().pressed.connect(self.handleItemPressed)

    def setItemChecked(self, index, checked=False):
        item = self.model().item(index, self.modelColumn())  # QStandardItem object

        if checked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)

        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self._changed = True

    def hidePopup(self):
        if not self._changed:
            super().hidePopup()
        self._changed = False

    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == Qt.Checked
