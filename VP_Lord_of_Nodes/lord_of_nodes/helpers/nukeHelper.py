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
