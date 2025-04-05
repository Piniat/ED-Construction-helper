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
    copy_progress = prompt("Copy from shopping list? (Progress.json) y/n \n> ", cursor=CursorShape.BLINKING_BLOCK)
    if copy_progress == "y":
        shutil.copyfile('progress.json', 'Construction_progress.json')
    elif copy_progress == "n":
        item_amount = int(prompt("How many different commodities do you need for construction? \n> ", cursor=CursorShape.BLINKING_BLOCK))
        for i in range(item_amount):
            key = prompt("Commodity name: \n> ", completer=complete, complete_while_typing=True, complete_in_thread=True)
            value = prompt("Amount needed: \n")
            key = key.strip()
            value = value.strip()
            key = key.replace(" ", "")
            key = re.sub(r'[^a-zA-Z0-9]', '', key)
            if key == "LandEnrichmentSystems":
                key = "terrainenrichmentsystems"
            progress_list[key.lower()] = int(value)
        formatted_list = json.dumps(progress_list, indent=4)
        with open("Construction_progress.json", "w") as outfile:
            outfile.write(formatted_list)