import requests
import os
import time
import configparser
from modules import state, updater, exit_app, error_logger, message_box, yes_and_no_prompt_box
from prompt_toolkit import prompt
from PySide6.QtWidgets import QFileDialog

def start_app():
    return

def update_version_file():
    #print("Updating config.ini with new version...")
    state.msg_box_contents = "Updating config.ini with new version..."
    state.msg_box_close_time = 300
    message_box.message_box()
    config = configparser.ConfigParser()
    config.read("config.ini")
    auto_update = config["AUTO_UPDATE"]["value"]
    journal_folder = config['JOURNAL_PATH']['path']
    updater_version = config['Updater_version']["version"]
    firstlaunch = config["FIRST_TIME_LAUNCH"]["value"]
    config['JOURNAL_PATH'] = {'path': journal_folder}
    config['AUTO_UPDATE'] = {'value': auto_update}
    config['Version'] = {'version': CURRENT_VERSION}
    config['FIRST_TIME_LAUNCH'] = {'value': firstlaunch}
    config['Updater_version'] = {'version': updater_version}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def request_version():
    global CURRENT_VERSION
    try:
        version_request = requests.get(state.REPO_ALL, timeout=4)
    except:
        #print("Connection timeout. Skipping...")
        state.msg_box_contents = "Connection timeout. Skipping..."
        state.msg_box_close_time = 500
        message_box.message_box()
        #time.sleep(0.5)
        start_app()
    api_request_status = version_request.status_code
    if api_request_status == 200:
        tries = 0
        #print("Api request successful")
        state.msg_box_contents = "Api request successful"
        state.msg_box_close_time = 300
        message_box.message_box()
        parsed_request = version_request.json()
        state.last_release = parsed_request[0].get("tag_name")
        #check for latest updater version
        updater_releases = []
        for release in parsed_request:
            if "-updater" in release.get("tag_name"):
                updater_releases.append(release.get("tag_name"))
        state.last_updater_release = updater_releases[0]
        if state.last_release != CURRENT_VERSION:
        #print(f"A new update has released: {state.last_release}. Please go to https://github.com/Piniat/ED-Construction-helper/releases to download the latest release")
            #update_consent = prompt("Update found. Do you want to download it? y/n \n>")
            state.msg_box_contents = "Update found. Do you want to download it?"
            yes_and_no_prompt_box.prompt_box()
            if state.msg_box_response == "y":
                state.msg_box_response = None
                updater.update()
                #print("Update complete. Please restart the app...")
                #state.msg_box_contents = "Update complete. Please restart the app..."
                #state.msg_box_close_time = 1000
                #message_box.message_box()
                #exit_app.close_app()
            elif state.msg_box_response == "n":
                state.msg_box_response = None
                #print("Skipping update...")
                state.msg_box_contents = "Skipping update..."
                state.msg_box_close_time = 500
                message_box.message_box()
                if state.last_updater_release == state.updater_verion:
                    start_app()
            else:
                print("invalid option. starting app...")
                start_app()
        if state.last_updater_release != state.updater_verion:
            state.msg_box_contents = "Updater update found. Do you want to download it?"
            yes_and_no_prompt_box.prompt_box()
            if state.msg_box_response == "y":
                state.msg_box_response = None
                updater.updater_update()
                #state.msg_box_contents = "Update complete. Please restart the app..."
                #state.msg_box_close_time = 1000
                #message_box.message_box()
                exit_app.close_app()
            elif state.msg_box_response == "n":
                state.msg_box_response = None
                state.msg_box_contents = "Skipping updater update..."
                state.msg_box_close_time = 500
                message_box.message_box()
                start_app()
            else:
                #print("invalid option. starting app...")
                start_app()
        if state.last_release == CURRENT_VERSION:
            #print("Version is up to date. Starting app...")
            state.msg_box_contents = "Version is up to date. Starting app..."
            state.msg_box_close_time = 400
            message_box.message_box()
            start_app()
    elif (api_request_status == 404) and tries < 5:
        #print("API error. If this continues please report this error to me")
        #print("Error", api_request_status)
        api_error_message = "API error: " + str(api_request_status) + "\nTrying again in 5 seconds"
        state.msg_box_contents = api_error_message
        state.msg_box_close_time = 5000
        message_box.message_box()
        #print("Trying again in 5 seconds")
        #time.sleep(5)
        tries += 1
        request_version()
    elif api_request_status == 403:
        #print("Rate limit detected. Skipping update...")
        state.msg_box_contents = "Rate limit detected. Skipping update..."
        state.msg_box_close_time = 500
        message_box.message_box()
        #time.sleep(0.5)
        start_app()
    else:
        if tries < 5:
            #print("API error.")
            #print("Error", api_request_status)
            api_error_message = "API error: " + str(api_request_status) + "\nTrying again in 5 seconds"
            state.msg_box_contents = api_error_message
            state.msg_box_close_time = 5000
            message_box.message_box()
            tries +=1
            request_version()
        elif tries >= 5:
            state.msg_box_contents = "Too many API errors. Skipping..."
            state.msg_box_close_time = 1000
            message_box.message_box()
            start_app()

def begin_checks(self):
    try:
        global CURRENT_VERSION
        global tries
        #App version for displaying and version check
        CURRENT_VERSION = "v2.0.0-beta"
        #ignore updates for dev version
        dev_version = False
        state.current_version = CURRENT_VERSION
        global Stored_version
        missing_auto_update = False
        missing_version = False
        missing_journal = False
        missing_first_launch = False
        missing_updater_version = False
        tries = 0
        if not os.path.isfile('config.ini'):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            path = QFileDialog.getExistingDirectory(None, "Select journal directory", options=options)
            config = configparser.ConfigParser()
            config['JOURNAL_PATH'] = {'path': path}
            config['AUTO_UPDATE'] = {'value': "True"}
            config['Version'] = {'version': CURRENT_VERSION}
            config['FIRST_TIME_LAUNCH'] = {'value': "True"}
            config['Updater_version'] = {'version': "None"}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            #print("Config file created.")
            state.msg_box_contents = "Config file created."
            state.msg_box_close_time = 500
            message_box.message_box()
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
        if not config.has_section("Updater_version"):
            missing_updater_version = True
        if missing_version:
            config['Version'] = {'version': CURRENT_VERSION}
        if missing_journal:
            path = input("Input game journal file path without quotes:  \n")
            config['JOURNAL_PATH'] = {'path': path}
        if missing_auto_update:
            config['AUTO_UPDATE'] = {'value': "True"}
        if missing_first_launch:
            config['FIRST_TIME_LAUNCH'] = {'value': "True"}
        if missing_updater_version:
            config['Updater_version'] = {'version': ""}
        if missing_auto_update or missing_journal or missing_version or missing_first_launch or missing_updater_version:
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
                config.read('config.ini')
                config.sections()
        state.updater_verion = config["Updater_version"]["version"]
        Stored_version = config['Version']['version']
        if Stored_version != CURRENT_VERSION:
            update_version_file()
        else:
            CURRENT_VERSION = config['Version']['version']
        first_launch = config["FIRST_TIME_LAUNCH"]['value']
        #if first_launch == "True":
        #    #clean_screen.clear_screen()
        #    first_time_launch.onboarding()
        AUTO_UPDATE = config["AUTO_UPDATE"]["value"]
        if (AUTO_UPDATE == "True") and (dev_version == False):
            if CURRENT_VERSION == None:
                #print("Error. Version number not found.")
                request_version()
                update_version_file()
            else:
                request_version()
        elif (AUTO_UPDATE == "False") or (dev_version == True):
            #print("Auto-update disabled. Skipping....")
            state.msg_box_contents = "Auto-update disabled. Skipping...."
            state.msg_box_close_time = 400
            message_box.message_box()
            #time.sleep(0.4)
            start_app()
        else:
            #print("Key error")
            state.msg_box_contents = "Key error. \n(something has gone terribly wrong with config.ini)"
            state.msg_box_close_time = 1000
            message_box.message_box()
    except:
        error_logger.log_file_error()