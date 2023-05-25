import nuke

import lord_of_nodes.hotkey_manager_settings as settings


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
