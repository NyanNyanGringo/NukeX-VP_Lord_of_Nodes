from PySide2.QtWidgets import *
from PySide2.QtCore import *

from lord_of_nodes.helpers import qtHelper


class CustomQMenu(QMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseReleaseEvent(self, event):
        action = self.activeAction()
        if action and action.isEnabled():
            if not action.menu():
                action.trigger()
            else:
                action.menu().exec_(self.mapToGlobal(event.pos()))
        else:
            super().mouseReleaseEvent(event)


class CustomPulldownChoice(QWidget):
    def __init__(self, parent,
                 label_text: str,
                 button_tooltip: str = None):
        super().__init__(parent)

        # variables
        self.parent = parent
        self._label_text = label_text
        self._button_tooltip = button_tooltip

        self.checked_actions = []
        self.default_button_text = "None"

        # setup ui
        self.menu = CustomQMenu(qtHelper.get_nuke_main_window())
        self.setup_ui()
        self._button.setMenu(self.menu)

    # setup ui

    def setup_ui(self):
        # widgets
        self._label = QLabel()
        self._label.setText(self._label_text)

        self._button = QPushButton()
        self._button.setText(self.default_button_text)
        self._button.setCheckable(True)
        if self._button_tooltip:
            self._button.setToolTip(self.button_tooltip)

        # layout
        self._layout = QHBoxLayout(self)

        self._layout.addWidget(self._label)
        self._layout.addWidget(self._button)

        self.setLayout(self._layout)

    def update_button_text(self):
        checked_actions = [action for action in self.menu.actions() if action.isChecked()]
        if len(checked_actions) > 3:
            checked_actions = checked_actions[:3] + [QAction("...", self.parent)]
        text = ", ".join(action.text() for action in checked_actions) if checked_actions else self.default_button_text
        self._button.setText(text)

    # menu

    def toggle_menu(self):
        print("Togle menu")
        if self._button.isChecked():
            # Adjust the width of the menu to match the button's width
            self.menu.setFixedWidth(self._button.width())

            self.menu.exec_(self._button.mapToGlobal(QPoint(0, self._button.height())))
        else:
            self.menu.close()

    # alike comboBox methods

    def addItem(self, text: str, checked: bool = False) -> QAction:
        action = QAction(text, self.parent)
        action.setCheckable(True)
        action.setChecked(checked)
        action.changed.connect(self.update_button_text)  # Connect to check state changed signal
        self.menu.addAction(action)

        if checked:
            self.checked_actions.append(action)

        return action

    def setItemData(self, item, value):
        item.setData(value)

    def getItemData(self, item):
        return item.data()

    def items(self, only_checked=False) -> list:
        if only_checked:
            return [action for action in self.menu.actions() if action.isChecked()]
        else:
            return self.menu.actions()

