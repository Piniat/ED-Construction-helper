from . import exit_app, edit_delivery_progress, edit_shopping_list, state, ship_cargo_ask
from prompt_toolkit import prompt
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style
import time
import os
import sys

style = Style.from_dict({
    "":          "#ff0066",
    "iwarning":  "#ff0000",
})

def user_input():
    command_list = WordCompleter(["help", "app-mode-1", "app-mode-2", "app-mode-3", "override-docked", "override-docked-construction", "edit-shopping-list", "edit-delivery-progress", "edit-ship-cargo", "exit", "reset-progress", "delivery-tracker", "shopping-list"], ignore_case=True)
    while True:
        with patch_stdout():
            usr_input = prompt("> ", cursor=CursorShape.BLINKING_BLOCK, completer=command_list, complete_while_typing=True, complete_in_thread=True)
            if usr_input == "exit":
                print("Exiting program...")
                time.sleep(1)
                exit_app.close_app()
            elif usr_input == "help":
                print("List of commands: \n exit - exits the program \n delivery-tracker - switches to construction delivery tracking \n shopping-list - switches to app to shopping list mode \n app-mode-3 - switches app to journal monitoring mode \n edit-shopping-list - allows you to edit shopping list \n edit-delivery-progress - allows you to edit the delivery progress list, \n reset-progress - deletes shopping list or construction progress allowing you to start from stratch \n override-docked - overrides docked status in mode 3 \n override-docked-construction - overrides if you are docked at a constructions site / megaship (any cargo removed from your hold will be counted towards progress to buiding) \n edit-ship-cargo")
            elif (usr_input == "app-mode-1") or (usr_input == "delivery-tracker"):
                state.switched = True
                state.just_started = False
                state.app_mode = "1"
                print("Switched to construction progress tracking.")
            elif (usr_input == "app-mode-2") or (usr_input == "shopping-list"):
                state.switched = True
                state.just_started = False
                state.initialized = False
                state.app_mode = "2"
                print("Switched to shopping list tracking")
            elif usr_input == "app-mode-3":
                state.switched = True
                state.just_started = False
                state.app_mode = "3"
                print("Switched to journal logging mode")
            elif usr_input == "override-docked":
                print("Current status: ", state.ship_docked)
                status = prompt("Are you docked? y/n \n> ")
                if status == "y":
                    state.ship_docked = True
                    print("Current status: ", state.ship_docked)
                elif status == "n":
                    state.ship_docked == False
                    print("Current status: ", state.ship_docked)
                else:
                    print("Error. Please choose y or n")
            elif usr_input == "override-docked-construction":
                print("Current status: ", state.docked_at_construction)
                state_colon = prompt("Are you docked at a place where colonisation contributions are accepted? y/n \n> ")
                if state_colon == "y":
                    state.docked_at_construction = True
                    print("Current status: ", state.docked_at_construction)
                elif state_colon == "n":
                    state.docked_at_construction = False
                    print("Current status: ", state.docked_at_construction)
                else:
                    print("Error. Please choose y or n")
            elif usr_input == "edit-shopping-list":
                edit_shopping_list.edit_list()
            elif usr_input == "edit-delivery-progress":
                    edit_delivery_progress.edit_colonisation_progress()
            elif usr_input == "edit-ship-cargo":
                ship_cargo_ask.request_ship_cargo()
                print("Updated ship cargo space")
            elif usr_input == "reset-progress":
                autocomplete = WordCompleter(["Shopping", "Delivery", "both"], ignore_case=True)
                which = prompt("Do you want to delete the commodity shopping list, colonisation delivery list or both?\n 1-Shopping list \n 2-Delivery tracker \n 3-both \n exit \n> ", completer=autocomplete, complete_while_typing=True, complete_in_thread=True)
                if which == "1":
                    sure = prompt(f"Are you sure? THIS CANNOT BE UNDONE! Continue anyway? y/n \n>", style=style)
                    if sure == "y":
                        try:
                            os.remove("progress.json")
                            print("File removed!")
                            print("Restarting...")
                            time.sleep(0.5)
                            python = sys.executable
                            os.execv(python, [python] + sys.argv)
                        except:
                            print("Error. File not found")
                    elif sure == "n":
                        print("Operation cancelled")
                    else:
                        print("Invalid option. Cancelling...")
                elif which == "2":
                    sure = prompt(f"Are you sure? THIS CANNOT BE UNDONE! Continue anyway? y/n \n>", style=style)
                    if sure == "y":
                        try:
                            os.remove("Construction_progress.json")
                            print("File removed!")
                            print("Restarting...")
                            time.sleep(0.5)
                            python = sys.executable
                            os.execv(python, [python] + sys.argv)
                        except:
                            print("Error. File not found")
                    elif sure == "n":
                        print("Operation cancelled")
                    else:
                        print("Invalid option. Cancelling...")
                elif which == "3":
                    sure = prompt(f"Are you sure? THIS CANNOT BE UNDONE! Continue anyway? y/n \n>", style=style)
                    if sure == "y":
                        try:
                            os.remove("Construction_progress.json")
                            os.remove("progress.json")
                            print("Files removed!")
                            print("Restarting...")
                            time.sleep(0.5)
                            python = sys.executable
                            os.execv(python, [python] + sys.argv)
                        except:
                            print("Error. File not found")
                    elif sure == "n":
                        print("Operation cancelled")
                    else:
                        print("Invalid option. Cancelling...")
                elif which == "exit":
                    print("Cancelled!")
                else:
                    print("Invalid option")
            #elif usr_input == "debug":
            #    print_construction_progress()
            else:
                print('Error. Invalid command. Type "help" for a list of commands')