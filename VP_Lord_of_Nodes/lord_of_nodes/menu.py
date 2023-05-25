"""
# TODO: Bug with C++ doesn't exists when open create hotkey menu
"""


import nuke
import os

from lord_of_nodes import hotkey_creator
from lord_of_nodes import hotkey_edit_menu
from lord_of_nodes import hotkey_edit_node_graph

from lord_of_nodes.helpers import osHelper, configHelper, toolsetsHelper, hotkeysHelper, nukeHelper, qtHelper
import lord_of_nodes.hotkey_manager_settings as settings


# Create menu and menu items with actions
menu = nuke.menu("Nuke").addMenu(settings.tab_name_in_nuke_menu)

create = menu.addCommand(settings.hotkey_creator_menu_name,
                         hotkey_creator.start)
edit = menu.addCommand(settings.edit_menu_menu_name,
                       hotkey_edit_menu.start)
edit_node_graph = menu.addCommand(settings.edit_node_graph_menu_name,
                                  hotkey_edit_node_graph.start)
edit_node_graph.action().setCheckable(True)


# Set icons
create.setIcon(os.path.join(osHelper.get_icon_path(), "create_icon.png"))
edit.setIcon(os.path.join(osHelper.get_icon_path(), "menu_icon.png"))


# Create config if it is not exists
configHelper.check_config_exists_else_create_it()


# Exclude our custom toolset path from main ToolSets
nuke.addToolsetExcludePaths(os.path.dirname(osHelper.get_toolset_path()))


# Create toolset path if not exists
if not os.path.exists(osHelper.get_toolset_path()):
    os.mkdir(osHelper.get_toolset_path())


# Create shortcuts when Nuke starts
for toolset in toolsetsHelper.get_list_of_toolsets():
    hotkeysHelper.add_hotkey_to_menu_by_toolset_name(toolset)


# Set checked edit_node_graph if edit already opened in project
def set_checked_edit_node_graph_command_if_edit_opened():
    if nukeHelper.check_editor_in_nodegraph():
        edit_node_graph_action = qtHelper.find_edit_node_graph_action()
        edit_node_graph_action.setChecked(True)


nuke.addOnScriptLoad(set_checked_edit_node_graph_command_if_edit_opened)
