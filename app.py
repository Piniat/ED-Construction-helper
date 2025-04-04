import os
import time
import ndjson
import glob
import configparser
import json
import threading
from prompt_toolkit import prompt
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style
from datetime import datetime
from tzlocal import get_localzone
import pytz
import shutil
import math
import re
import sys

#prompt colors (only red for now) also ignore the random positioning of this
style = Style.from_dict({
    "":          "#ff0066",
    "iwarning":  "#ff0000",
})

#functions  

def template():
    print("\n" + "-" * 60)
    print(f"{'Timestamp':<20}: {formatted_timestamp}")
    print(f"{'event':<20}: {event.get('event')}")

def unhandled_event():
    print("\n" + "-" * 60)
    print("[Unhandled event]: " + event.get('event'))

def game_shutdown():
    template()
    print("\nGame shutdown detected. Exiting...")
    time.sleep(1)
    close_app()
        
def start_jump():
    template()
    print(f"{'Destination':<20}: {event.get('StarSystem')}")
    print(f"{'Star type':<20}: {event.get('StarClass')}")

def docked():
    template()
    print(f"{'Station Name':<20}: {event.get('StationName')}")
    print(f"{'Station Type':<20}: {event.get('StationType')}")

def undocked():
    template()
    print(f"{'Station Name':<20}: {event.get('StationName')}")
    print(f"{'Station Type':<20}: {event.get('StationType')}")

def docking_cancelled():
    template()
    print(f"{'Station Name':<20}: {event.get('StationName')}")
    print(f"{'Station Type':<20}: {event.get('StationType')}")

def docking_denied():
    template()
    print(f"{'Station Name':<20}: {event.get('StationName')}")
    print(f"{'Station Type':<20}: {event.get('StationType')}")
    print(f"{'Reason':<20}: {event.get('Reason')}")

def docking_granted():
    template()
    print(f"{'Station Name':<20}: {event.get('StationName')}")
    print(f"{'Station Type':<20}: {event.get('StationType')}")
    print(f"{'Pad':<20}: {event.get('LandingPad')}")

def docking_timeout():
    template()
    print(f"{'Station Name':<20}: {event.get('StationName')}")
    print(f"{'Station Type':<20}: {event.get('StationType')}")

def music():
    template()
    print(f"{'Music Track':<20}: {event.get('MusicTrack')}")

def commander():
    template()
    print(f"{'Name':<20}: {event.get('Name')}")
    print(f"{'Player id':<20}: {event.get('FID')}")

def resurrect():
    template()
    print(f"{'Option':<20}: {event.get('Option')}")
    print(f"{'Cost':<20}: {event.get('Cost')}")
    print(f"{'Bankrupt':<20}: {event.get('Bankrupt')}")

def death():
    template()
    print(f"{'Killer name':<20}: {event.get('KillerName')}")
    print(f"{'Killer ship':<20}: {event.get('KillerShip')}")
    print(f"{'Killer rank':<20}: {event.get('KillerRank')}")

def friends():
    template()
    print(f"{'Name':<20}: {event.get('Name')}")
    print(f"{'Status':<20}: {event.get('Status')}")

def materials():
    template()
    raw_array = event.get('Raw')
    print("\n" + "*" * 30 + "\n Raw")
    for name in raw_array:
        print(f"{name['Name']:<20}: {name['Count']}")
    manu_array = event.get('Manufactured')
    print("\n" + "*" * 30 + "\n Manufactured")
    for name in manu_array:
        print(f"{name['Name']:<20}: {name['Count']}")
    encoded_array = event.get('Encoded')
    print("\n" + "*" * 30 + "\n Encoded")
    for name in encoded_array:
        print(f"{name['Name']:<20}: {name['Count']}")
    
def header():
    template()
    print(f"{'Part':<20}: {event.get('part')}")
    print(f"{'Language':<20}: {event.get('language')}")
    print(f"{'Game version':<20}: {event.get('gameversion')}")
    print(f"{'Build':<20}: {event.get('build')}")

def rank():
    template()
    print(f"{'Combat':<20}: {event.get('Combat')}")
    print(f"{'Trade':<20}: {event.get('Trade')}")
    print(f"{'Exploration':<20}: {event.get('Explore')}")
    print(f"{'CQC':<20}: {event.get('CQC')}")

def marketbuy():
    template()
    print(f"{'MarketID':<20}: {event.get('MarketID')}")
    print(f"{'Type':<20}: {event.get('Type')}")
    print(f"{'Count':<20}: {event.get('Count')}")
    print(f"{'Buy Price':<20}: {event.get('BuyPrice')}")
    print(f"{'Total Cost':<20}: {event.get('TotalCost')}")

def get_latest_journal():
    latest_file = glob.glob(os.path.join(journal_folder, 'Journal.*.log'))
    if not latest_file:
        print("No journal files found.")
    newest_file = max(latest_file, key=os.path.getctime)
    return newest_file

def user_input():
    global message
    global app_mode
    global ship_docked
    global docked_at_construction
    global ship_cargo_space
    global switched
    global just_started
    command_list = WordCompleter(["help", "app-mode-1", "app-mode-2", "app-mode-3", "override-docked", "override-docked-construction", "edit-shopping-list", "edit-construction-progress", "edit-ship-cargo", "exit", "reset-progress"], ignore_case=True)
    while True:
        with patch_stdout():
            usr_input = prompt("> ", cursor=CursorShape.BLINKING_BLOCK, completer=command_list, complete_while_typing=True, complete_in_thread=True)
            if usr_input == "exit":
                print("Exiting program...")
                time.sleep(1)
                close_app()
            elif usr_input == "help":
                print("List of commands: \n exit - exits the program \n app-mode-1 - switches to construction progress tracking \n app-mode-2 - switches to app to shopping list mode \n app-mode-3 - switches app to journal monitoring mode \n edit-shopping-list - allows you to edit shopping list in-app \n override-docked - overrides docked status in mode 3 \n override-docked-construction - overrides if you are docked at a constructions site / megaship (any cargo removed from your hold will be counted towards progress to buiding) \n edit-ship-cargo")
            elif usr_input == "app-mode-1":
                switched = True
                just_started = False
                app_mode = "1"
                print("Switched to construction progress tracking.")
            elif usr_input == "app-mode-2":
                switched = True
                just_started = False
                app_mode = "2"
                print("Switched to shopping list tracking")
            elif usr_input == "app-mode-3":
                switched = True
                just_started = False
                app_mode = "3"
                print("Switched to journal logging mode")
            elif usr_input == "override-docked":
                print("Current status: ", ship_docked)
                state = prompt("Are you docked? y/n \n> ")
                if state == "y":
                    ship_docked = True
                    print("Current status: ", ship_docked)
                elif state == "n":
                    ship_docked == False
                    print("Current status: ", ship_docked)
                else:
                    print("Error. Please choose y or n")
            elif usr_input == "override-docked-construction":
                print("Current status: ", docked_at_construction)
                state_colon = prompt("Are you docked at a place where colonisation contributions are accepted? y/n \n> ")
                if state_colon == "y":
                    docked_at_construction = True
                    print("Current status: ", docked_at_construction)
                elif state_colon == "n":
                    docked_at_construction = False
                    print("Current status: ", docked_at_construction)
                else:
                    print("Error. Please choose y or n")
            elif usr_input == "edit-shopping-list":
                edit_list()
            elif usr_input == "edit-construction-progress":
                    edit_colonisation_progress()
            elif usr_input == "edit-ship-cargo":
                ship_cargo_space = int(prompt("How much cargo space does your ship have? \n> "))
                print("Updated ship cargo space")
            elif usr_input == "reset-progress":
                autocomplete = WordCompleter(["Shopping", "Delivery", "both"], ignore_case=True)
                which = prompt("Do you want to delete the commodity shopping list, colonisation delivery list or both?\n 1-Shopping list \n 2-Delivery tracker \n 3-both \n exit \n> ", completer=autocomplete, complete_while_typing=True, complete_in_thread=True)
                if which == "1":
                    sure = prompt(f"Are you sure? THIS CANNOT BE UNDONE! Continue anyway? y/n \n>", style=style)
                    if sure == "y":
                        try:
                            os.remove("progress.json")
                            print("File removed!")
                            print("Restarting...")
                            time.sleep(0.5)
                            python = sys.executable
                            os.execv(python, [python] + sys.argv)
                        except:
                            print("Error. File not found")
                    elif sure == "n":
                        print("Operation cancelled")
                    else:
                        print("Invalid option. Cancelling...")
                elif which == "2":
                    sure = prompt(f"Are you sure? THIS CANNOT BE UNDONE! Continue anyway? y/n \n>", style=style)
                    if sure == "y":
                        try:
                            os.remove("Construction_progress.json")
                            print("File removed!")
                            print("Restarting...")
                            time.sleep(0.5)
                            python = sys.executable
                            os.execv(python, [python] + sys.argv)
                        except:
                            print("Error. File not found")
                    elif sure == "n":
                        print("Operation cancelled")
                    else:
                        print("Invalid option. Cancelling...")
                elif which == "3":
                    sure = prompt(f"Are you sure? THIS CANNOT BE UNDONE! Continue anyway? y/n \n>", style=style)
                    if sure == "y":
                        try:
                            os.remove("Construction_progress.json")
                            os.remove("progress.json")
                            print("Files removed!")
                            print("Restarting...")
                            time.sleep(0.5)
                            python = sys.executable
                            os.execv(python, [python] + sys.argv)
                        except:
                            print("Error. File not found")
                    elif sure == "n":
                        print("Operation cancelled")
                    else:
                        print("Invalid option. Cancelling...")
                elif which == "exit":
                    print("Cancelled!")
                else:
                    print("Invalid option")
            #elif usr_input == "debug":
            #    print_construction_progress()
            else:
                print('Error. Invalid command. Type "help" for a list of commands')
            
def edit_list():
    global all_comodities
    complete = WordCompleter(all_comodities, ignore_case=True)
    if not os.path.isfile('progress.json'):
        print("Error no list detected, please make one first")
    else:
        with open('progress.json', 'r') as readfile:
            loaded_list = json.load(readfile)
            option = prompt("1- Edit/Add \n2-Remove \n")
            if option == "1":
                key = prompt("Commodity name in all lower case and no spaces: \n", completer=complete, complete_while_typing=True, complete_in_thread=True)
                value = prompt("New amount needed: \n")
                key = key.strip()
                value = value.strip()
                key = key.replace(" ", "")
                key = re.sub(r'[^a-zA-Z0-9]', '', key)
                loaded_list[key.lower()] = int(value)
            elif option == "2":
                key = prompt("Commodity name in all lower case and no spaces: \n", completer=complete, complete_while_typing=True, complete_in_thread=True)
                key = key.strip()
                key = key.replace(" ", "")
                key = re.sub(r'[^a-zA-Z0-9]', '', key)
                if key in loaded_list:
                    del loaded_list[key]
                    print(f"{key} removed from list")
                else:
                    print(f"{key} not found")
            else:
                print("Invalid choice. Please enter 'add', 'edit', or 'remove'.")
        with open('progress.json', 'w') as writefile:
            json.dump(loaded_list, writefile, indent=4)
        print("done!")
        print_list()

def edit_colonisation_progress():
    global all_comodities
    complete = WordCompleter(all_comodities, ignore_case=True)
    if not os.path.isfile('Construction_progress.json'):
        print("Error no list detected, please make one first")
    else:
        with open('Construction_progress.json', 'r') as readfile:
            loaded_list = json.load(readfile)
            option = prompt("1- Edit/Add \n2-Remove \n")
            if option == "1":
                key = prompt("Commodity name in all lower case and no spaces: \n", completer=complete, complete_while_typing=True, complete_in_thread=True)
                value = prompt("New amount to deliver: \n")
                key = key.strip()
                value = value.strip()
                key = key.replace(" ", "")
                key = re.sub(r'[^a-zA-Z0-9]', '', key)
                loaded_list[key.lower()] = int(value)
            elif option == "2":
                key = prompt("Commodity name in all lower case and no spaces: \n", completer=complete, complete_while_typing=True, complete_in_thread=True)
                key = key.strip()
                key = key.replace(" ", "")
                key = re.sub(r'[^a-zA-Z0-9]', '', key)
                if key in loaded_list:
                    del loaded_list[key]
                    print(f"{key} removed from list")
                else:
                    print(f"{key} not found")
            else:
                print("Invalid choice. Please enter 'add', 'edit', or 'remove'.")
        with open('Construction_progress.json', 'w') as writefile:
            json.dump(loaded_list, writefile, indent=4)
        print("done!")
        print_construction_progress()

def start_user_input():
    t1 = threading.Thread(target=user_input, daemon=True)
    t1.start()
                
def close_app():
    os._exit(0)

def app_mode_selection():
    global app_mode
    app_mode = prompt("Select app mode: \n 1-Colonisation construction tracker \n 2-Shopping list \n 3-Journal monitor \n exit-exits the app \n : ", cursor=CursorShape.BLINKING_BLOCK)
    if app_mode == "exit":
        close_app()
    elif app_mode not in ["1", "2", "3"]:
        print("Invalid mode. Please select 1, 2, or 3.")
        app_mode_selection()

def convert_timestamp(ed_timestamp):
    utc_time = datetime.strptime(ed_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = pytz.utc.localize(utc_time)
    local_tz = get_localzone()
    local_time = utc_time.astimezone(local_tz)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

def log_mode():
    global input_started
    if input_started == False:
        start_user_input()
        input_started = True
    for line in lines:
                try:
                    curr_event = ndjson.loads(line.strip())
                    global event
                    for event in curr_event:
                        timestamp = event.get('timestamp')
                        global formatted_timestamp
                        ed_timestamp=timestamp
                        formatted_timestamp = convert_timestamp(ed_timestamp)
                        if event.get('event') == "Shutdown":
                            game_shutdown()
                        elif event.get('event') == "StartJump":
                            start_jump()
                        elif event.get('event') == "Docked":
                            docked()
                        elif event.get('event') == "Undocked":
                            undocked()
                        elif event.get('event') == "DockingCancelled":
                            docking_cancelled()
                        elif event.get('event') == "DockingDenied":
                            docking_denied()
                        elif event.get('event') == "DockingGranted":
                            docking_granted()
                        elif event.get('event') == "DockingTimeout":
                            docking_timeout()
                        elif event.get('event') == "Music":
                            music()
                        elif event.get('event') == "Commander":
                            commander()
                        elif event.get('event') == "Resurrect":
                            resurrect()
                        elif event.get('event') == "Friends":
                            friends()
                        elif event.get('event') == "Materials":
                            materials()
                        elif event.get('event') == "fileheader":
                            header()
                        elif event.get('event') == "Rank":
                            rank()
                        elif event.get('event') == "MarketBuy":
                            marketbuy()
                        else:
                            unhandled_event()
                except json.JSONDecodeError:
                    print(f"Skipping invalid line: {line}")
                    continue

def tracking_mode():
    global initialized
    global input_started
    global ship_cargo_space
    global all_comodities
    global switched
    complete = WordCompleter(all_comodities, ignore_case=True)
    if not os.path.isfile('progress.json') and initialized == False:
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
            print_list()
        elif copy_over == "n":
            print_list()
            initialized = True
        else:
            print("Error. Incorrect option. Defaulting to no")
    elif initialized == False or switched is True:
        with open('progress.json', 'r') as openfile:
            initial_list = json.load(openfile)
            formatted_list = json.dumps(initial_list, indent=4)
            clear_screen()
            ship_cargo_space = int(prompt("Type the cargo capacity of your ship:\n> ", cursor=CursorShape.BLINKING_BLOCK))
            clear_screen()
            print_list()
            initialized = True
            switched = False
    if input_started == False:
        start_user_input()
        input_started = True
    for line in lines:
                try:
                    curr_event = ndjson.loads(line.strip())
                    global event
                    for event in curr_event:
                            if event.get('event') == "MarketBuy":
                                with open('progress.json', 'r') as openfile:
                                    initial_list = json.load(openfile)
                                    formatted_list = json.dumps(initial_list, indent=4)
                                timestamp = event.get('timestamp')
                                ed_timestamp=timestamp
                                formatted_timestamp = convert_timestamp(ed_timestamp)
                                curr_material = event.get('Type')
                                subtract = event.get('Count')
                                if event.get('Type') not in initial_list:
                                    print("Error, item not on list. Did you spell it correctly?")
                                else:
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
                                    clear_screen()
                                    print("\n" + "-" * 60)
                                    print(f"{'Timestamp':<20}: {formatted_timestamp}")
                                    print("\n" + "-" * 60)
                                    print_list()
                                    item_trips_left = new_amount/ship_cargo_space
                                    item_trips_left = math.ceil(item_trips_left)
                                    print(f"{item_trips_left} trips for {curr_material} left")
                                    print("\n" + "-" * 60)
                                    print(curr_material.capitalize() + " remaining: " + str(new_amount))
                            elif event.get('event') == "Shutdown":
                                game_shutdown()
                except json.JSONDecodeError:
                    print(f"Skipping invalid line: {line}")
                    continue

def request_ship_cargo():
    global ship_cargo_space
    ship_cargo_space = int(prompt("How much cargo space does your ship have? \n> "))

def print_list():
    global initialized
    global ship_cargo_space
    if ship_cargo_space == 0:
        request_ship_cargo()
    total = 0
    with open('progress.json', 'r') as openfile:
        initial_list = json.load(openfile)
    timestamp = generate_one_time_timestamp()
    clear_screen()
    print("\n" + "-" * 60)
    print(f"Timestamp: {timestamp}")
    print("\n" + "-" * 60)
    print("Materials:")
    for material, amount in initial_list.items():
        total += amount
        if amount > 0:
            if material == "terrainenrichmentsystems":
                print(f"    Landenrichmentsystems: {amount} - Landenrichmentsystems")
            else:
                print(f"    {material.capitalize()}: {amount}")
        elif amount == 0:
            if material == "terrainenrichmentsystems":
                print(f"    Landenrichmentsystems: {amount} - Landenrichmentsystems")
            else:
                print(f"    ✔  {material.capitalize()}: {amount}")
        elif amount < 0:
            if material == "terrainenrichmentsystems":
                print(f"    Landenrichmentsystems: {amount} - Landenrichmentsystems")
            else:
                print(f"    ✔!  {material.capitalize()}: {amount} - overstock!")
    print("\n" + "-" * 60)
    trips_left = total/ship_cargo_space
    trips_left = math.ceil(trips_left)
    print(f"{trips_left} trips left")
    print("\n" + "-" * 60)

def generate_one_time_timestamp():
    local_tz = get_localzone()
    now = datetime.now(local_tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_progress_tracking():
    global all_comodities
    complete = WordCompleter(all_comodities, ignore_case=True)
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
            if key == "LandEnrichmentSystems":
                key = "terrainenrichmentsystems"
            progress_list[key.lower()] = int(value)
        formatted_list = json.dumps(progress_list, indent=4)
        with open("Construction_progress.json", "w") as outfile:
            outfile.write(formatted_list)

#Colonisation delivery tracker
def colonisation_tracker():
    global opened_json
    global journal_folder
    global ship_docked
    global docked_at_construction
    global input_started
    global updated_cargo
    global initialized
    global ship_cargo_space
    global item_name_list
    global item_count_list
    global delivered_amount
    global switched
    global item_name
    ready_to_print = False
    #initial setup for tracking
    if initialized == False or switched == True:
        clear_screen()
        ship_cargo_space = int(prompt("Type the cargo capacity of your ship:\n> ", cursor=CursorShape.BLINKING_BLOCK))
        item_name_list = []
        item_count_list = []
        delivered_amount = 0
        print_construction_progress()
        print("Helpful comands:\nhelp\noverride-docked\noverride-docked-construction")
        initialized = True
        switched = False
    #checks if progress file exists
    if not os.path.isfile("Construction_progress.json"):
        with open("Construction_progress.json", "w") as progress_file:
            create_progress_tracking()
            print_construction_progress()
    # Start user input if not started
    if input_started == False:
        start_user_input()
        input_started = True
    # set file path to the appropiate format matching the os
    cargo_file = os.path.join(journal_folder, "Cargo.json")
    for line in lines:
        try:
            curr_event = ndjson.loads(line.strip())
            for event in curr_event:
                if event.get('event') == "Docked":
                    print("Docked at a station")
                    ship_docked = True
                    #checks for colonisationcontribution service and if available sets docked_at_construction to allow tracking
                    if "colonisationcontribution" in event.get('StationServices', []):
                        print("Docked at a construction ship, tracking deliveries.")
                        docked_at_construction = True
                    else:
                        docked_at_construction = False
                #clears both docked statuses
                elif event.get('event') == "Undocked":
                    ship_docked = False
                    docked_at_construction = False
                    print("Undocked from station")
                #terminates app if shutdown event is detected
                elif event.get('event') == "Shutdown":
                    game_shutdown()
        except json.JSONDecodeError:
            print(f"Skipping invalid line: {line}")
            continue
    if ship_docked:
        try:
            #opens cargo.json file
            with open(cargo_file, "r") as cargo:
                cargo_data = json.load(cargo)
                #extracts cargo data
                current_cargo_list = cargo_data.get("Inventory", [])
                current_cargo_data = {item['Name']: item['Count'] for item in current_cargo_list}
                if current_cargo_data != updated_cargo:
                    print("Cargo change detected")
                    #loops through every time to find which one/s have been fully removed from cargo.json
                    for item_name in list(updated_cargo.keys()):
                        if item_name not in current_cargo_data and docked_at_construction:
                            #appends items names and amounts to a list used to update progress and to display
                            item_name_list.append(item_name)
                            delivered_amount = updated_cargo[item_name]
                            item_count_list.append(delivered_amount)
                            #attempts to updated progress file
                            try:
                                if os.path.isfile("Construction_progress.json"):
                                    with open("Construction_progress.json", "r") as progress_file:
                                        progress_data = json.load(progress_file)
                                else:
                                    progress_data = {}
                                if item_name in progress_data:
                                    progress_data[item_name] = progress_data[item_name] - delivered_amount
                                else:
                                    print("Item not found in progress list. Did you spell it correctly?")
                                # Write updated progress to file
                                with open("Construction_progress.json", "w") as update_file:
                                    json.dump(progress_data, update_file, indent=4)
                                    ready_to_print = True
                            except (json.JSONDecodeError, FileNotFoundError) as e:
                                print(f"Error updating Construction_progress.json: {e}")
                    #loops through every time to find which one/s have been only partially removed from cargo.json
                    for item_name, item_count in current_cargo_data.items():
                        if docked_at_construction:
                            if item_count < updated_cargo.get(item_name, 0):
                                delivered_amount = updated_cargo[item_name] - item_count
                                #appends items names and amounts to a list used to update progress and to display
                                item_name_list.append(item_name)
                                item_count_list.append(delivered_amount)
                                # attempts to update Construction_progress.json
                                try:
                                    if os.path.isfile("Construction_progress.json"):
                                        with open("Construction_progress.json", "r") as progress_file:
                                            progress_data = json.load(progress_file)
                                    else:
                                        progress_data = {}
                                    if item_name in progress_data:
                                        progress_data[item_name] = progress_data[item_name] - delivered_amount
                                    else:
                                        print("Item not found in progress list. Did you spell it correctly?")
                                    with open("Construction_progress.json", "w") as update_file:
                                        json.dump(progress_data, update_file, indent=4)
                                        ready_to_print = True
                                except (json.JSONDecodeError, FileNotFoundError) as e:
                                    print(f"Error updating Construction_progress.json: {e}")
                        #just displays amounts of commodities bought/transferred or stored. Serves no other function
                        elif ship_docked and not docked_at_construction:
                            if item_name not in updated_cargo:
                                print(f"New cargo detected. Bought/transferred: {item_name} - {item_count} tonnes")
                            elif item_count > updated_cargo.get(item_name, 0):
                                print(f"Bought/transferred {item_name}: {item_count - updated_cargo[item_name]} tonnes")
                            elif item_count < updated_cargo.get(item_name, item_count):
                                print(f"Stored: {updated_cargo[item_name] - item_count} tonnes of {item_name}")     
                    #updates cargo data
                    updated_cargo = current_cargo_data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading cargo file: {e}")
        if ready_to_print == True:
            print_construction_progress()
            ready_to_print = False
    time.sleep(0.1)

#displays the construction delivery progress
def print_construction_progress():
    global ship_cargo_space
    global total
    global docked_at_construction
    global ship_docked
    global item_name_list
    global item_count_list
    loops = 0
    total = 0
    clear_screen()
    timestamp = generate_one_time_timestamp()
    print("\n" + "-" * 60)
    print(f"Timestamp: {timestamp}")
    print("\n" + "-" * 60)
    try:
        with open('Construction_progress.json', "r") as progress:
            progress_data = json.load(progress)
            for item, count in progress_data.items():
                total += int(count)
                if count > 0:
                    if item == "terrainenrichmentsystems":
                        print(f"    Landenrichmentsystems: {count} - Landenrichmentsystems")
                    else:
                        print(f"    {item.capitalize()}: {count}")
                elif count < 0:
                    if item == "terrainenrichmentsystems":
                        print(f"    Landenrichmentsystems: {count} - Landenrichmentsystems")
                    else:
                        print(f"    ✔!  {item.capitalize()}: {count} - Overdelivered! Did someone else help deliver?")
                elif count == 0:
                    if item == "terrainenrichmentsystems":
                        print(f"    Landenrichmentsystems: {count} - Landenrichmentsystems")
                    else:
                        print(f"    ✔  {item.capitalize()}: {count}")
        print("\n" + "-" * 60)
        trips_left = total/ship_cargo_space
        trips_left = math.ceil(trips_left)
        print(f"{trips_left} trips left")
        print("\n" + "-" * 60)
        if docked_at_construction:
            for item in item_name_list:
                if item_name_list[loops] == "terrainenrichmentsystems":
                    print(f"Delivered {item_count_list[loops]} of Landenrichmentsystems")
                print(f"Delivered {item_count_list[loops]} of {item_name_list[loops]}")
                loops += 1
            item_name_list.clear()
            item_count_list.clear()
            loops = 0 
    except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error reading cargo file: {e}")

clear_screen()
print('ED Construction helper v0.6.0-beta \n Type "help" for a list of commands')
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()
global journal_folder
journal_folder = config['JOURNAL_PATH']['path']
journal_file_path = get_latest_journal()
if journal_file_path == "None":
    print("No journal files found. Exiting...")
    time.sleep(1)
    close_app()
if not journal_file_path:
    print("No journal files found.")
    time.sleep(1)
    close_app()
app_mode_selection()
global initialized
global input_started
global ship_docked
global opened_json
global t1
global docked_at_construction
global file_detected
global updated_cargo
global all_comodities
global ship_cargo_space
global switched
ship_cargo_space = 0
#nice list down there huh?
all_comodities = [
    "Agronomic Treatment",
    "Explosives",
    "Hydrogen Fuel",
    "Hydrogen Peroxide",
    "Liquid Oxygen",
    "Mineral Oil",
    "Nerve Agents",
    "Pesticides",
    "Rockforth Fertiliser",
    "Surface Stabilisers",
    "Synthetic Reagents",
    "Tritium",
    "Water",
    "Clothing",
    "Consumer Technology",
    "Domestic Appliances",
    "Evacuation Shelter",
    "Survival Equipment",
    "Algae",
    "Animal Meat",
    "Coffee",
    "Fish",
    "Food Cartridges",
    "Fruit and Vegetables",
    "Grain",
    "Synthetic Meat",
    "Tea",
    "Ceramic Composites",
    "CMM Composite",
    "Insulating Membrane",
    "Meta-Alloys",
    "Micro-Weave Cooling Hoses",
    "Neofabric Insulation",
    "Polymers",
    "Semiconductors",
    "Superconductors",
    "Beer",
    "Bootleg Liquor",
    "Liquor",
    "Narcotics",
    "Onionhead Gamma Strain",
    "Tobacco",
    "Wine",
    "Articulation Motors",
    "Atmospheric Processors",
    "Building Fabricators",
    "Crop Harvesters",
    "Emergency Power Cells",
    "Energy Grid Assembly",
    "Exhaust Manifold",
    "Geological Equipment",
    "Heatsink Interlink",
    "HN Shock Mount",
    "Magnetic Emitter Coil",
    "Marine Equipment",
    "Microbial Furnaces",
    "Mineral Extractors",
    "Modular Terminals",
    "Power Converter",
    "Power Generators",
    "Power Transfer Bus",
    "Radiation Baffle",
    "Reinforced Mounting Plate",
    "Skimmer Components",
    "Thermal Cooling Units",
    "Water Purifiers",
    "Advanced Medicines",
    "Agri-Medicines",
    "Basic Medicines",
    "Combat Stabilisers",
    "Performance Enhancers",
    "Progenitor Cells",
    "Aluminium",
    "Beryllium",
    "Bismuth",
    "Cobalt",
    "Copper",
    "Gallium",
    "Gold",
    "Hafnium 178",
    "Indium",
    "Lanthanum",
    "Lithium",
    "Osmium",
    "Palladium",
    "Platinum",
    "Platinum Alloy",
    "Praseodymium",
    "Samarium",
    "Silver",
    "Tantalum",
    "Thallium",
    "Thorium",
    "Titanium",
    "Uranium",
    "Alexandrite",
    "Bauxite",
    "Benitoite",
    "Bertrandite",
    "Bromellite",
    "Coltan",
    "Cryolite",
    "Gallite",
    "Goslarite",
    "Grandidierite",
    "Indite",
    "Jadeite",
    "Lepidolite",
    "Lithium Hydroxide",
    "Low Temperature Diamonds",
    "Methane Clathrate",
    "Methanol Monohydrate Crystals",
    "Moissanite",
    "Monazite",
    "Musgravite",
    "Painite",
    "Pyrophyllite",
    "Rhodplumsite",
    "Rutile",
    "Serendibite",
    "Taaffeite",
    "Uraninite",
    "Void Opals",
    "AI Relics",
    "Ancient Artefact",
    "Ancient Key",
    "Anomaly Particles",
    "Antimatter Containment Unit",
    "Antique Jewellery",
    "Antiquities",
    "Assault Plans",
    "Black Box",
    "Commercial Samples",
    "Damaged Escape Pod",
    "Data Core",
    "Diplomatic Bag",
    "Earth Relics",
    "Encrypted Correspondence",
    "Encrypted Data Storage",
    "Experimental Chemicals",
    "Fossil Remnants",
    "Gene Bank",
    "Geological Samples",
    "Guardian Casket",
    "Guardian Orb",
    "Guardian Relic",
    "Guardian Tablet",
    "Guardian Totem",
    "Guardian Urn",
    "Hostage",
    "Large Survey Data Cache",
    "Military Intelligence",
    "Military Plans",
    "Mollusc Brain Tissue",
    "Mollusc Fluid",
    "Mollusc Membrane",
    "Mollusc Mycelium",
    "Mollusc Soft Tissue",
    "Mollusc Spores",
    "Mysterious Idol",
    "Occupied Escape Pod",
    "Personal Effects",
    "Pod Core Tissue",
    "Pod Dead Tissue",
    "Pod Mesoglea",
    "Pod Outer Tissue",
    "Pod Shell Tissue",
    "Pod Surface Tissue",
    "Pod Tissue",
    "Political Prisoner",
    "Precious Gems",
    "Prohibited Research Materials",
    "Prototype Tech",
    "Rare Artwork",
    "Rebel Transmissions",
    "SAP 8 Core Container",
    "Scientific Research",
    "Scientific Samples",
    "Small Survey Data Cache",
    "Space Pioneer Relics",
    "Tactical Data",
    "Technical Blueprints",
    "Thargoid Basilisk Tissue Sample",
    "Thargoid Biological Matter",
    "Thargoid Bio-Storage Capsule",
    "Thargoid Cyclops Tissue Sample",
    "Thargoid Glaive Tissue Sample",
    "Thargoid Heart",
    "Thargoid Hydra Tissue Sample",
    "Thargoid Link",
    "Thargoid Orthrus Tissue Sample",
    "Thargoid Probe",
    "Thargoid Resin",
    "Thargoid Sensor",
    "Thargoid Medusa Tissue Sample",
    "Thargoid Scout Tissue Sample",
    "Thargoid Technology Samples",
    "Time Capsule",
    "Titan Deep Tissue Sample",
    "Titan Maw Deep Tissue Sample",
    "Titan Maw Partial Tissue Sample",
    "Titan Maw Tissue Sample",
    "Titan Partial Tissue Sample",
    "Titan Tissue Sample",
    "Trade Data",
    "Trinkets of Hidden Fortune",
    "Unclassified Relic",
    "Unoccupied Escape Pod",
    "Unstable Data Core",
    "Wreckage Components",
    "Imperial Slaves",
    "Slaves",
    "Advanced Catalysers",
    "Animal Monitors",
    "Aquaponic Systems",
    "Auto Fabricators",
    "Bioreducing Lichen",
    "Computer Components",
    "H.E. Suits",
    "Hardware Diagnostic Sensor",
    "Ion Distributor",
    "Land Enrichment Systems",
    "Medical Diagnostic Equipment",
    "Micro Controllers",
    "Muon Imager",
    "Nanobreakers",
    "Resonating Separators",
    "Robotics",
    "Structural Regulators",
    "Telemetry Suite",
    "Conductive Fabrics",
    "Leather",
    "Military Grade Fabrics",
    "Natural Fabrics",
    "Synthetic Fabrics",
    "Biowaste",
    "Chemical Waste",
    "Scrap",
    "Toxic Waste",
    "Battle Weapons",
    "Landmines",
    "Non-Lethal Weapons",
    "Personal Weapons",
    "Reactive Armour",
    "Terrain Enrichment Systems",
    "Steel"
]
cargo_file = os.path.join(journal_folder, "Cargo.json")
try:
    with open(cargo_file, "r") as cargo:
        cargo_data = json.load(cargo)
        current_cargo_list = cargo_data.get("Inventory", [])
        current_cargo_data = {item['Name']: item['Count'] for item in current_cargo_list}
except json.JSONDecodeError:
    print(f"Json decode error")
updated_cargo = current_cargo_data
file_detected = True
docked_at_construction = False
opened_json = False
ship_docked = False
switched = False
input_started = False
initialized = False
just_started = True
try:
    with open(journal_file_path) as f:
        f.seek(0, os.SEEK_END)
        while True:
            lines = f.readlines()
            if not lines and just_started == False and app_mode != "1":
                time.sleep(0.1)
                continue
            if app_mode == "3":
                just_started = False
                if input_started == False:
                    input_started = True
                log_mode()
            elif app_mode == "2":
                just_started = False
                tracking_mode()
            elif app_mode == "1":
                just_started = False
                colonisation_tracker()
                time.sleep(0.3)
except json.JSONDecodeError:
    print(f"Json decode error")
            
            