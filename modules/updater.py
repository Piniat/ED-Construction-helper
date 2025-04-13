import requests
import platform
import os
import time
from prompt_toolkit.shortcuts import ProgressBar
import subprocess
from . import state
import configparser

def update_updater_version():
    print("Updating config.ini with new version...")
    config = configparser.ConfigParser()
    config.read("config.ini")
    auto_update = config["AUTO_UPDATE"]["value"]
    journal_folder = config['JOURNAL_PATH']['path']
    CURRENT_VERSION = config['Version']["version"]
    firstlaunch = config["FIRST_TIME_LAUNCH"]["value"]
    config['JOURNAL_PATH'] = {'path': journal_folder}
    config['AUTO_UPDATE'] = {'value': auto_update}
    config['Version'] = {'version': CURRENT_VERSION}
    config['FIRST_TIME_LAUNCH'] = {'value': firstlaunch}
    config['Updater_version'] = {'version': state.last_updater_release}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def updater_update():
    global user_platform
    global executable
    global executable_name
    user_platform = platform.system().lower()
    if user_platform == 'windows':
        executable = "updater.exe"
        executable_name = executable
    elif user_platform == 'linux':
        executable = "./updater"
        executable_name = "updater"
    else:
        print(f"Unsupported platform. Detected platform: {platform}")
        return
    download_link = f"https://github.com/Piniat/ED-Construction-helper/releases/download/{state.last_updater_release}/{executable_name}"
    filename = executable_name
    print(download_link)
    print(f"Downloading from {download_link}")
    try:
        with requests.get(download_link, stream=True, timeout=10) as download_stream:
            download_stream.raise_for_status()
            total_size = int(download_stream.headers.get('content-length', 0))
            chunk_size = 1024
            with ProgressBar() as pb:
                with open(filename, "wb") as download_file:
                    for chunk in pb(download_stream.iter_content(chunk_size), label="Downloading", total=(total_size // chunk_size)):
                        if chunk:
                            download_file.write(chunk)
            print("Download complete")
            print("Updating updater version in config.ini...")
            update_updater_version()
            time.sleep(0.5)
    except requests.exceptions.HTTPError as http_err:
        print(f"A HTTP error has occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Connection error.")
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except Exception as err:
        print(f"An error occurred: {err}")

def start_extract():
    global executable
    global executable_name
    global user_platform
    if user_platform == 'linux':
        os.chmod(executable_name, 0o755)
    subprocess.Popen([executable], close_fds=True)
    os._exit(0)

def update():
    global user_platform
    global executable
    global executable_name
    user_platform = platform.system().lower()
    if user_platform == 'windows':
        state.user_os = "windows"
        executable = "updater.exe"
        executable_name = executable
    elif user_platform == 'linux':
        state.user_os = "linux"
        executable = "./updater"
        executable_name = "updater"
    else:
        print("Unsupported platform")
        return
    if "updater" in state.last_release:
        updater_update()
    else:
        download_link = f"https://github.com/Piniat/ED-Construction-helper/releases/download/{state.last_release}/{state.user_os}.zip"
        filename = state.user_os + ".zip"
        print(download_link)
        print(f"Downloading from {download_link}")
        try:
            with requests.get(download_link, stream=True, timeout=10) as download_stream:
                download_stream.raise_for_status()
                total_size = int(download_stream.headers.get('content-length', 0))
                chunk_size = 1024
                with ProgressBar() as pb:
                    with open(filename, "wb") as download_file:
                        for chunk in pb(download_stream.iter_content(chunk_size), label="Downloading", total=(total_size // chunk_size)):
                            if chunk:
                                download_file.write(chunk)
                print("Download complete")
        except requests.exceptions.HTTPError as http_err:
            print(f"A HTTP error has occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Connection error.")
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except Exception as err:
            print(f"An error occurred: {err}")
        if not os.path.isfile(executable):
            updater_update()
        start_extract()