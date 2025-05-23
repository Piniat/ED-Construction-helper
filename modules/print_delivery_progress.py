#from modules import clean_screen, state, generate_time_timestamp
import json
import math
import os
from . import state
import time
import ndjson
import json

#def print_construction_progress():
#    loops = 0
#    total = 0
#    clean_screen.clear_screen()
#    timestamp = generate_time_timestamp.generate_one_time_timestamp()
#    print("\n" + "-" * 60)
#    print(f"Timestamp: {timestamp}")
#    print("\n" + "-" * 60)
#    print("Delivery tracking mode")
#    print("\n" + "-" * 60)
#    try:
#        with open('Construction_progress.json', "r") as progress:
#            progress_data = json.load(progress)
#            max_item_length = max(len(item) for item in progress_data)
#            for item, count in progress_data.items():
#                total += int(count)
#                if count > 0:
#                    print(f"{item.capitalize():<{max_item_length}}: {count:>{5}}")
#                elif count < 0:
#                    print(f"✔!  {item.capitalize():<{max_item_length - 4}}: {count:>{5}} - This shouldn't happen...")
#                elif count == 0:
#                    print(f"✔  {item.capitalize():<{max_item_length - 3}}: {count:>{5}}")
#        print("\n" + "-" * 60)
#        trips_left = total/state.ship_cargo_space
#        trips_left = math.ceil(trips_left)
#        print(f"{trips_left} trip{'s' if trips_left != 1 else ''} left\n")
#        if state.percent_complete is None:
#            print("\n" + "-" * 60)
#            print("Percentage will be displayed on game journal update")
#        else:
#            state.percent_complete = round(state.percent_complete, 1)
#            bar_length = 50
#            percent_intiger = int(state.percent_complete)
#            if percent_intiger == 0:
#                 block = 0
#            else:
#                 block = int((bar_length * percent_intiger) / 100)
#            progress = "#" * block + "-" * (bar_length - block)
#            print("\n" + "-" * 60)
#            print(f"Progress: {state.percent_complete}% \n")
#            print(f"[{progress}]")
#        print("\n" + "-" * 60)
#        for item in state.contributed_display_name:
#            print(f"{state.contributed_display_amount[loops]} tonnes of {state.contributed_display_name[loops]} delivered")
#            loops += 1
#        state.contributed_display_name.clear()
#        state.contributed_display_amount.clear()
#    except (json.JSONDecodeError, FileNotFoundError) as e:
#                print(f"Error reading cargo file: {e}")

def get_data():
    with open(state.journal_file_path) as f:
        f.seek(0, os.SEEK_END)
        while True:
            lines = f.readlines()
            for line in lines:
                curr_event = ndjson.loads(line.strip())
                for state.event in curr_event:
                    if state.event.get('event') == "ColonisationConstructionDepot":
                        state.percent_complete = state.event.get('ConstructionProgress')
                        state.percent_complete = state.percent_complete * 100
                        state.percent_complete = int(state.percent_complete)
                        print(state.percent_complete)
            else:
                time.sleep(0.5)