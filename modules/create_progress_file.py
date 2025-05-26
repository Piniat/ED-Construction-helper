import json
from modules import state

def create_progress_tracking():
    formatted_list = json.dumps(state.progress_list, indent=4)
    with open("Shopping_list.json", "w") as outfile:
        outfile.write(formatted_list)