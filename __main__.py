import requests
import os
import sys
import time
import configparser
import app
from modules import state, updater, first_time_launch, clean_screen
from prompt_toolkit import prompt

def start_app():
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

def update_version_file():
    print("Updating config.ini with new version...")
    config = configparser.ConfigParser()
    config.read("config.ini")
    auto_update = config["AUTO_UPDATE"]["value"]
    journal_folder = config['JOURNAL_PATH']['path']
    config['JOURNAL_PATH'] = {'path': journal_folder}
    config['AUTO_UPDATE'] = {'value': auto_update}
    config['Version'] = {'version': CURRENT_VERSION}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def request_version():
    global CURRENT_VERSION
    try:
        version_request = requests.get(state.REPO, timeout=4)
    except:
        print("Connection timeout. Skipping...")
        time.sleep(0.5)
        start_app()
    api_request_status = version_request.status_code
    if api_request_status == 200:
        print("Api request successful")
        parsed_request = version_request.json()
        state.last_release = parsed_request.get("tag_name")
        if (state.last_release != CURRENT_VERSION) and (state.last_release != state.updater_verion):
            if "updater "not in state.last_release:
            #print(f"A new update has released: {state.last_release}. Please go to https://github.com/Piniat/ED-Construction-helper/releases to download the latest release")
                update_consent = prompt("Update found. Do you want to download it? y/n \n>")
                if update_consent == "y":
                    updater.update()
                    print("Update complete. Please restart the app...")
                    time.sleep(1)
                    app.exit_app
                elif update_consent == "n":
                    print("Skipping update...")
                    start_app()
                else:
                    print("invalid option. starting app...")
                    start_app()
            else:
                update_consent = prompt("Updater update found. Do you want to download it? y/n \n>")
                if update_consent == "y":
                    updater.updater_update()
                    print("Update complete. Please restart the app...")
                    time.sleep(1)
                    app.exit_app
                elif update_consent == "n":
                    print("Skipping update...")
                    start_app()
                else:
                    print("invalid option. starting app...")
                    start_app()
        elif state.last_release == CURRENT_VERSION:
            print("Version is up to date. Starting app...")
            time.sleep(0.4)
            start_app()
    elif api_request_status == 404:
        print("API error. If this continues please report this error to me")
        print("Error", api_request_status)
        time.sleep(0.3)
        print("Trying again in 10 seconds")
        time.sleep(10)
        request_version()
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
global tries
CURRENT_VERSION = "v0.7.0-rc3"
state.current_version = CURRENT_VERSION
global Stored_version
missing_auto_update = False
missing_version = False
missing_journal = False
missing_first_launch = False
tries = 0
if not os.path.isfile('config.ini'):
    path = input("Input game journal file path without quotes:  \n")
    config = configparser.ConfigParser()
    config['JOURNAL_PATH'] = {'path': path}
    config['AUTO_UPDATE'] = {'value': True}
    config['Version'] = {'version': CURRENT_VERSION}
    config['FIRST_TIME_LAUNCH'] = {'value': True}
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
if not config.has_section("FIRST_TIME_LAUNCH"):
    missing_first_launch = True
if missing_version:
    config['Version'] = {'version': CURRENT_VERSION}
if missing_journal:
    path = input("Input game journal file path without quotes:  \n")
    config['JOURNAL_PATH'] = {'path': path}
if missing_auto_update:
    config['AUTO_UPDATE'] = {'value': True}
if missing_first_launch:
    config['FIRST_TIME_LAUNCH'] = {'value': True}
if missing_auto_update or missing_journal or missing_version or missing_first_launch:
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
        config.read('config.ini')
        config.sections()
Stored_version = config['Version']['version']
if Stored_version != CURRENT_VERSION:
    update_version_file()
else:
    CURRENT_VERSION = config['Version']['version']
first_launch = config["FIRST_TIME_LAUNCH"]['value']
if first_launch == "True":
    clean_screen.clear_screen()
    first_time_launch.onboarding()
AUTO_UPDATE = config["AUTO_UPDATE"]["value"]
if AUTO_UPDATE == "True":
    if CURRENT_VERSION == None:
        print("Error. Version number not found.")
        request_version()
        update_version_file()
    else:
        request_version()
elif AUTO_UPDATE == "False":
    print("Auto-update disabled. Skipping....")
    time.sleep(0.4)
    start_app()
else:
    print("Key error")
