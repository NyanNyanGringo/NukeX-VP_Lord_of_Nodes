import os
import nuke

from lord_of_nodes.helpers import osHelper, configHelper
import lord_of_nodes.hotkey_manager_settings as settings


def get_list_of_toolsets():
    """
    Return list of toolsets without ".nk"
    :return: list
    """
    list_of_toolsets = []
    for file in os.listdir(osHelper.get_toolset_path()):
        list_of_toolsets.append(file.replace(".nk", ""))
    return list_of_toolsets


def get_list_of_toolsets_with_path():
    """
    Return list of toolsets without ".nk" but with full path
    :return:
    """
    list_of_toolsets = []
    for file in os.listdir(osHelper.get_toolset_path()):
        list_of_toolsets.append(os.path.join(osHelper.get_toolset_path(), file.replace(".nk", "")).replace("\\", "/"))
    return list_of_toolsets


def delete_toolset_by_name(toolset_name):
    """
    Remove Toolset.nk file and delete it from config file and delete it from menu
    :param toolset_name: str | with no ".nk"
    """

    if toolset_name in get_list_of_toolsets():
        os.remove(os.path.join(osHelper.get_toolset_path(), toolset_name + ".nk").replace("\\", "/"))

    if configHelper.check_key(toolset_name):
        configHelper.delete_key(toolset_name)

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
    nuke.loadToolset(osHelper.get_toolset_path(toolset_name))
    return [node for node in nuke.allNodes() if node not in all_nodes_before_load_toolset]


def get_toolsets_hotkeys_list():
    """
    Return list of all hotkeys that using Hotkey Manager
    :return:
    """
    l = []
    for toolset_name, dict_of_values in configHelper.read_config().items():
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

    nuke.loadToolset(os.path.join(osHelper.get_toolset_path(), toolset_name + ".nk"))
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
