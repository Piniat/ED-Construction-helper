from modules import state, print_shopping_list
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import prompt
import json
import re
import os

def edit_list():
    complete = WordCompleter(state.all_comodities, ignore_case=True)
    if not os.path.isfile('progress.json'):
        print("Error no list detected, please make one first")
    else:
        with open('progress.json', 'r') as readfile:
            loaded_list = json.load(readfile)
            option = prompt("1- Edit/Add \n2-Remove \n")
            if option == "1":
                key = prompt("Commodity name in all lower case and no spaces: \n", completer=complete, complete_while_typing=True, complete_in_thread=True)
                value = prompt("New amount needed: \n")
                key = key.strip()
                value = value.strip()
                key = key.replace(" ", "")
                key = re.sub(r'[^a-zA-Z0-9]', '', key)
                loaded_list[key.lower()] = int(value)
            elif option == "2":
                key = prompt("Commodity name in all lower case and no spaces: \n", completer=complete, complete_while_typing=True, complete_in_thread=True)
                key = key.strip().lower()
                key = key.replace(" ", "")
                key = re.sub(r'[^a-zA-Z0-9]', '', key)
                if key in loaded_list:
                    del loaded_list[key]
                    print(f"{key} removed from list")
                else:
                    print(f"{key} not found")
            else:
                print("Invalid choice. Please enter 'add', 'edit', or 'remove'.")
                edit_list()
        with open('progress.json', 'w') as writefile:
            json.dump(loaded_list, writefile, indent=4)
        print("done!")
        print_shopping_list.print_list()