import os
import nukescripts


def get_plugin_path():
    """
    Return application path (Windows Example): "C:/Users/user/.nuke/Python/VP_Lord_of_nodes"
    :return: str
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace("\\", "/")


def get_application_path():
    """
    Return application path (Windows Example): "C:/Users/user/.nuke/Python/VP_Lord_of_nodes/lord_of_nodes"
    :return: str
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")


def get_config_path():
    return os.path.join(get_plugin_path(), "config").replace("\\", "/")


def get_toolset_path(toolset_name=None):
    """
    Return path to our custom toolsets or to given toolset by name
    :param toolset_name: str
    :return: str
    """
    if toolset_name:
        return os.path.join(get_config_path(), "ToolSets", toolset_name + ".nk").replace("\\", "/")
    return os.path.join(get_config_path(), "ToolSets").replace("\\", "/")


def get_icon_path():
    return os.path.join(get_application_path(), "icons").replace("\\", "/")


def get_nuke_preset_filepath():
    return os.path.join(nukescripts.nodepresets.getNukeUserFolder(), "NodePresets", "user_presets.py").replace("\\", "/")
