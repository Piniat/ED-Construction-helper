from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.cursor_shapes import CursorShape
import shutil
import json
import re
from modules import state

def create_progress_tracking():
    complete = WordCompleter(state.all_comodities, ignore_case=True)
    print("Need to create file")
    progress_list = {}
    copy_progress = prompt("Copy from shopping list? (Progress.json) y/n \n> ", cursor=CursorShape.BLINKING_BLOCK).strip().lower()
    if copy_progress == "y":
        shutil.copyfile('progress.json', 'Construction_progress.json')
    elif copy_progress == "n":
        item_amount = int(prompt("How many different commodities do you need for construction? \n> ", cursor=CursorShape.BLINKING_BLOCK))
        for i in range(item_amount):
            key = prompt("Commodity name: \n> ", completer=complete, complete_while_typing=True, complete_in_thread=True).strip().lower().replace(" ", "")
            key = re.sub(r'[^a-zA-Z0-9]', '', key)
            while True:
                try:
                    value = int(prompt("Amount needed: \n"))
                    break
                except:
                    print("Invalid input. Please input the number of commodities you need")
            progress_list[key] = value
        formatted_list = json.dumps(progress_list, indent=4)
        with open("Construction_progress.json", "w") as outfile:
            outfile.write(formatted_list)