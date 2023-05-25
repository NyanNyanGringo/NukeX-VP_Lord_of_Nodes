"""
# TODO: Bug with C++ doesn't exists when open create hotkey menu
# TODO: Funtion to delete from .nuke lines with custom presets


"""


import nuke
import os

from lord_of_nodes import hotkey_creator
from lord_of_nodes import hotkey_edit_menu
from lord_of_nodes import hotkey_edit_node_graph
from lord_of_nodes import knob_default_creator

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
menu.addSeparator()
set_knobs = menu.addCommand(settings.set_knob_default_menu_name, knob_default_creator.add_knob_default_for_selected_node)
remove_knobs = menu.addCommand(settings.remove_knob_default_menu_name, knob_default_creator.remove_knob_default_for_selected_node)


# Set icons
create.setIcon(os.path.join(osHelper.get_icon_path(), "create_icon.png"))
edit.setIcon(os.path.join(osHelper.get_icon_path(), "menu_icon.png"))


# Create config if it is not exists
configHelper.check_config_exists_else_create_it(conf_file_path=configHelper.get_user_config_path())
configHelper.check_config_exists_else_create_it(conf_file_path=configHelper.get_presets_config_path())


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


# make knob default
nuke.addOnUserCreate(knob_default_creator.apply_preset_on_user_create)
