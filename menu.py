import nuke
import os

import hotkey_creator
import hotkey_edit_menu
import hotkey_edit_node_graph

import helper_config
import helper_hotkey_manager as helper
import hotkey_manager_settings as settings


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
icon_path = os.path.join(helper.get_current_path(), "icons")
create.setIcon(os.path.join(icon_path, "create_icon.png"))
edit.setIcon(os.path.join(icon_path, "menu_icon.png"))


# Create config if it is not exists
helper_config.check_config_exists_else_create_it()


# Exclude our custom toolset path from main ToolSets
nuke.addToolsetExcludePaths(os.path.dirname(helper.get_toolset_path()))


# Create toolset path if not exists
if not os.path.exists(helper.get_toolset_path()):
    os.mkdir(helper.get_toolset_path())


# Create shortcuts when Nuke starts
for toolset in helper.get_list_of_toolsets():
    helper.add_hotkey_to_menu_by_toolset_name(toolset)


# Set checked edit_node_graph if edit already opened in project
def set_checked_edit_node_graph_command_if_edit_opened():
    if helper.check_editor_in_nodegraph():
        edit_node_graph_action = helper.find_edit_node_graph_action()
        edit_node_graph_action.setChecked(True)


nuke.addOnScriptLoad(set_checked_edit_node_graph_command_if_edit_opened)
