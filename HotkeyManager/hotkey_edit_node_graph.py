import nuke
import nukescripts
import os

import helper_config
import helper_hotkey_manager as helper
import hotkey_manager_settings as settings

import hotkey_creator


class HotkeyEditNodeGraphWidget(hotkey_creator.HotkeyCreatorWidget):
    """
    Modified instance of HotkeyCreatorWidget used to edit existing toolsets
    in NodeGraph
    """

    def __init__(self, parent, emitter_node):
        super(HotkeyEditNodeGraphWidget, self).__init__(parent)

        # VARIABLES
        self._not_show_panel_name = "None"

        self.parent = parent
        self.emitter_node = emitter_node  # If class emitted from node (button "SAVE" from NodeGraph)

        # SETUP UI
        self.ui_pushButton_create.setText("Save")

        # CONSTRUCT
        self.construct_if_emitter()

        # CONNECTS
        self.connects_if_emitter()

    # CONSTRUCT

    def construct_if_emitter(self):
        self.autofill_input_node_if_emitter()
        self.autofill_output_node_if_emitter()
        self.autofill_name_if_emitter()
        self.autofill_hotkey_if_emitter()

    # CONNECTS

    def connects_if_emitter(self):
        self.ui_comboBox_input_node.currentIndexChanged.disconnect()
        self.ui_comboBox_input_node.currentIndexChanged.connect(self.autofill_output_node)

        self.ui_pushButton_create.clicked.disconnect()
        self.ui_pushButton_create.clicked.connect(self.start_create_hotkey_if_emitter)

    # AUTOFILL

    def autofill_input_node_if_emitter(self):
        self.ui_comboBox_input_node.setCurrentIndex(0)

    def autofill_output_node_if_emitter(self):
        self.ui_comboBox_output_node.setCurrentIndex(0)

    def autofill_name_if_emitter(self):
        self.ui_lineEdit_name.setText(self.get_toolset_name_from_emitter())

    def autofill_hotkey_if_emitter(self):
        hotkey = helper_config.read_config_key(self.get_toolset_name_from_emitter())["hotkey"]
        if "ctrl" in hotkey:
            self.ui_checkBox_ctrl_hotkey.setChecked(True)
        if "shift" in hotkey:
            self.ui_checkBox_shift_hotkey.setChecked(True)
        if "alt" in hotkey:
            self.ui_checkBox_alt_hotkey.setChecked(True)
        self.ui_lineEdit_hotkey.setText(hotkey[-1])

    # CREATE HOTKEY

    def start_create_hotkey_if_emitter(self):
        if self.check_before_start_create_hotkey_if_emitter():
            helper.delete_toolset_by_name(self.get_toolset_name_from_emitter())
            self.set_input_output_show_panel_info_to_nodes()
            self.create_toolset()
            helper.delete_extra_knobs_from_toolset_nodes(self.selected)
            self.write_config_about_toolset()
            helper.add_hotkey_to_menu_by_toolset_name(self.ui_lineEdit_name.text())
            self.rename_nodes_if_edit_opened_in_nodegraph()
            self.close()
            nuke.message(settings.finish_message)

    def rename_nodes_if_edit_opened_in_nodegraph(self):
        last_preset_name = self.get_toolset_name_from_emitter()

        new_preset_name = self.ui_lineEdit_name.text()
        new_hotkey = self.get_hotkey()

        save_node = self.emitter_node
        delete_node = \
        [node for node in nuke.allNodes() if node.name() == last_preset_name + settings.delete_node_subname][0]
        backdrop = [node for node in nuke.allNodes() if node.name() == last_preset_name + settings.backdrop_subname][0]

        # Change BackDrop
        backdrop.unlock()
        backdrop["label"].setValue(helper.get_label_for_backdrop(new_preset_name, new_hotkey))
        backdrop["name"].setValue(new_preset_name + settings.backdrop_subname)
        backdrop.lock()

        # Change SaveNode and DeleteNode
        save_node.unlock()
        save_node["name"].setValue(new_preset_name + settings.save_node_subname)
        save_node.lock()
        delete_node.unlock()
        delete_node["name"].setValue(new_preset_name + settings.delete_node_subname)
        delete_node.lock()

    # CHECKERS

    def check_before_start_create_hotkey_if_emitter(self):
        if self.check_preset_name_is_not_empty():
            if self.check_hotkey_is_not_empty():
                if not self.check_preset_with_same_name_exists_if_emitter():
                    if not self.check_hotkey_already_exists_if_emitter():
                        if self.check_input_output_is_not_none():
                            if self.ask_if_global_hotkey_already_exists():
                                return True

    def check_preset_with_same_name_exists_if_emitter(self):
        if not self.get_toolset_name_from_emitter() == self.ui_lineEdit_name.text():
            if (self.ui_lineEdit_name.text() + ".nk") in os.listdir(helper.get_toolset_path()):
                nuke.message("Preset with name " + self.ui_lineEdit_name.text() + " already exists!")
                return True
        return False

    def check_hotkey_already_exists_if_emitter(self):
        preset_hotkey = helper_config.read_config_key(self.get_toolset_name_from_emitter())["hotkey"]
        if os.path.exists(helper_config.get_user_config_path()):
            for toolset_name, dict_of_values in helper_config.read_config().items():
                if self.get_hotkey() == dict_of_values["hotkey"] and self.get_hotkey() != preset_hotkey:
                    nuke.message("Hotkey " + self.get_hotkey() + " already exist in preset " + toolset_name)
                    return True
        return False

    # HELPERS

    def get_toolset_name_from_emitter(self):
        return '_'.join(self.emitter_node.name().split("_")[0:-1])


def show_editor_in_nodegraph():
    """
    Show Edit NodeGraph nodes in NodeGraph. These nodes include:
    1) BackDrops - the main element that contains all info aboout
    toolset
    2) Node-buttons (save and delete) - the main buttons that used
    to save or delete presets
    3) BackDrops Nodes - all nodes inside BackDrop that contains
    in toolset
    :return: None
    """
    # Find all toolsets to create
    toolsets_to_create = helper.get_list_of_toolsets()

    all_nodes_before_load_toolset = nuke.allNodes()
    for toolset_name in toolsets_to_create:
        try:
            toolset_nodes = helper.load_and_get_toolset_nodes(toolset_name)
            helper.find_input_output_show_panel_nodes(toolset_nodes)
            for node in toolset_nodes:
                nuke.delete(node)
        except RuntimeError:
            nuke.message("My Lord, can't create " + toolset_name + "!\nPlease delete this hotkey.")
            helper.find_edit_node_graph_action().setChecked(False)
            return

    # Find start position in NodeGraph for creating toolsets (BackDrops, Node-Buttons etc.).
    # It calculates as the lowest and middle position relative of all nodes. If no
    # nodes in NodeGraph - position will be zero for x and y.
    if nuke.allNodes():
        max_y = max([node.ypos() + node.screenHeight() for node in nuke.allNodes()])
        x_list = [node.xpos() + node.screenWidth() // 2 for node in nuke.allNodes()]
        start_x, start_y = ((min(x_list) + max(x_list)) // 2), (max_y + 150)
    else:
        start_x = 0
        start_y = 0

    # Creating list [BackDrop, [SaveNode-Button, DeleteNode-Button], [ToolsetNodes]]
    list_of_items = []
    for toolset_name in toolsets_to_create:
        # Get ToolsetNodes
        toolset_nodes = helper.load_and_get_toolset_nodes(toolset_name)

        # Get and setup BackDrop
        [node.setSelected(True) for node in toolset_nodes]
        backdrop = nukescripts.autoBackdrop()
        hotkey = helper_config.read_config_key(toolset_name)["hotkey"]
        backdrop["label"].setValue(helper.get_label_for_backdrop(toolset_name, hotkey))
        backdrop["tile_color"].setValue(settings.bg_color)
        backdrop["name"].setValue(toolset_name + settings.backdrop_subname)

        # Get and setup SaveNode-Button and DeleteNode-Button
        save_node = nuke.nodes.NoOp(name=toolset_name + settings.save_node_subname)
        delete_node = nuke.nodes.NoOp(name=toolset_name + settings.delete_node_subname)
        for node in save_node, delete_node:
            node.knob("autolabel").setValue("nuke.thisNode()['label'].value()")
            node["hide_input"].setValue(True)
            node["label"].setValue(node.name().split("_")[-1].upper())
            node["tile_color"].setValue(settings.button_color)

        # Add all to list
        list_of_items.append([backdrop, [save_node, delete_node], toolset_nodes])

    def get_width_height_center(nodes):
        """
        Return nodes width, height and centre positions
        :param nodes: list of nodes
        :return: tuple
        """
        min_x = min([node.xpos() for node in nodes])
        max_x = max([node.xpos() + node.screenWidth() for node in nodes])
        min_y = min([node.ypos() for node in nodes])
        max_y = max([node.ypos() + node.screenHeight() for node in nodes])

        width, height = max_x - min_x, max_y - min_y
        center_x, center_y = min_x + width // 2, min_y + height // 2

        return width, height, center_x, center_y

    def get_backdrop_n_buttons_n_toolset_nodes(items):
        """
        Return BackDrop, SaveNode-Button, DeleteNode-Button and ToolsetNodes
        :param items: items to unpack
        :return: tuple
        """
        backdrop = items[0]
        save_node = items[1][0]
        delete_node = items[1][1]
        toolset_nodes = items[2]
        return backdrop, save_node, delete_node, toolset_nodes

    # Finding max width or height for BackDrop. Some toolsets might be very large. So we need to find
    # maximum width or height from all toolsets. This value will be the size size of all
    # other BackDrops
    longest_sides = []
    for items in list_of_items:
        backdrop, save_node, delete_node, toolset_nodes = get_backdrop_n_buttons_n_toolset_nodes(items)
        width, height, center_x, center_y = get_width_height_center(toolset_nodes)
        longest_sides.append(max(width, height))
    longest_side = max(longest_sides) + 150
    if longest_side < 440:
        longest_side = 440

    # Set BackDrop to the lowest point relative toolset
    for items in list_of_items:
        backdrop, save_node, delete_node, toolset_nodes = get_backdrop_n_buttons_n_toolset_nodes(items)

        width, height, center_x, center_y = get_width_height_center(toolset_nodes)

        backdrop["bdwidth"].setValue(longest_side)
        backdrop["bdheight"].setValue(longest_side)

        backdrop_final_x = center_x - longest_side // 2
        backdrop_final_y = center_y - longest_side // 2

        backdrop.setXYpos(backdrop_final_x, backdrop_final_y)
        save_node.setXYpos(backdrop_final_x, backdrop_final_y)
        delete_node.setXYpos(backdrop_final_x, backdrop_final_y)

    # Set position of parts (BackDrop + Node-Buttons + ToolsetNodes)
    # one by one as grid
    i = 0
    start_x_before = start_x
    for items in list_of_items:
        backdrop, save_node, delete_node, toolset_nodes = get_backdrop_n_buttons_n_toolset_nodes(items)
        for node in toolset_nodes + [save_node, delete_node, backdrop]:
            node_x_relative_bd = node.xpos() - backdrop.xpos()
            node_y_relative_bd = node.ypos() - backdrop.ypos()
            node.setXYpos(start_x + node_x_relative_bd, start_y + node_y_relative_bd)

            if settings.delete_node_subname in node.name():
                node.setXpos(node.xpos() + 80)

        start_x += longest_side + 50
        i += 1
        if (i % 3) == 0:
            start_x = start_x_before
            start_y += longest_side + 50

    # Delete knobs input, output and show_panel in toolset nodes
    for items in list_of_items:
        backdrop, save_node, delete_node, toolset_nodes = get_backdrop_n_buttons_n_toolset_nodes(items)
        helper.find_input_output_show_panel_nodes(toolset_nodes)

    # Set additional settings for BackDrop and Buttons
    for items in list_of_items:
        backdrop, save_node, delete_node, toolset_nodes = get_backdrop_n_buttons_n_toolset_nodes(items)

        backdrop.knob("knobChanged").setValue(
            """
try:
    this_node = nuke.thisNode()
    this_knob = nuke.thisKnob()

    if this_knob.name() == "selected":
        this_node.setSelected(False)
except:
    raise Exception("Error in BackDropNode knobChanged!")
""")

        save_node.knob("knobChanged").setValue(
            """
try:
    import hotkey_edit_node_graph
    import helper_hotkey_manager as helper
    
    this_node = nuke.thisNode()
    this_knob = nuke.thisKnob()
    
    if this_knob.name() == "selected":
        # Get backdrop
        backdrop = nuke.toNode('_'.join(this_node.name().split("_")[0:-1]) + '""" + settings.backdrop_subname + """')
        toolset_nodes = backdrop.getNodes()
        
        if not toolset_nodes:
            nuke.message("Inside backdrop should be at least one node!")
            [node.setSelected(False) for node in nuke.allNodes()]
        else:
            [node.setSelected(False) for node in nuke.allNodes()]
            [node.setSelected(True) for node in toolset_nodes]
            
            if not helper.check_hotkey_manager_creator_is_opened():
                nuke_main_window = helper.get_nuke_main_window()
                nuke_main_window.setEnabled(False)
                edit_widget = hotkey_edit_node_graph.HotkeyEditNodeGraphWidget(parent=nuke_main_window, emitter_node=this_node)
                edit_widget.show()
except:
    raise Exception("Error in SAVE node knobChanged!")
""")

        delete_node.knob("knobChanged").setValue(
            """
try:
    import helper_hotkey_manager as helper
    
    
    this_node = nuke.thisNode()
    this_knob = nuke.thisKnob()
    
    if this_knob.name() == "selected" and this_node.isSelected():
        if nuke.ask("Are you sure you want to delete preset?"):
            toolset_name = '_'.join(this_node.name().split("_")[0:-1])
            helper.delete_toolset_by_name(toolset_name)
            backdrop = nuke.toNode(toolset_name + '""" + settings.backdrop_subname + """')
            save_node = nuke.toNode(toolset_name + '""" + settings.save_node_subname + """')
            delete_node = nuke.toNode(toolset_name + '""" + settings.delete_node_subname + """')
            toolset_nodes = backdrop.getNodes()
            
            for node in toolset_nodes + [backdrop, save_node, delete_node]:
                node.unlock()
            delete_node["knobChanged"].setValue("")  # clear knobChanged to not 
                                                     # cause errors after deleting delete_node
            for node in toolset_nodes + [backdrop, save_node, delete_node]:
                nuke.delete(node)
                
            if not helper.get_list_of_toolsets():
                edit_node_graph_action = helper.find_edit_node_graph_action()
                edit_node_graph_action.setChecked(False)
        else:
            this_node.setSelected(False)
except:
    raise Exception("Error in DELETE node knobChanged!")
""")
        backdrop.lock()
        save_node.lock()
        delete_node.lock()

    # Zoom to nodes
    [node.setSelected(False) for node in nuke.allNodes()]
    for items in list_of_items:
        backdrop, save_node, delete_node, toolset_nodes = get_backdrop_n_buttons_n_toolset_nodes(items)
        for node in [backdrop]:
            node.setSelected(True)

    nuke.zoomToFitSelected()


def hide_editor_in_nodegraph():
    """
    Find Edit NodeGraph nodes (backdrops and it's elements, node-buttons)
    in NodeGraph and delete it
    :return: None
    """
    # Delete buttons
    for node in nuke.allNodes():
        if node.Class() == "NoOp":
            if node["tile_color"].value() == settings.button_color:
                if settings.save_node_subname in node.name() or settings.delete_node_subname in node.name():
                    node.unlock()
                    nuke.delete(node)
    # Delete backdrops and its contain
    for node in nuke.allNodes():
        if node.Class() == "BackdropNode":
            if node["tile_color"].value() == settings.bg_color:
                if settings.backdrop_subname in node.name():
                    node.unlock()
                    for inside_node in node.getNodes():
                        inside_node.unlock()
                        nuke.delete(inside_node)
                    nuke.delete(node)


def check_before_start():
    """
    Check before start showing all toolsets in NodeGraph
    :return: bool
    """
    if not helper.check_node_graph_is_visible_and_not_hidden():
        nuke.message("Please select NodeGraph tab first!")
        return False
    if not helper.get_list_of_toolsets():
        nuke.message("No Hotkeys exists!")
        helper.find_edit_node_graph_action().setChecked(False)
        return False
    return True


def start():
    """
    Start showing all toolsets in NodeGraph
    :return: None
    """
    if check_before_start():
        if helper.find_edit_node_graph_action().isChecked():
            show_editor_in_nodegraph()
            helper.set_mouse_tracking_in_nodegraph(False)
        else:
            hide_editor_in_nodegraph()
            helper.set_mouse_tracking_in_nodegraph(True)
    else:
        helper.find_edit_node_graph_action().setChecked(False)
