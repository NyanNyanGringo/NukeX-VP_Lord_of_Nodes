"""
Library to work with config-files .json

"""


import json
import os


from lord_of_nodes.helpers import osHelper


def get_user_config_path():
    """
    Get default user config path for HotKey Manager
    :
    :rtype: str
    """
    return os.path.join(osHelper.get_config_path(), "hotkey_manager_config.json").replace("\\", "/")


def write_configs(keys, confs, conf_file_path=get_user_config_path()):
    """
    Write values to config-file as key-value
    :
    :param keys: list | dict of str
    :param confs: list | dict of str
    :param conf_file_path: str
    :
    :rtype: bool
    """
    config_data = dict()

    if len(keys) != len(confs):
        raise Exception("Different length of keys and values!")

    if os.path.isfile(conf_file_path):
        f = open(conf_file_path, mode='r')
        config_data = json.load(f)
        f.close()

    i = 0
    for key in keys:
        config_data[key] = confs[i]
        i += 1

    f = open(conf_file_path, mode='w')
    json.dump(config_data, f, indent=2, sort_keys=True)
    f.close()

    return True


def write_config(key, conf, conf_file_path=get_user_config_path()):
    """
    Write value to config-file as key-value
    :
    :param key: str
    :param conf: any
    :param conf_file_path: str
    :
    :rtype: bool
    """
    config_data = dict()

    if os.path.isfile(conf_file_path):
        f = open(conf_file_path, mode='r')
        config_data = json.load(f)
        f.close()

    config_data[key] = conf

    f = open(conf_file_path, mode='w')
    json.dump(config_data, f, indent=2, sort_keys=True)
    f.close()

    return True


def read_config(conf_file_path=get_user_config_path()):
    """
    Read all from config file
    :
    :param conf_file_path: str
    :
    :rtype: dict
    """

    if not os.path.isfile(conf_file_path):
        raise Exception("Config " + conf_file_path + " doesn't exists!")

    f = open(conf_file_path, mode='r')
    config_data_input = json.load(f)
    f.close()

    return config_data_input


def read_config_key(key, conf_file_path=get_user_config_path()):
    """
    Read value by the config key
    :
    :param key: any
    :param conf_file_path: str
    :
    :rtype: any
    """

    if not check_key(key, conf_file_path):
        raise Exception("Config " + conf_file_path + " or key " + key + " doesn't exists!")

    f = open(conf_file_path, mode='r')
    config_data_input = json.load(f)
    f.close()

    return config_data_input[key]


def check_key(key, conf_file_path=get_user_config_path()):
    """
    Check if config file exists and has key
    :
    :param key: any
    :param conf_file_path: str
    :
    :rtype: bool
    """

    if not os.path.isfile(conf_file_path):
        return False

    f = open(conf_file_path, mode='r')
    config_data_input = json.load(f)
    f.close()

    if key in config_data_input.keys():
        return True
    else:
        return False


def delete_key(key, conf_file_path=get_user_config_path()):
    """
    Delete key, and it's value from config file
    :
    :param key: any
    :param conf_file_path: str
    :
    :rtype: bool
    """

    if check_key(key, conf_file_path):
        f = open(conf_file_path, mode='r')
        config_data = json.load(f)
        f.close()

        del config_data[key]

        f = open(conf_file_path, mode='w')
        json.dump(config_data, f, indent=2, sort_keys=True)
        f.close()
        return True
    return False


def check_config_exists_else_create_it(conf_file_path=get_user_config_path()):
    if not os.path.isfile(conf_file_path):
        write_config("TEMP_KEY", "TEMP_VALUE")
        delete_key("TEMP_KEY")
