import nuke
import nukescripts

from lord_of_nodes.helpers import presetHelper, configHelper


# APPLY ON USER CREATE


def apply_preset_on_user_create():
    node = nuke.thisNode()
    node_id = presetHelper.get_node_id(node)

    config = configHelper.get_presets_config_path()
    if configHelper.check_key(node_id, config):
        knobs = configHelper.read_config_key(node_id, configHelper.get_presets_config_path())

        temp_preset_name = "LORDOFNODES_TEMP_PRESET_NAME1"

        if temp_preset_name in nuke.getUserPresets(node):
            nuke.deleteUserPreset(node_id, temp_preset_name)

        nuke.setUserPreset(node_id, temp_preset_name, knobs)
        nukescripts.nodepresets.saveNodePresets()

        nuke.applyUserPreset(node_id, temp_preset_name, node)
        nukescripts.nodepresets.saveNodePresets()

        nuke.deleteUserPreset(node_id, temp_preset_name)
        nukescripts.nodepresets.saveNodePresets()

        return True


# CONFIG


def add_preset_to_config(node_id, knobs):
    config = configHelper.get_presets_config_path()
    configHelper.write_config(node_id, knobs, config)


def remove_preset_from_config(node_id):
    config = configHelper.get_presets_config_path()

    if configHelper.check_key(node_id, config):
        configHelper.delete_key(node_id, config)


# CHECK


def check_selection() -> bool:
    if not len(nuke.selectedNodes()) == 1:
        nuke.message("My Lord,\n\nPlease, select one node!")
        return False
    return True


def check_before_add_knob_default(node_id) -> bool:
    if configHelper.check_key(node_id, configHelper.get_presets_config_path()):
        if not nuke.ask(f"My Lord,\n\nKnobs Default already exists for {node_id}.\n\nContinue?"):
            return False

    return True


def check_before_remove_knob_default(node_id):
    if not configHelper.check_key(node_id, configHelper.get_presets_config_path()):
        nuke.message(f"My Lord,\n\nKnobs Default doesn't exists for {node_id}.")
        return False

    if not nuke.ask(f"My Lord,\n\nRemove Knobs Default for {node_id}?"):
        return False

    return True


# MAIN


def add_knob_default_for_selected_node():
    if not check_selection():
        return

    node = nuke.selectedNode()
    node_id = nuke.getNodePresetID()

    if not check_before_add_knob_default(node_id):
        return

    knobs = presetHelper.get_only_modified_by_user_knob_values(node, node_id)

    add_preset_to_config(node_id, knobs)

    nuke.message("Knobs Default successfully added!")


def remove_knob_default_for_selected_node():
    if not check_selection():
        return

    node_id = nuke.getNodePresetID()

    if not check_before_remove_knob_default(node_id):
        return

    remove_preset_from_config(node_id)

    nuke.message("Knobs Default successfully removed!")
