import requests
import os
import sys
import time
import configparser
import app
from modules import state

def start_app():
    #os.system("python app.py")
    app.start()

def create_autoupdate_file():
    file = open("auto_update.txt", 'w')
    value = "True"
    file.write(value)
    file.close()
    print("Auto-update setting file not found. Creating and setting to True...")
    time.sleep(0.2)
    print("Restarting...")
    time.sleep(0.4)
    python = sys.executable
    os.execv(python, [python] + sys.argv)

def update_version():
    global last_release
    config = configparser.ConfigParser()
    config.read("config.ini")
    auto_update = config["AUTO_UPDATE"]["value"]
    journal_folder = config['JOURNAL_PATH']['path']
    config['JOURNAL_PATH'] = {'path': journal_folder}
    config['AUTO_UPDATE'] = {'value': auto_update}
    config['Version'] = {'version': last_release}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def request_version():
    global REPO
    global last_release
    global CURRENT_VERSION
    version_request = requests.get(REPO)
    api_request_status = version_request.status_code
    if api_request_status == 200:
        print("Api request successful")
        parsed_request = version_request.json()
        last_release = parsed_request.get("tag_name")
        if last_release != CURRENT_VERSION:
            print(f"A new update has released: {last_release}. Please go to https://github.com/Piniat/ED-Construction-helper/releases to download the latest release")
            input("Press enter to continue to app")
            start_app()
        elif last_release == CURRENT_VERSION:
            print("Version is up to date. Starting app...")
            time.sleep(0.4)
            start_app()
    elif api_request_status == 404:
        print("API error. If this continues please report this error to me")
        print("Error", api_request_status)
        time.sleep(0.3)
        print("Trying again in 10 seconds")
        time.sleep(10)
        python = sys.executable
        os.execv(python, [python] + sys.argv)
    elif api_request_status == 403:
        print("Rate limit detected. Skipping update...")
        time.sleep(0.5)
        start_app()
    else:
        if tries < 5:
            print("API error. If this continues please report this error to me")
            print("Error", api_request_status)
            time.sleep(0.3)
            print("Trying again in 10 seconds")
            time.sleep(10)
            tries +=1
            request_version()
        elif tries >= 5:
            print("Too many api errors. Skipping...")
            time.sleep(0.4)
            start_app()

global CURRENT_VERSION
global REPO
global tries
CURRENT_VERSION = "0.6.0-beta"
missing_auto_update = False
missing_version = False
missing_journal = False
tries = 0
VERSION_FILE = "version.txt"
REPO = "https://api.github.com/repos/Piniat/ED-Construction-helper/releases/latest"
if not os.path.isfile('config.ini'):
    path = input("Input game journal file path without quotes:  \n")
    config = configparser.ConfigParser()
    config['JOURNAL_PATH'] = {'path': path}
    config['AUTO_UPDATE'] = {'value': True}
    config['Version'] = {'version': CURRENT_VERSION}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Config file created.")
    time.sleep(1)
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()
if not config.has_section("AUTO_UPDATE"):
    missing_auto_update = True
if not config.has_section("Version"):
    missing_version = True
if not config.has_section("JOURNAL_PATH"):
    missing_journal = True
if missing_version:
    config['Version'] = {'version': CURRENT_VERSION}
if missing_journal:
    path = input("Input game journal file path without quotes:  \n")
    config['JOURNAL_PATH'] = {'path': path}
if missing_auto_update:
    config['AUTO_UPDATE'] = {'value': True}
if missing_auto_update or missing_journal or missing_version:
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
CURRENT_VERSION = config['Version']['version']
AUTO_UPDATE = config["AUTO_UPDATE"]["value"]
if AUTO_UPDATE == "True":
    if CURRENT_VERSION == None:
        print("Error. Version number not found.")
        request_version()
        update_version()
    else:
        request_version()
elif AUTO_UPDATE == "False":
    print("Auto-update disabled. Skipping....")
    time.sleep(0.4)
    start_app()
else:
    print("Key error")
