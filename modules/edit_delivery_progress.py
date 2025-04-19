from modules import state, print_delivery_progress
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import prompt
import re
import json
import os

def edit_colonisation_progress():
    print("Warning: The delivery list is now automatically synced with in-game data. Manual edits may be overwritten when new journal events are processed.")
    complete = WordCompleter(state.all_comodities, ignore_case=True)
    if not os.path.isfile('Construction_progress.json'):
        print("Error no list detected, please make one first")
    else:
        with open('Construction_progress.json', 'r') as readfile:
            loaded_list = json.load(readfile)
            option = prompt("1- Edit/Add \n2-Remove \n")
            if option == "1":
                key = prompt("Commodity name in all lower case and no spaces: \n", completer=complete, complete_while_typing=True, complete_in_thread=True)
                value = prompt("New amount to deliver: \n")
                key = key.strip()
                value = value.strip()
                key = key.replace(" ", "")
                key = re.sub(r'[^a-zA-Z0-9]', '', key)
                loaded_list[key.lower()] = int(value)
            elif option == "2":
                key = prompt("Commodity name in all lower case and no spaces: \n", completer=complete, complete_while_typing=True, complete_in_thread=True)
                key = key.strip()
                key = key.replace(" ", "")
                key = key.lower()
                key = re.sub(r'[^a-zA-Z0-9]', '', key)
                if key in loaded_list:
                    del loaded_list[key]
                    print(f"{key} removed from list")
                else:
                    print(f"{key} not found")
            else:
                print("Invalid choice. Please enter 'add', 'edit', or 'remove'.")
                edit_colonisation_progress()
        with open('Construction_progress.json', 'w') as writefile:
            json.dump(loaded_list, writefile, indent=4)
        print("done!")
        #print_construction_progress()
        print_delivery_progress.print_construction_progress()