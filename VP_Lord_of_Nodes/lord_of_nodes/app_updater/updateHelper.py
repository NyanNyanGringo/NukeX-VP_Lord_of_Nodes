import nuke
import os
import re
import shutil
import subprocess
import webbrowser
import tempfile
import time
import zipfile

from PySide2.QtWidgets import QAction

from lord_of_nodes.app_updater import update_config


# GET PATHS and NAMES
def get_application_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_plugin_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_application_name():
    return os.path.basename(get_application_path())


def get_plugin_path_name():
    return os.path.basename(get_plugin_path())


def get_nuke_executable_path():
    """Return something like: C:/Program Files/Nuke13.2v6/Nuke13.2.exe"""
    nuke_executable_path = nuke.env["ExecutablePath"].replace("\\", "/")

    # if os.path.exists(nuke_executable_path):
    #     return nuke_executable_path

    nuke_folder_path = os.path.dirname(nuke.env["NukeLibraryPath"])  # try other way to find nuke path
    nuke_executable_filename = os.path.basename(nuke_executable_path)  # get name of nuke app
    nuke_executable_path = os.path.join(nuke_folder_path, nuke_executable_filename).replace("\\", "/")

    if os.path.exists(nuke_executable_path):
        return nuke_executable_path

    raise Exception(f"Nuke executable path {nuke_executable_path} doesn't exists!")


def get_nuke_folder_path():
    """Return something like: C:/Program Files/Nuke13.2v6"""
    return os.path.dirname(get_nuke_executable_path())


def get_nuke_python_path():
    python_file_name = None
    if nuke.env["WIN32"]:
        python_file_name = "python.exe"
    elif nuke.env["MACOS"]:
        python_file_name = "python"
    elif nuke.env["LINUX"]:
        for file in [f for f in os.listdir(get_nuke_folder_path()) if os.path.isfile(os.path.join(get_nuke_folder_path(), f))]:
            if re.fullmatch(f"python[0-9]+.[0-9]+", file):
                python_file_name = file
                break

    return os.path.join(get_nuke_folder_path(), python_file_name).replace("\\", "/")


def get_github_username():
    return update_config.github_username


def get_github_repository_name():
    return update_config.github_repository


# VERSIONING


def get_application_version():
    for file_name in os.listdir(get_application_path()):
        if re.fullmatch(r"v\d+.\d+.\d+", file_name):
            return file_name


def check_new_version_available(current_version, last_version) -> bool:
    current_parts = current_version[1:].split('.')
    last_parts = last_version[1:].split('.')

    for current, last in zip(current_parts, last_parts):
        if int(current) < int(last):
            return True
        elif int(current) > int(last):
            return False

    return False  # Both versions are equal


# HELP METHODS


def unzip(zip_file_path: str, delete_zip: int = False) -> str:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_file_path))

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        files_inside = zip_ref.namelist()

    if delete_zip:
        os.remove(zip_file_path)

    return os.path.join(os.path.dirname(zip_file_path), files_inside[0]).replace("\\", "/")


def correct_path_to_console_path(input_path: str) -> str:
    path_corrected = str()
    for path_part in input_path.replace("\\", r'/').split("/"):
        if " " in path_part:
            path_corrected += f'"{path_part}"/'
            continue
        path_corrected += f'{path_part}/'

    if path_corrected[-1] == "/":
        path_corrected = path_corrected[:-1]

    return path_corrected


def run_terminal_command(command: str, cwd: str = None) -> None:
    if nuke.env["WIN32"]:
        script = ['start', 'cmd', '/k', command]
        use_shell = True

    elif nuke.env["MACOS"]:
        script = f'osascript -e \'tell application "Terminal" to do script "{command}"\''
        # command += f"""&& osascript -e 'tell application "Terminal" to close first window'""" close macOS terminal
        use_shell = True

    else:
        script = ['x-terminal-emulator', '-e', command]
        use_shell = False

    if cwd:
        subprocess.Popen(script, shell=use_shell, cwd=cwd)
    else:
        subprocess.Popen(script, shell=use_shell)


def open_application_github_in_web():
    webbrowser.open(f"https://github.com/{get_github_username()}/{get_github_repository_name()}")


def ask_error_message(reason: str):
    message = f"""
My Lord,
I can't update VP_LittleHelpers - {reason}

Be sure:
1. You are connected to the internet;
2. Nuke Python and Terminal not blocked by FireWall;

Do you want to update manually?
"""
    if nuke.ask(message):
        open_application_github_in_web()


# RESTART NUKE


def open_nuke_in_new_terminal(script_path=None):
    """
    Opens NukeX or NukeStudio in new terminal
    :param script_path: string, path to script for open
    :return: None
    """
    command = ""

    # change disk if Windows
    if script_path and nuke.env["WIN32"]:
        command += script_path.replace("\\", "/").split("/")[0] + " & "

    # change dir to script dir
    if script_path:
        command += "cd " + correct_path_to_console_path(os.path.dirname(script_path)) + " & "

    # set nuke executable path
    command += correct_path_to_console_path(get_nuke_executable_path())

    # set sys args that nuke has
    for arg in nuke.rawArgs:
        if arg == nuke.rawArgs[0]:  # first arg is nuke executable we already have it
            continue
        command += " " + arg

    # set scriptn file name to open
    if script_path:
        command += " " + os.path.basename(script_path)

    # exit terminal after execute nuke
    command += " && exit"

    # get script directory
    if script_path:
        cwd = os.path.dirname(script_path)
    else:
        cwd = None

    run_terminal_command(command, cwd=cwd)


def restart_any_nuke():
    """
    Restart NukeX or NukeStudio (support script reopening)
    :return: None
    """
    script_path = nuke.Root().name()

    if script_path == "Root":
        open_nuke_in_new_terminal()
    else:
        open_nuke_in_new_terminal(script_path=script_path)
        nuke.scriptSave(script_path)

    nuke.scriptExit()


# REPOSITORY


def get_data_from_last_repository_release(data: str):
    """
    :param data: "zipball_url" -> get URL to download last release (str: "https://api.github.com/...")
                 "tag_name" -> get last release version (str: v0.0.0)
                 "body" -> get info about updates - what was done in this release (str)
    :param repository: repository to search release
    """
    url = f"https://api.github.com/repos/{get_github_username()}/{get_github_repository_name()}/releases/latest"
    python_path = get_nuke_python_path()
    python_code = f'''
import urllib.request
import json
import ssl

# Add SSH certificate permission (without this doesn't work on macOS)
ssl._create_default_https_context = ssl._create_unverified_context

url = "{url}"
response = urllib.request.urlopen(url)
data = json.loads(response.read())
zipball_url = data["{data}"]

print(zipball_url)
    '''

    if update_config.use_test_mode:
        print(f"url: {url}")
        print(f"python_path: {python_path}")
        print(f"python_code: {python_code}")

    result = subprocess.run([python_path, '-c', python_code], capture_output=True, text=True)
    result = result.stdout.strip()

    if not result and not data == "body":
        raise Exception("Something went wrong while getting data...")
    return result


def download_repository_by_url(url) -> str:
    temppath = tempfile.gettempdir()
    repository_user = url.replace("\\", "/").split("/")[-4]
    repository_name = url.replace("\\", "/").split("/")[-3]
    repository_version = url.replace("\\", "/").split("/")[-1]

    # delete previous temp files if exists
    for file in os.listdir(temppath):
        items = [repository_user, repository_name, repository_version]
        if all([(item in file) for item in items]):
            file_path = os.path.join(temppath, file).replace("\\", "/")
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)

    # download
    # cd to change dir | curl to download
    download_command = f"cd {correct_path_to_console_path(temppath)} && curl -LJO -k {url} && exit"

    if update_config.use_test_mode:
        print(f"Try to run command: {download_command}")

    run_terminal_command(download_command)

    # find files after download
    for x in range(22):
        time.sleep(1)
        for file in os.listdir(temppath):
            items = [repository_user, repository_name, repository_version]
            if all([(item in file) for item in items]):
                return os.path.join(temppath, file).replace("\\", "/")

    raise Exception(f"Something went wrong while downloading file by {url}!")


# MAIN


def start_updating_application_when_initiazile(action):
    def do():
        current_version = get_application_version()
        last_version = get_data_from_last_repository_release("tag_name")

        if update_config.use_test_mode:
            current_version = "v0.0.0"

        if check_new_version_available(current_version, last_version):

            action.setText(f"Update {get_plugin_path_name()} from {current_version} to {last_version}")
            # nuke.message(f"Available update for VP_LittleHelpers from {current_version} to {last_version}! ^_^")

    if update_config.use_test_mode:
        do()
        return

    try:
        do()
    except:
        pass


def start_updating_application_when_trigger():
    # get application version
    current_version = get_application_version()
    if not current_version:
        nuke.message(f"I can't find version file in {get_application_path()}!")
        return

    if update_config.use_test_mode:
        current_version = "v0.0.0"
        print(f"current_version: {current_version}")

    # get last release version
    last_version = str()
    if update_config.use_test_mode:
        last_version = get_data_from_last_repository_release("tag_name")
        print(f"last_version: {last_version}")
    else:
        try:
            last_version = get_data_from_last_repository_release("tag_name")
        except:
            ask_error_message("can't check last release version.")
            return

    # get last release download URL
    download_url = str()
    if update_config.use_test_mode:
        download_url = get_data_from_last_repository_release("zipball_url")
        print(f"download_url: {download_url}")
    else:
        try:
            download_url = get_data_from_last_repository_release("zipball_url")
        except:
            ask_error_message("can't get url to download last release.")
            return
    # body
    release_update_info = str()
    if update_config.use_test_mode:
        release_update_info = get_data_from_last_repository_release("body")
        print(f"release_update_info: {release_update_info}")
    else:
        try:
            release_update_info = get_data_from_last_repository_release("body")
        except:
            ask_error_message("can't get update information (what's new in release).")
            return

    # compare versions
    if check_new_version_available(current_version, last_version):
        # ask to download
        if nuke.ask(f"My Lord,\n\n{get_plugin_path_name()}_{last_version} available!\n\nUpdate?"):

            # download and get zip of last release
            zip_path = str()
            if update_config.use_test_mode:
                zip_path = download_repository_by_url(download_url)
                print(f"zip_path: {zip_path}")
            else:
                try:
                    zip_path = download_repository_by_url(download_url)
                except:
                    ask_error_message("can't download last release .zip file from GitHub.")
                    return

            # unzip
            unzip_path = unzip(zip_path, delete_zip=True)

            # get paths
            new_program_path = os.path.join(unzip_path, get_plugin_path_name(), get_application_name()).replace("\\", "/")
            old_program_path = get_application_path().replace("\\", "/")

            if update_config.use_test_mode:
                old_program_path += " (TEST MODE)"
                print(f"unzip_path: {unzip_path}")
                print(f"new_program_path: {new_program_path}")
                print(f"old_program_path: {old_program_path}")

            if update_config.use_test_mode:
                if os.path.exists(old_program_path):
                    shutil.rmtree(old_program_path)
                shutil.move(new_program_path, old_program_path)
            else:
                try:
                    if os.path.exists(old_program_path):
                        shutil.rmtree(old_program_path)
                    shutil.move(new_program_path, old_program_path)
                except FileNotFoundError:
                    ask_error_message(f"path to move/replace doesn't exists: {new_program_path}.")
                    return
                except Exception:
                    ask_error_message(f"can't move {new_program_path} to {old_program_path}.")
                    return
                finally:
                    pass

            # ask to restart Nuke
            release_update_info = release_update_info.replace(r"\n", "").replace(r"\r", "")
            release_update_info = "- ".join(release_update_info.split("#"))
            message = f"""
My Lord, update finished successfully!

New in {get_plugin_path_name()}_{last_version}:
{release_update_info}

Restart Nuke?
            """
            if nuke.ask(message):
                restart_any_nuke()

    else:
        nuke.message(f"My Lord,\n\nYou have the latest version of {get_plugin_path_name()} ^_^")
        return


# SET UP ACTION


def add_update_action_to_menu(menu):
    # create action
    action = QAction(f"Check {get_plugin_path_name()} updates...")

    # add action to menu
    menu.addAction(action)

    # set up action
    action.triggered.connect(start_updating_application_when_trigger)

    return action
