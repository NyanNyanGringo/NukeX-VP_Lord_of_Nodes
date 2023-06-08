import os.path
import shutil

import nuke
import nukescripts

from lord_of_nodes.helpers import osHelper, filesHelper


def cleanup_user_presets_py(temp_preset_name):
    preset_path = osHelper.get_nuke_preset_path()
    preset_filepath = osHelper.get_nuke_preset_filepath()

    # check user_presets.py exist
    if not os.path.exists(preset_path) or not os.path.exists(preset_filepath):
        return

    # open file and delete strings
    new_lines = filesHelper.delete_lines_that_contains_string_from_filepath(preset_filepath, temp_preset_name)

    # if "nuke.setUserPreset(" still in file user_presets.py --> return
    if "nuke.setUserPreset(" in str(new_lines):
        return

    # if no user files inside .nuke/NodePresets --> delete folder
    nuke_files = ["user_presets.py", "user_presets.pyc", "__init__.py", "__pycache__"]

    if not [f for f in os.listdir(preset_path) if f not in nuke_files]:
        try:
            shutil.rmtree(preset_path)
        except:
            pass


def get_only_modified_by_user_knob_values(node, node_id):
    """
    Using Nuke Presets API gets modified knob values of node that
    will be written to Knob Defaults
    """
    temp_preset_name = "LORDOFNODES_TEMP_PRESET_NAME2"

    if temp_preset_name in nuke.getUserPresets(node):
        nuke.deleteUserPreset(node_id, temp_preset_name)

    nuke.saveUserPreset(node, temp_preset_name)
    nukescripts.nodepresets.saveNodePresets()

    knobs = nuke.getUserPresetKnobValues(node_id, temp_preset_name)

    nuke.deleteUserPreset(node_id, temp_preset_name)
    nukescripts.nodepresets.saveNodePresets()

    cleanup_user_presets_py(temp_preset_name)

    return knobs


def get_node_id(node):
    """
    Using Nuke Presets API gets node unique ID
    """
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

                    cleanup_user_presets_py(temp_preset_name)

                    return node_id

            cleanup_user_presets_py(temp_preset_name)
            raise Exception(f"I haven't found line with {temp_preset_name} in {file}")
