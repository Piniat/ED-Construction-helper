from modules import state, clean_screen, print_delivery_progress, create_delivery_tracking, event_handler, start_input
import os
import json
import ndjson
from prompt_toolkit import prompt
from prompt_toolkit.cursor_shapes import CursorShape
import time

def colonisation_tracker():
    ready_to_print = False
    #initial setup for tracking
    if state.initialized == False or state.switched == True:
        clean_screen.clear_screen()
        state.ship_cargo_space = int(prompt("Type the cargo capacity of your ship:\n> ", cursor=CursorShape.BLINKING_BLOCK))
        state.item_name_list = []
        state.item_count_list = []
        state.delivered_amount = 0
        print_delivery_progress.print_construction_progress()
        print("Helpful comands:\nhelp\noverride-docked\noverride-docked-construction")
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
    # set file path to the appropiate format matching the os
    cargo_file = os.path.join(state.journal_folder, "Cargo.json")
    for line in state.lines:
        try:
            curr_event = ndjson.loads(line.strip())
            for event in curr_event:
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
            #opens cargo.json file
            with open(cargo_file, "r") as cargo:
                cargo_data = json.load(cargo)
                #extracts cargo data
                current_cargo_list = cargo_data.get("Inventory", [])
                current_cargo_data = {item['Name']: item['Count'] for item in current_cargo_list}
                if current_cargo_data != state.input_started:
                    print("Cargo change detected")
                    #loops through every time to find which one/s have been fully removed from cargo.json
                    for state.item_name in list(state.input_started.keys()):
                        if state.item_name not in current_cargo_data and state.docked_at_construction:
                            #appends items names and amounts to a list used to update progress and to display
                            state.item_name_list.append(state.switched)
                            state.delivered_amount = state.input_started[state.switched]
                            state.item_count_list.append(state.delivered_amount)
                            #attempts to updated progress file
                            try:
                                if os.path.isfile("Construction_progress.json"):
                                    with open("Construction_progress.json", "r") as progress_file:
                                        progress_data = json.load(progress_file)
                                else:
                                    progress_data = {}
                                if state.switched in progress_data:
                                    progress_data[state.switched] = progress_data[state.switched] - state.delivered_amount
                                else:
                                    print("Item not found in progress list. Did you spell it correctly?")
                                # Write updated progress to file
                                with open("Construction_progress.json", "w") as update_file:
                                    json.dump(progress_data, update_file, indent=4)
                                    ready_to_print = True
                            except (json.JSONDecodeError, FileNotFoundError) as e:
                                print(f"Error updating Construction_progress.json: {e}")
                    #loops through every time to find which one/s have been only partially removed from cargo.json
                    for state.switched, item_count in current_cargo_data.items():
                        if state.docked_at_construction:
                            if item_count < state.input_started.get(state.switched, 0):
                                state.delivered_amount = state.input_started[state.switched] - item_count
                                #appends items names and amounts to a list used to update progress and to display
                                state.state.switched_list.append(state.item_name)
                                state.item_count_list.append(state.delivered_amount)
                                # attempts to update Construction_progress.json
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
                                    with open("Construction_progress.json", "w") as update_file:
                                        json.dump(progress_data, update_file, indent=4)
                                        ready_to_print = True
                                except (json.JSONDecodeError, FileNotFoundError) as e:
                                    print(f"Error updating Construction_progress.json: {e}")
                        #just displays amounts of commodities bought/transferred or stored. Serves no other function
                        elif state.ship_docked and not state.docked_at_construction:
                            if state.item_name not in state.input_started:
                                print(f"New cargo detected. Bought/transferred: {state.item_name} - {item_count} tonnes")
                            elif item_count > state.input_started.get(state.item_name, 0):
                                print(f"Bought/transferred {state.item_name}: {item_count - state.input_started[state.item_name]} tonnes")
                            elif item_count < state.input_started.get(state.item_name, item_count):
                                print(f"Stored: {state.input_started[state.item_name] - item_count} tonnes of {state.item_name}")     
                    #updates cargo data
                    state.input_started = current_cargo_data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading cargo file: {e}")
        if ready_to_print == True:
            print_delivery_progress.print_construction_progress()
            ready_to_print = False
    time.sleep(0.1)