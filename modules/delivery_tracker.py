from modules import state, print_delivery_progress
import os
import json
import ndjson
import time
import re

#updates progress file
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

#removes commodities not found in the colonisation event
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
        
def colonisation_tracker(self):
    state.ready_to_print = False
    #initial setup for tracking
    if (state.initialized == False) or (state.switched == True):
        state.delivered_amount = []
        state.current_amount_delivered = []
        if not os.path.isfile("Construction_progress.json"):
                with open("Construction_progress.json", "w") as progress_file:
                    #create_progress_file.create_progress_tracking()
                    message = {"dontprint": 0}
                    json.dump(message, progress_file, indent=4)
                    print_delivery_progress.print_construction_progress(self)
        state.initialized = True
        state.switched = False
        print_delivery_progress.print_construction_progress(self)
    try:
        for line in state.line:
            curr_event = ndjson.loads(state.line.strip())
            for self.event in curr_event:
                if self.event.get('event') == "Loadout":
                    state.ship_cargo_space = self.event.get('CargoCapacity')
                    print_delivery_progress.print_construction_progress(self)
                #exits app if shutdown event is detected
                if self.event.get('event') == "Shutdown":
                    #event_handler.game_shutdown()
                    print("App would shutdown here")
                elif self.event.get('event') == "ColonisationConstructionDepot":
                    current_items = set()
                    state.percent_complete = self.event.get('ConstructionProgress')
                    #state.percent_complete = round(state.percent_complete * 100)
                    state.percent_complete = state.percent_complete * 100
                    for resource in self.event.get('ResourcesRequired'):
                        # Clean and set the item name
                        item_name = re.sub(r'[^a-zA-Z0-9]', '', resource.get('Name_Localised', resource.get('Name')).strip().lower().replace(" ", "").replace("name", ""))
                        needed_amount = resource.get('RequiredAmount')
                        provided_amount = resource.get('ProvidedAmount')
                        # Update the current needed amount for this resource
                        updated_needed = needed_amount - provided_amount
                        current_items.add(item_name)
                        # Check if there's any change compared to the last delivered amount
                        if state.last_delivered_amount.get(item_name) != provided_amount:
                            write_delivery_progress(item_name, updated_needed)
                            # Update the last delivered amount for this resource
                            state.last_delivered_amount[item_name] = provided_amount
                    clean_invalid_items(current_items)
                #track how much of a commodity was delivered
                elif self.event.get('event') == "ColonisationContribution":
                    for contribution in self.event.get('Contributions'):
                        item_name = contribution.get('Name_Localised', contribution.get('Name'))
                        amount_contributed = contribution.get('Amount')
                        state.contributed_display_amount.append(amount_contributed)
                        state.contributed_display_name.append(item_name)
    except json.JSONDecodeError:
        print(f"Json error on line: {state.lines}")
    if state.ready_to_print == True:
        print_delivery_progress.print_construction_progress(self)
        state.ready_to_print = False
    time.sleep(0.1)