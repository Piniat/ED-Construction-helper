from modules import state, start_input, clean_screen, elite_timestamp, event_handler, ship_cargo_ask, print_shopping_list
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import prompt
import re
import os
import ndjson
import json
import math

def tracking_mode():
    complete = WordCompleter(state.all_comodities, ignore_case=True)
    if not os.path.isfile('progress.json') and state.initialized == False:
        initial_list = {}
        item_amount = int(prompt("How many items do you plan on buying? \n"))
        i = 0
        for i in range(item_amount):
            key = prompt("Commodity name in all lower case and no spaces: \n", completer=complete, complete_while_typing=True, complete_in_thread=True)
            value = prompt("Amount needed: \n")
            key = key.strip()
            value = value.strip()
            key = key.replace(" ", "")
            key = re.sub(r'[^a-zA-Z0-9]', '', key)
            if key == "LandEnrichmentSystems":
                key = "terrainenrichmentsystems"
            initial_list[key.lower()] = int(value)
        formatted_list = json.dumps(initial_list, indent=4)
        copy_over = prompt("Would you like to copy the list to Construction_progress.json for delivery tracking later? y/n\n> ")
        with open("progress.json", "w") as outfile:
            outfile.write(formatted_list)
        print("created progress file")
        if copy_over == "y":
            with open("Construction_progress.json", "w") as other_outfile:
                other_outfile.write(formatted_list)
            ship_cargo_ask.request_ship_cargo()
            print_shopping_list.print_list()
        elif copy_over == "n":
            ship_cargo_ask.request_ship_cargo()
            print_shopping_list.print_list()
            state.initialized = True
        else:
            print("Error. Incorrect option. Defaulting to no")
    elif state.initialized == False or state.switched is True:
        with open('progress.json', 'r') as openfile:
            initial_list = json.load(openfile)
            formatted_list = json.dumps(initial_list, indent=4)
            clean_screen.clear_screen()
            #state.ship_cargo_space = int(prompt("Type the cargo capacity of your ship:\n> ", cursor=CursorShape.BLINKING_BLOCK))
            ship_cargo_ask.request_ship_cargo()
            clean_screen.clear_screen()
            print_shopping_list.print_list()
            state.initialized = True
            state.switched = False
    if state.input_started == False:
        start_input.start_user_input()
        state.input_started = True
    for line in state.lines:
                try:
                    curr_event = ndjson.loads(line.strip())
                    for state.event in curr_event:
                            if state.event.get('event') == "MarketBuy":
                                with open('progress.json', 'r') as openfile:
                                    initial_list = json.load(openfile)
                                    formatted_list = json.dumps(initial_list, indent=4)
                                timestamp = state.event.get('timestamp')
                                ed_timestamp=timestamp
                                state.formatted_timestamp = elite_timestamp.convert_timestamp(ed_timestamp)
                                curr_material = state.event.get('Type')
                                try:
                                    localised_curr_material = str(state.event.get("Name_Localised")).strip().lower().replace(" ", "")
                                    localised_curr_material = re.sub(r'[^a-zA-Z0-9]', '', localised_curr_material)
                                except:
                                    continue
                                subtract = state.event.get('Count')
                                if state.event.get('Type') not in initial_list or localised_curr_material not in initial_list:
                                    print("Error, item not on list. Did you spell it correctly?")
                                else:
                                    if state.event.get('Type') not in initial_list:
                                         curr_material = localised_curr_material
                                    saved_old_amount = int(initial_list.get(curr_material))
                                    new_amount = saved_old_amount - subtract
                                    with open('progress.json', 'w') as updateprogressfile:
                                        try:
                                            initial_list[curr_material] = new_amount
                                            json.dump(initial_list, updateprogressfile, indent=4)
                                        except KeyError as e:
                                            print(f"KeyError: {e}")
                                            missing_key = "Key formatting error or item not on list"
                                            print(missing_key)
                                    clean_screen.clear_screen()
                                    print("\n" + "-" * 60)
                                    print(f"{'Timestamp':<20}: {elite_timestamp.convert_timestamp(ed_timestamp)}")
                                    print("\n" + "-" * 60)
                                    print_shopping_list.print_list()
                                    item_trips_left = new_amount/state.ship_cargo_space
                                    item_trips_left = math.ceil(item_trips_left)
                                    print(f"{item_trips_left} trips for {curr_material} left")
                                    print("\n" + "-" * 60)
                                    print(curr_material.capitalize() + " remaining: " + str(new_amount))
                            elif state.event.get('event') == "Shutdown":
                                event_handler.game_shutdown()
                except json.JSONDecodeError:
                    print(f"Skipping invalid line: {line}")
                    continue