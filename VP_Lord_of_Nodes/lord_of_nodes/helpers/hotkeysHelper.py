import nuke


from lord_of_nodes.helpers import osHelper, nukeHelper, configHelper
import lord_of_nodes.hotkey_manager_settings as settings


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

    input_node, output_node, show_panel_node = nukeHelper.find_input_output_show_panel_nodes(toolset_nodes)

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
                            shortcut=configHelper.read_config_key(toolset_name)["hotkey"])
