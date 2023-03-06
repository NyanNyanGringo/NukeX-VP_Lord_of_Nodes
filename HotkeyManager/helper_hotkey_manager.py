import nuke
import os

from PySide2.QtWidgets import QApplication

import helper_config
import hotkey_manager_settings as settings


# ADD HOTKEYS

def load_toolset_to_nodegraph(toolset_name):
    """
    The main function that import and create toolset to NodeGraph
    when user call action using Hotkey or Nuke Nodes Menu
    :param toolset_name: str
    :return: None
    """
    all_nodes_before_load_toolset = nuke.allNodes()
    selected_nodes_before_load_toolset = nuke.selectedNodes()

    [node.setSelected(False) for node in nuke.allNodes()]

    nuke.loadToolset(get_toolset_path(toolset_name))

    toolset_nodes = [node for node in nuke.allNodes() if node not in all_nodes_before_load_toolset]

    input_node, output_node, show_panel_node = find_input_output_show_panel_nodes(toolset_nodes)

    if selected_nodes_before_load_toolset:
        topNode = selected_nodes_before_load_toolset[0]
        botNodes = topNode.dependent()  # Sometimes doesn't work with first
        botNodes = topNode.dependent()  # call. So we call "dependent()" twice.

        x_pos_before = input_node.xpos()
        y_pos_before = input_node.ypos()
        x_pos_after, y_pos_after = get_node_bottom_xy_position(input_node, topNode)

        x_transform = x_pos_after - x_pos_before
        y_transform = y_pos_after - y_pos_before
        [n.setXYpos(n.xpos() + x_transform, n.ypos() + y_transform) for n in toolset_nodes]

        input_node.setInput(0, topNode)

        if len(botNodes) > 0:

            for botNode in botNodes:

                # Get dict of key "input number" and value "None or Node Object"
                inputs_dict = {}
                for input_number in range(0, botNode.inputs()):
                    input_node = botNode.input(input_number)
                    inputs_dict[input_number] = input_node

                # Set dependent input to main node
                for input_number, input_node in inputs_dict.items():
                    if input_node == topNode:
                        botNode.setInput(input_number, output_node)

    if show_panel_node:
        show_panel_node.showControlPanel(True)


def add_hotkey_to_menu_by_toolset_name(toolset_name):
    """
    The main function that adds hotkey to Nodes menu, so we can call it
    :param toolset_name: str | without ".nk" only name
    :rtype: None
    """
    menu_hotkeys = nuke.menu('Nodes').addMenu(settings.tab_name_in_nuke_menu)
    menu_hotkeys.addCommand(name=toolset_name,
                            command=lambda: load_toolset_to_nodegraph(toolset_name),
                            shortcut=helper_config.read_config_key(toolset_name)["hotkey"])


# WIDGETS


def get_nuke_main_window():
    """
    :return: Nuke main window
    """
    widget = QApplication.instance().activeWindow()
    if widget:
        return widget
    # qApp = QApplication.instance()
    # for widget in qApp.topLevelWidgets():
    #     if widget.metaObject().className() == 'Foundry::UI::DockMainWindow':
    #         return widget
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


# OS


def get_current_path():
    """
    Return Hotkey Manager path like "C:/Users/user/.nuke/Python/HotkeyManager"
    :return: str
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")


# TOOLSETS


def get_toolset_path(toolset_name=None):
    """
    Return path to our custom toolsets or to given toolset by name
    :param toolset_name: str
    :return: str
    """
    if toolset_name:
        return os.path.join(get_current_path(), "ToolSets", toolset_name + ".nk").replace("\\", "/")
    return os.path.join(get_current_path(), "ToolSets").replace("\\", "/")


def get_list_of_toolsets():
    """
    Return list of toolsets without ".nk"
    :return: list
    """
    list_of_toolsets = []
    for file in os.listdir(get_toolset_path()):
        list_of_toolsets.append(file.replace(".nk", ""))
    return list_of_toolsets


def get_list_of_toolsets_with_path():
    """
    Return list of toolsets without ".nk" but with full path
    :return:
    """
    list_of_toolsets = []
    for file in os.listdir(get_toolset_path()):
        list_of_toolsets.append(os.path.join(get_toolset_path(), file.replace(".nk", "")).replace("\\", "/"))
    return list_of_toolsets


def delete_toolset_by_name(toolset_name):
    """
    Remove Toolset.nk file and delete it from config file and delete it from menu
    :param toolset_name: str | with no ".nk"
    """

    if toolset_name in get_list_of_toolsets():
        os.remove(os.path.join(get_toolset_path(), toolset_name + ".nk").replace("\\", "/"))

    if helper_config.check_key(toolset_name):
        helper_config.delete_key(toolset_name)

    menu_hotkeys = nuke.menu("Nodes").addMenu(settings.tab_name_in_nuke_menu)
    menu_hotkeys.removeItem(menu_hotkeys.findItem(toolset_name).name())


def load_and_get_toolset_nodes(toolset_name):
    """
    Load toolset to Nuke and return all it's nodes
    :param toolset_name: str
    :return: list
    """
    all_nodes_before_load_toolset = nuke.allNodes()
    [node.setSelected(False) for node in all_nodes_before_load_toolset]
    nuke.loadToolset(get_toolset_path(toolset_name))
    return [node for node in nuke.allNodes() if node not in all_nodes_before_load_toolset]


def get_toolsets_hotkeys_list():
    """
    Return list of all hotkeys that using Hotkey Manager
    :return:
    """
    l = []
    for toolset_name, dict_of_values in helper_config.read_config().items():
        l.append(dict_of_values["hotkey"].replace(" ", "").lower())
    return l


def get_string_of_all_nodes_of_toolset(toolset_name):
    """
    Return string of all nodes that toolset has. So it can be used in
    table item tooltip
    :param toolset_name: str
    :return: str
    """
    selected_nodes = nuke.selectedNodes()
    all_nodes = nuke.allNodes()

    [node.setSelected(False) for node in all_nodes]

    nuke.loadToolset(os.path.join(get_toolset_path(), toolset_name + ".nk"))
    toolset_nodes = [node for node in nuke.allNodes() if node not in all_nodes]

    i = 0
    tooltip = str()
    for toolset_node in toolset_nodes:
        if i == 0:
            tooltip = toolset_node.Class()
        else:
            tooltip += "\n" + toolset_node.Class()
        nuke.delete(toolset_nodes[i])
        i += 1

    [node.setSelected(True) for node in all_nodes if node in selected_nodes]

    return tooltip

# NODE GRAPH


def get_node_bottom_xy_position(toNode, aboutNode):
    """
    Return Node button position relative to other node
    :param toNode: Node
    :param aboutNode: Node
    :return: tuple (x and y position)
    """
    tempNode = getattr(nuke.nodes, toNode.Class())()

    x1, y1 = tempNode.xpos(), tempNode.ypos()
    w1, h1 = tempNode.screenWidth(), tempNode.screenHeight()

    x2, y2 = aboutNode.xpos(), aboutNode.ypos()
    w2, h2 = aboutNode.screenWidth(), aboutNode.screenHeight()

    distance = 6
    x = x2 + w2 // 2 - w1 // 2
    y = y2 + h2 + distance

    nuke.delete(tempNode)

    return x, y


def find_input_output_show_panel_nodes(nodes):
    """
    Search in nodes input, output and show_panel nodes and return its
    :param nodes: list of Nodes
    :return: tuple of input, output and show_panel nodes
    """
    input_node = None
    output_node = None
    show_panel_node = None
    for node in nodes:
        node_has_minimum_one_hotkey_knob = False
        for knob_name, knob in node.knobs().items():
            if knob_name == "HK_input_node":
                input_node = node
                node.removeKnob(knob)
                node_has_minimum_one_hotkey_knob = True
            if knob_name == "HK_output_node":
                output_node = node
                node.removeKnob(knob)
                node_has_minimum_one_hotkey_knob = True
            if knob_name == "HK_show_panel_node":
                show_panel_node = node
                node.removeKnob(knob)
                node_has_minimum_one_hotkey_knob = True
            if knob_name == "HK_other_node":
                node.removeKnob(knob)
                node_has_minimum_one_hotkey_knob = True
        if not node_has_minimum_one_hotkey_knob:
            raise RuntimeError("Node " + node.name() + " doesn't have any Hotkey knobs! Maybe this node haven't been"
                                                       " imported from ToolSet correctly!")

        # Remove 'User' node if it is the only one left
        node_knobs = node.knobs()
        if "User" in node_knobs:
            temp_node = getattr(nuke.nodes, node.Class())()
            if len(temp_node.knobs()) == (len(node_knobs) - 1):
                [node.removeKnob(k) for k_name, k in node_knobs.items() if k_name == "User"]
            nuke.delete(temp_node)

    if not input_node or not output_node:
        raise RuntimeError("Can't find input or output node!")

    return input_node, output_node, show_panel_node


def delete_extra_knobs_from_toolset_nodes(toolset_nodes):
    """
    Deletes from toolset_nodes input, output and show_panel knobs
    :param toolset_nodes: list of Nodes
    :return: None
    """
    for node in toolset_nodes:
        for knob_name, knob in node.knobs().items():
            if knob_name == "input_node":
                node.removeKnob(knob)
            if knob_name == "output_node":
                node.removeKnob(knob)
            if knob_name == "show_panel_node":
                node.removeKnob(knob)
        # Remove 'User' node if it is the only one left
        node_knobs = node.knobs()
        if "User" in node_knobs:
            temp_node = getattr(nuke.nodes, node.Class())()
            if len(temp_node.knobs()) == (len(node_knobs) - 1):
                [node.removeKnob(k) for k_name, k in node_knobs.items() if k_name == "User"]
            nuke.delete(temp_node)


def get_label_for_backdrop(toolset_name, hotkey):
    return '<font color="#fffff0" face="Verdana">' + toolset_name + " | " + hotkey


def check_editor_in_nodegraph():
    """
    Check if Editor Menu already opened in NodeGraph
    :return: bool
    """
    for node in nuke.allNodes():
        if node.Class() in ["BackdropNode", "NoOp"]:
            if node["tile_color"].value() in [settings.bg_color, settings.button_color]:
                if any([n for n in [settings.backdrop_subname, settings.save_node_subname, settings.delete_node_subname] if n in node.name()]):
                    return True
    return False


def check_node_is_gizmo_or_contains_gizmo(node):
    if type(node) == nuke.Gizmo and node.Class() == "Gizmo":
        return True
    elif type(node) == nuke.Group:
        with node:
            for n in nuke.allNodes():
                if check_node_is_gizmo_or_contains_gizmo(n):
                    return True
    return False


# COLOR


def rgb_to_hex(r, g, b, zero_to_one_range):
    # zero_to_one_range True - R, G, B in range 1 to 0
    # zero_to_one_range False - R, G, B in range 0 to 255

    if zero_to_one_range:
        mult = 255
    else:
        mult = 1

    r = int(r * mult)
    g = int(g * mult)
    b = int(b * mult)
    hex = int("%02x%02x%02x%02x" % (r, g, b, 1), 16)

    return hex


def hex_to_rgb(hex):
    # use binar python operators to convert HEX to RGB

    hex = int(hex)
    r = (0xFF & hex >> 24) / 255.0
    g = (0xFF & hex >> 16) / 255.0
    b = (0xFF & hex >> 8) / 255.0

    return r, g, b


# OTHER

def check_symbol_is_english(symbol):
    """
    Check if symbol is English or not
    :param symbol: str
    :return: bool
    """
    try:
        symbol.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
