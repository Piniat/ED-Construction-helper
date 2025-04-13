from prompt_toolkit import prompt
from prompt_toolkit.cursor_shapes import CursorShape
import configparser
import time
from . import clean_screen

def onboarding():
    first = prompt("Is this your first time using the app? y/n \n>", cursor=CursorShape.BLINKING_BLOCK).strip().lower()
    if first == "n":
        update_config()
        time.sleep(1)
    elif first == "y":
        print("\nUnderstood. Welcome to the Elite Dangerous Construction helper app. \n")
        continue_onboarding()
        print("This apps goal is to help you with tracking how many commodities are left to deliver or buy for your shiny new station, settlement or other building \n")
        continue_onboarding()
        print("Currently the app only features this TUI so you will need to use commands to navigate it. \n")
        continue_onboarding()
        print('The most important command will be "help". This will print out a list of all the commands that you can use at any time \n')
        continue_onboarding()
        print('"edit-delivery-progress" and "edit-shopping-list" will allow you to edit the delivery progress list and shopping list respectively \n')
        continue_onboarding()
        print('"edit-ship-cargo" will allow you to change the cargo space used to calculate remaining deliveries (eg. if you change ships or input the wrong amount) \n')
        continue_onboarding()
        print('"reset-progress" will allow you to delete your shopping and/or delivery lists. Useful for when you finish a construction \n')
        continue_onboarding()
        print('"exit" this will allow you to exit the app in most areas of the app (some areas might require you to close the window to close the app) \n')
        continue_onboarding()
        print("Ok, I think that's all of the more important ones. Before you go please remember to report any bugs/errors and crashes you find on github, it really can help me fix them faster. I'm also open to suggestions. Anyways, have fun hauling CMDR! \n")
        continue_onboarding()
        print("Continuing app startup...")
        update_config()
        time.sleep(2)
    else:
        print("Error. Please input y or n")
        time.sleep(1)
        onboarding()

def continue_onboarding():
    prompt("(Press enter to continue)")
    clean_screen.clear_screen()

def update_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    auto_update = config["AUTO_UPDATE"]["value"]
    journal_folder = config['JOURNAL_PATH']['path']
    app_version = config['Version']['version']
    updater_version = config['Updater_version']["version"]
    config['JOURNAL_PATH'] = {'path': journal_folder}
    config['AUTO_UPDATE'] = {'value': auto_update}
    config['Version'] = {'version': app_version}
    config['FIRST_TIME_LAUNCH'] = {'value': False}
    config['Updater_version'] = {'version': updater_version}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
