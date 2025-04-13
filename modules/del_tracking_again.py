#no longer used in favour of delivery_tracking which now uses journal events

from modules import state, clean_screen, print_delivery_progress, create_delivery_tracking, event_handler, start_input, ship_cargo_ask
import os
import json
import ndjson
import time
import re

def colonisation_tracker():
    ready_to_print = False
    #initial setup for tracking
    if state.initialized == False or state.switched == True:
        clean_screen.clear_screen()
        if state.ship_cargo_space == 0:
            ship_cargo_ask.request_ship_cargo()
        state.item_name_list = []
        state.item_count_list = []
        state.delivered_amount = 0
        if not os.path.isfile("Construction_progress.json"):
            with open("Construction_progress.json", "w") as progress_file:
                create_delivery_tracking.create_progress_tracking()
                print_delivery_progress.print_construction_progress()
        print_delivery_progress.print_construction_progress()
        print("Use the appropriate command if app started while docked:\noverride-docked\noverride-docked-construction")
        state.initialized = True
        state.switched = False
    #checks if progress file exists
    if not os.path.isfile("Construction_progress.json"):
        with open("Construction_progress.json", "w") as progress_file:
            create_delivery_tracking.create_progress_tracking()
            print_delivery_progress.print_construction_progress()
    # Start user input if not started
    if state.input_started == False:
        start_input.start_user_input()
        state.input_started = True
    cargo_file = os.path.join(state.journal_folder, "Cargo.json")
    for line in state.lines:
        try:
            curr_event = ndjson.loads(line.strip())
            for state.event in curr_event:
                if state.event.get('event') == "Docked":
                    print("Docked at a station")
                    state.ship_docked = True
                    #checks for colonisationcontribution service and if available sets state.docked_at_construction to allow tracking
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
        except json.JSONDecodeError:
            print(f"Skipping invalid line: {line}")
            continue
    if state.ship_docked:
        try:
            with open(cargo_file, "r") as cargo:
                cargo_data = json.load(cargo)
                current_cargo_list = cargo_data.get('Inventory', [])
                current_cargo_data = {re.sub(r'[^a-zA-Z0-9]', '', item.get('Name_Localised', item.get('Name')).strip().lower().replace(" ", "")): item['Count'] for item in current_cargo_list}
                state.cargo_read_attempts = 0
                if state.initialized == False:
                    state.get_updated_cargo = current_cargo_data
                    state.initialized = True
                if current_cargo_data != state.get_updated_cargo:
                    for item, old_count in state.get_updated_cargo.items():
                        new_count = current_cargo_data.get(item, 0)
                        if state.docked_at_construction:
                            if item not in current_cargo_list:
                                if new_count == 0:
                                    state.delivered_amount = old_count
                                elif new_count < old_count:
                                    state.delivered_amount = old_count - new_count
                                if  old_count >= new_count:
                                    state.item_name = item
                                    state.item_name_list.append(state.item_name)
                                    state.item_count_list.append(state.delivered_amount)
                                    try:
                                        if os.path.isfile("Construction_progress.json"):
                                            with open("Construction_progress.json", "r") as progress_file:
                                                progress_data = json.load(progress_file)
                                        else:
                                            progress_data = {}
                                        if state.item_name in progress_data:
                                            progress_data[state.item_name] = progress_data[state.item_name] - state.delivered_amount
                                        else:
                                            print("Item not found in progress list. Did you spell it correctly?")
                                        # Write updated progress to file
                                        with open("Construction_progress.json", "w") as update_file:
                                            json.dump(progress_data, update_file, indent=4)
                                            ready_to_print = True
                                    except (json.JSONDecodeError, FileNotFoundError) as e:
                                        print(f"Error updating Construction_progress.json: {e}")
        except(json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading cargo file: {e}")
            if state.cargo_read_attempts <= 5:
                state.cargo_read_attempts += 1
                print(f"Retrying in 2 seconds... (attempt {state.cargo_read_attempts})")
                time.sleep(2)
                colonisation_tracker()
            else:
                print("5 retry attempts failed. Aborting....")
                return
        state.get_updated_cargo = current_cargo_data
        if ready_to_print == True:
            print_delivery_progress.print_construction_progress()
            ready_to_print = False
        time.sleep(0.1)