import nuke

from lord_of_nodes.helpers import osHelper, nukeHelper, configHelper
from lord_of_nodes.knob_default_creator import apply_preset_on_user_create
import lord_of_nodes.hotkey_manager_settings as settings


# WORK WITH CONTEXT SENSITIVE


def get_supported_context_sensitive_knobs():
    return ("CurveTool",  # IMAGE
            "Noise", "Text", "Radial", "Rectangle",  # DRAW
            "FrameHold", "FrameRange", "Kronos", "OFlow2", "Retime", "TimeWarp",  # TIME
            "ColorTransfer", "OCIOLookTransform", "OCIOFileTransform", "OCIODisplay",  # COLOR
            "OCIOColorSpace", "OCIOCDLTransform",  # COLOR
            "GodRays", "Inpaint2",  # FILTER
            "Primatte3",  # KEYER
            "CopyRectangle",  # MERGE
            "Transform", "TransformMasked", "Tracker4", "GridWarp2", "Crop",  # TRANSFORM
            "CornerPin2D", "VectorCornerPin",  # TRANSFORM
            "DeepCrop")  # DEEP


def check_node_has_context_sensitive_knobs(node) -> bool:
    return node.Class() in get_supported_context_sensitive_knobs()


def set_context_sensitive_knobs(to_node, top_node=None) -> None:
    """
    Set knob values to context-sensitive knobs for to_node
    """
    selected = nuke.selectedNodes()
    [n.setSelected(False) for n in nuke.allNodes()]

    # VARIABLES
    input_not_connected = True  # checks if temp_node connected to top_node else use Root settings

    if top_node:
        top_node.setSelected(True)
        temp_node = nuke.createNode(to_node.Class(), inpanel=False)
        input_not_connected = 1 - bool(temp_node.inputs())

        if input_not_connected:
            nuke.delete(temp_node)
        else:
            first, last = temp_node.upstreamFrameRange(0).first(), temp_node.upstreamFrameRange(0).last()
            width, height = temp_node.width(), temp_node.height()

    if input_not_connected:
        temp_node = nuke.createNode(to_node.Class(), inpanel=False)

        first, last = nuke.Root()["first_frame"].value(), nuke.Root()["last_frame"].value()
        width, height = nuke.Root().format().width(), nuke.Root().format().height()

    bbox = [0, 0, width, height]
    area = [width / 4, height / 4, (width - (width / 4)), height - (height / 4)]
    center = [width / 2, height / 2]

    # IMAGE
    if to_node.Class() == "CurveTool":
        to_node["ROI"].setValue(area)
        to_node["autocropdata"].setValue(area)

    # DRAW
    if to_node.Class() in ["Noise", "Text"]:
        to_node["center"].setValue(center)
        if to_node.Class() == "Text":
            to_node["box"].setValue(area)

    if to_node.Class() == "Radial" or to_node.Class() == "Rectangle":
        to_node["area"].setValue(area)

    # TIME
    if to_node.Class() == "FrameHold":
        to_node["firstFrame"].setValue(nuke.frame())

    if to_node.Class() == "FrameRange":
        to_node["first_frame"].setValue(first)
        to_node["last_frame"].setValue(last)

    if to_node.Class() in ["Kronos", "OFlow2", "Retime"]:
        to_node["input.first"].setValue(first)
        to_node["input.last"].setValue(last)
        if to_node.Class() == "Retime":
            to_node["output.first"].setValue(first)
            to_node["output.last"].setValue(last)

    if to_node.Class() == "TimeWarp":
        to_node["lookup"].clearAnimated()
        to_node["lookup"].setAnimated()
        to_node["lookup"].setValueAt(first, first)
        to_node["lookup"].setValueAt(last, last)

    # COLOR
    if to_node.Class() in ["OCIOLookTransform", "OCIOFileTransform", "OCIODisplay", "OCIOColorSpace",
                           "OCIOCDLTransform"]:
        for knob_name in get_automatic_context_sensitive_knobs(to_node):
            value = temp_node[knob_name].value()
            to_node[knob_name].setValue(value)

    if to_node.Class() == "ColorTransfer":
        to_node["ROI"].setValue(area)

    # FILTER
    if to_node.Class() in ["GodRays", "Inpaint2"]:
        to_node["center"].setValue(center)

    # KEYER
    if to_node.Class() == "Primatte3":
        to_node["crop"].setValue(bbox)

    # MERGE
    if to_node.Class() == "CopyRectangle":
        to_node["area"].setValue(area)

    # TRANSFORM
    if to_node.Class() in ["Transform", "TransformMasked", "Tracker4", "GridWarp2"]:
        to_node["center"].setValue(center)

    if to_node.Class() == "Crop":
        to_node["box"].setValue(bbox)

    if to_node.Class() in ["CornerPin2D", "VectorCornerPin"]:

        pairs = [['to1', 'to2', 'to3', 'to4'], ['from1', 'from2', 'from3', 'from4']]

        if to_node.Class() == "VectorCornerPin":
            pairs.append(['user1', 'user2', 'user3', 'user4'])

        for pair in pairs:
            to_node[pair[0]].setValue([0, 0])
            to_node[pair[1]].setValue([width, 0])
            to_node[pair[2]].setValue([width, height])
            to_node[pair[3]].setValue([0, height])

    # DEEP
    if to_node.Class() == "DeepCrop":
        to_node["bbox"].setValue(area)

    # Put everything back the way it was in NodeGraph
    nuke.delete(temp_node)
    [n.setSelected(True) for n in selected]


def get_automatic_context_sensitive_knobs(node) -> list:
    """
    Try to understand what knobs are context sensetive in node
    and return list with these knobs (or empty list)
    """
    # remember selected nodes
    selected = nuke.selectedNodes()

    # create temp FrameRange and Reformat
    frame_range = nuke.nodes.FrameRange()
    reformat = nuke.nodes.Reformat()

    reformat.setInput(0, frame_range)
    reformat.autoplace()

    frame_range["first_frame"].setValue(5981)
    frame_range["last_frame"].setValue(5981)

    reformat["type"].setValue("to box")
    reformat["box_fixed"].setValue(True)
    reformat["box_width"].setValue(5981)
    reformat["box_height"].setValue(5981)

    # get context-sensitive knob values from node
    [n.setSelected(False) for n in nuke.allNodes()]
    reformat.setSelected(True)
    temp_node = nuke.createNode(node.Class(), inpanel=False)
    temp_node.resetKnobsToDefault()

    result = temp_node.writeKnobs(nuke.WRITE_NON_DEFAULT_ONLY).split(" ")

    if result == [""]:
        result = []

    # delete created temp Nodes
    nuke.delete(frame_range)
    nuke.delete(reformat)
    nuke.delete(temp_node)

    # restore selection
    [n.setSelected(True) for n in selected]

    return result


# WORK WITH TOOLSET

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

    nuke.loadToolset(osHelper.get_toolset_path(toolset_name))

    toolset_nodes = [node for node in nuke.allNodes() if node not in all_nodes_before_load_toolset]

    input_node, output_node, show_panel_nodes, context_sensitive_nodes, knob_default_nodes = get_nodes_by_extra_knobs_and_delete_extra_knobs(
        toolset_nodes)

    for node in knob_default_nodes:  # setup knob defaults
        apply_preset_on_user_create(node)

    if selected_nodes_before_load_toolset:
        topNode = selected_nodes_before_load_toolset[0]
        botNodes = topNode.dependent()  # Sometimes doesn't work with first
        botNodes = topNode.dependent()  # call. So we call "dependent()" twice.

        x_pos_before = input_node.xpos()
        y_pos_before = input_node.ypos()
        x_pos_after, y_pos_after = nukeHelper.get_node_bottom_xy_position(input_node, topNode)

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

        # set context-sensitive according topNode
        for node in context_sensitive_nodes:
            set_context_sensitive_knobs(node, topNode)
    else:
        # set context-sensitive according topNode
        for node in context_sensitive_nodes:
            set_context_sensitive_knobs(node)

    for node in show_panel_nodes:
        node.showControlPanel()


def add_hotkey_to_menu_by_toolset_name(toolset_name):
    """
    The main function that adds hotkey to Nodes menu, so we can call it
    :param toolset_name: str | without ".nk" only name
    :rtype: None
    """
    menu_hotkeys = nuke.menu('Nodes').addMenu(settings.tab_name_in_nuke_menu)
    menu_hotkeys.addCommand(name=toolset_name,
                            command=lambda: load_toolset_to_nodegraph(toolset_name),
                            shortcut=configHelper.read_config_key(toolset_name)["hotkey"])


# WORK WITH EXTRA KNOBS

def get_nodes_by_extra_knobs_and_delete_extra_knobs(nodes) -> tuple:
    """
    Search in nodes input, output and show_panel nodes and return its
    :param nodes: list of Nodes
    :return: tuple of input, output and show_panel nodes
    """
    input_node = None
    output_node = None
    show_panel_nodes = []
    context_sensitive_nodes = []
    knob_default_nodes = []

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
                show_panel_nodes.append(node)
                node.removeKnob(knob)
                node_has_minimum_one_hotkey_knob = True
            if knob_name == "HK_context_sensitive":
                context_sensitive_nodes.append(node)
                node.removeKnob(knob)
                node_has_minimum_one_hotkey_knob = True
            if knob_name == "HK_knob_default":
                knob_default_nodes.append(node)
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

    return input_node, output_node, show_panel_nodes, context_sensitive_nodes, knob_default_nodes
