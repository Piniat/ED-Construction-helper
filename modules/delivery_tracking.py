#this will be the new journal event based delivery tracker (thanks fdev for finally adding the journal logs :D)



from modules import state, clean_screen, print_delivery_progress, create_delivery_tracking, event_handler, start_input, ship_cargo_ask
import os
import json
import ndjson
import time
import re
from prompt_toolkit import prompt
from prompt_toolkit.cursor_shapes import CursorShape

def write_delivery_progress(item_name, updated_needed):
    try:
        if os.path.isfile("Construction_progress.json"):
            with open("Construction_progress.json", "r") as progress_file:
                progress_data = json.load(progress_file)
        else:
            progress_data = {}
        progress_data[item_name] = updated_needed
        with open("Construction_progress.json", "w") as update_file:
            json.dump(progress_data, update_file, indent=4)
        state.ready_to_print = True
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error updating Construction_progress.json: {e}")

def clean_invalid_items(current_items):
    try:
        if os.path.isfile("Construction_progress.json"):
            with open("Construction_progress.json", "r") as progress_file:
                progress_data = json.load(progress_file)
        else:
            return
        items_to_delete = [key for key in progress_data if key not in current_items]
        for key in items_to_delete:
            print(f"Removing unrequired item: {key}")
            del progress_data[key]
        with open("Construction_progress.json", "w") as f:
            json.dump(progress_data, f, indent=4)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error updating Construction_progress.json: {e}")
        

def colonisation_tracker():
    state.ready_to_print = False
    #initial setup for tracking
    if state.initialized == False or state.switched == True:
        clean_screen.clear_screen()
        if state.ship_cargo_space == 0:
            ship_cargo_ask.request_ship_cargo()
        state.item_name_list = []
        state.item_count_list = []
        state.delivered_amount = []
        state.current_amount_delivered = []
        if not os.path.isfile("Construction_progress.json"):
            auto_create = prompt("Would you like to automatically create the delivery list? y/n \n> ", cursor=CursorShape.BLINKING_BLOCK).strip().lower()
            if auto_create == "n":
                with open("Construction_progress.json", "w") as progress_file:
                    create_delivery_tracking.create_progress_tracking()
                    print_delivery_progress.print_construction_progress()
            else:
                print("Understood. Please dock at your desired construction and wait for list to update...")
        else:
            print_delivery_progress.print_construction_progress()
        state.initialized = True
        state.switched = False
    # Start user input if not started
    if state.input_started == False:
        start_input.start_user_input()
        state.input_started = True
    for line in state.lines:
        try:
            curr_event = ndjson.loads(line.strip())
            for state.event in curr_event:
                if state.event.get('event') == "Docked":
                    print("Docked at a station")
                    state.ship_docked = True
                    #checks for colonisationcontribution service and if available sets state.docked_at_construction
                    if "colonisationcontribution" in state.event.get('StationServices', []):
                        print("Docked at a construction ship, tracking deliveries.")
                        state.docked_at_construction = True
                    else:
                        state.docked_at_construction = False
                #clears both docked statuses
                elif state.event.get('event') == "Undocked":
                    state.ship_docked = False
                    state.docked_at_construction = False
                    print("Undocked from station")
                #terminates app if shutdown event is detected
                elif state.event.get('event') == "Shutdown":
                    event_handler.game_shutdown()
                elif state.event.get('event') == "ColonisationConstructionDepot":
                    #print("construction data detected")
                    current_items = set()
                    state.percent_complete = int(state.event.get('ConstructionProgress'))
                    state.percent_complete = round(state.event.get('ConstructionProgress'))
                    for resource in state.event.get('ResourcesRequired'):
                        # Clean and set the item name
                        item_name = re.sub(r'[^a-zA-Z0-9]', '', resource.get('Name_Localised', resource.get('Name')).strip().lower().replace(" ", "").replace("name", ""))
                        needed_amount = resource.get('RequiredAmount')
                        provided_amount = resource.get('ProvidedAmount')
                        state.item_name_list.append(item_name)
                        state.item_count_list.append(needed_amount)
                        # Update the current delivery amount for this resource
                        updated_needed = needed_amount - provided_amount
                        current_items.add(item_name)
                        # Check if there's any change compared to the last delivered amount (assuming state.last_delivered_amount is a dict)
                        if state.last_delivered_amount.get(item_name) != provided_amount:
                            write_delivery_progress(item_name, updated_needed)
                            # Update the last delivered amount for this resource
                            state.last_delivered_amount[item_name] = provided_amount
                    state.percent_complete = state.event.get('ConstructionProgress')
                    state.percent_complete = int(state.percent_complete * 100)
                    clean_invalid_items(current_items)
                #track how much of a commodity was delivered
                elif state.event.get('event') == "ColonisationContribution":
                    for contribution in state.event.get('Contributions'):
                        item_name = contribution.get('Name_Localised', contribution.get('Name'))
                        amount_contributed = contribution.get('Amount')
                        state.contributed_display_amount.append(amount_contributed)
                        state.contributed_display_name.append(item_name)
        except json.JSONDecodeError:
            print(f"Skipping invalid line: {line}")
            continue
        if state.ready_to_print == True:
            print_delivery_progress.print_construction_progress()
            state.ready_to_print = False
        time.sleep(0.1)