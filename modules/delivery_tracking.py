#this will be the new journal event based delivery tracker (thanks fdev for finally adding the journal logs :D)



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
        if ready_to_print == True:
            print_delivery_progress.print_construction_progress()
            ready_to_print = False
    time.sleep(0.1)