from . import state, create_timestamp, print_shopping_list, create_shopping_list_dialog
from dialogs import manual_only_creation
from PySide6.QtCore import QObject, Signal
import re
import os
import ndjson
import json

def tracking_mode(self):
    self.html_output = ""
    self.extra = ""
    self.trips = ""
    self.html_output += f"<hr>{create_timestamp.generate_one_time_timestamp()}<hr>"
    if not os.path.isfile('Shopping_list.json') and state.initialized == False:
        if os.path.isfile('Construction_progress.json'):
            print("copy possible, ask if wanna copy")
            self.creation_ask.emit()
        else:
            print("notify about missing file and peform manual creation")
            self.creation_no_ask.emit()
    elif (state.initialized == False) or (state.switched == True):
        with open('Shopping_list.json', 'r') as openfile:
            initial_list = json.load(openfile)
            print_shopping_list.print_list(self)
            state.initialized = True
            state.switched = False
        state.input_started = True
    for line in state.line:
                try:
                    curr_event = ndjson.loads(line.strip())
                    for self.event in curr_event:
                            if self.event.get('event') == "MarketBuy":
                                with open('progress.json', 'r') as openfile:
                                    initial_list = json.load(openfile)
                                curr_material = self.event.get('Type')
                                try:
                                    localised_curr_material = str(self.event.get("Type_Localised")).strip().lower().replace(" ", "")
                                    localised_curr_material = re.sub(r'[^a-zA-Z0-9]', '', localised_curr_material)
                                except:
                                    continue
                                subtract = self.event.get('Count')
                                if (self.event.get('Type') not in initial_list) and (localised_curr_material not in initial_list):
                                    self.extra += "Error, item not on list. Did you spell it correctly?"
                                else:
                                    if self.event.get('Type') not in initial_list:
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
                                            self.extra += missing_key
                                    print_shopping_list.print_list(self)
                                    #Re-implement later possibly
                                    #item_trips_left = new_amount/state.ship_cargo_space
                                    #item_trips_left = math.ceil(item_trips_left)
                                    #print(f"{item_trips_left} trips for {curr_material} left")
                                    #print("\n" + "-" * 60)
                                    #print(curr_material.capitalize() + " remaining: " + str(new_amount))
                            elif self.event.get('event') == "Shutdown":
                                #event_handler.game_shutdown()
                                print("app shutdown here")
                except json.JSONDecodeError:
                    print(f"Skipping invalid line: {line}")
                    continue