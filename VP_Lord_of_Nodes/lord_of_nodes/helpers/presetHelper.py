import nuke
import nukescripts


from lord_of_nodes.helpers import configHelper, osHelper


def get_only_modified_by_user_knob_values(node, node_id):
    temp_preset_name = "LORDOFNODES_TEMP_PRESET_NAME2"

    if temp_preset_name in nuke.getUserPresets(node):
        nuke.deleteUserPreset(node_id, temp_preset_name)

    nuke.saveUserPreset(node, temp_preset_name)
    nukescripts.nodepresets.saveNodePresets()

    knobs = nuke.getUserPresetKnobValues(node_id, temp_preset_name)

    nuke.deleteUserPreset(node_id, temp_preset_name)
    nukescripts.nodepresets.saveNodePresets()

    return knobs


def get_node_id(node):
    temp_preset_name = "LORDOFNODES_TEMP_PRESET_NAME3"

    if nuke.saveUserPreset(node, temp_preset_name):
        nukescripts.nodepresets.saveNodePresets()

        file = osHelper.get_nuke_preset_filepath()

        with open(file, 'r') as f:
            for line in f:
                if temp_preset_name in line:
                    node_id = line.split("(")[1]
                    node_id = node_id.split(",")[0]
                    node_id = node_id.replace("'", "").replace('"', '')

                    nuke.deleteUserPreset(node_id, temp_preset_name)
                    nukescripts.nodepresets.saveNodePresets()

                    return node_id
            raise Exception(f"I haven't found line with {temp_preset_name} in {file}")
