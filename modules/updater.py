import requests
import platform
import sys
import os
import time
from prompt_toolkit.shortcuts import ProgressBar
import subprocess
from . import state

def update():
    global platform
    global updater_version
    updater_verion = "v0.1.0-updater"
    platform = platform.system().lower()
    if platform == 'windows':
        state.user_os = "windows"
    elif platform == 'linux':
        state.user_os = "linux"
    else:
        print("Unsupported platform")
        return
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
    if platform == 'windows':
        executable = "updater.exe"
        executable_name = executable
    elif platform == 'linux':
        executable = "./updater"
        executable_name = "updater"
    else:
        print("Unsupported platform")
        return
    print(executable)
    if not os.path.isfile(executable):
        download_link = f"https://github.com/Piniat/ED-Construction-helper/releases/download/{updater_verion}/{executable_name}"
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
        except requests.exceptions.HTTPError as http_err:
            print(f"A HTTP error has occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Connection error.")
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except Exception as err:
            print(f"An error occurred: {err}")
    print("Sleeping for 2 seconds to avoid errors")
    time.sleep(2)
    if platform == 'linux':
        os.chmod(executable, 0o755)
    subprocess.Popen([executable], close_fds=True)
    sys.exit()