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
from datetime import datetime
from tzlocal import get_localzone
import pytz
import shutil
import math

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
    #time.sleep(1)
    return newest_file

def user_input():
    #time.sleep(1)
    global app_mode
    global ship_docked
    global docked_at_construction
    global ship_cargo_space
    while True:
        with patch_stdout():
            usr_input = prompt("> ", cursor=CursorShape.BLINKING_BLOCK)
            if usr_input == "exit":
                print("Exiting program...")
                time.sleep(1)
                close_app()
            elif usr_input == "help":
                print("List of commands: \n exit - exits the program \n app-mode-1 - switches app to journal monitoring mode \n app-mode-2 - switches to app to shopping list mode \n app-mode-3 - switches to construction progress tracking \n edit-shopping-list - allows you to edit shopping list in-app \n override-docked - overrides docked status in mode 3 \n override-docked-construction - overrides if you are docked at a constructions site / megaship (any cargo removed from your hold will be counted towards progress to buiding)")
            elif usr_input == "app-mode-1":
                app_mode = "1"
            elif usr_input == "app-mode-2":
                app_mode = "2"
            elif usr_input == "app-mode-3":
                app_mode = "3"
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
                ship_cargo_space = prompt("How much cargo space does your ship have? \n> ")
            else:
                print('Error. Invalid command. Type "help" for a list of commands')
            
def edit_list():
    if not os.path.isfile('progress.json'):
        print("Error no list detected, please make one first")
    else:
        with open('progress.json', 'r') as readfile:
            loaded_list = json.load(readfile)
            option = prompt("1- Edit/Add \n2-Remove \n")
            if option == "1":
                key = prompt("Commodity name in all lower case and no spaces: \n")
                value = prompt("New amount needed: \n")
                key = key.strip()
                value = value.strip()
                key = key.replace(" ", "")
                key = key.replace("-", "")
                loaded_list[key.lower()] = int(value)
            elif option == "2":
                key = prompt("Commodity name in all lower case and no spaces: \n")
                key = key.strip()
                key = key.replace(" ", "")
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
    if not os.path.isfile('Construction_progress.json'):
        print("Error no list detected, please make one first")
    else:
        with open('Construction_progress.json', 'r') as readfile:
            loaded_list = json.load(readfile)
            option = prompt("1- Edit/Add \n2-Remove \n")
            if option == "1":
                key = prompt("Commodity name in all lower case and no spaces: \n")
                value = prompt("New amount to deliver: \n")
                key = key.strip()
                value = value.strip()
                key = key.replace(" ", "")
                loaded_list[key.lower()] = int(value)
            elif option == "2":
                key = prompt("Commodity name in all lower case and no spaces: \n")
                key = key.strip()
                key = key.replace(" ", "")
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

            

def start_user_input():
    t1 = threading.Thread(target=user_input, daemon=True)
    t1.start()
                
def close_app():
    os._exit(0)

def app_mode_selection():
    global app_mode
    app_mode = prompt("Select app mode: \n 1-Journal monitor \n 2-Shopping list (W.I.P) \n 3-Colonisation construction tracker (W.I.P) \n exit-exits the app \n : ", cursor=CursorShape.BLINKING_BLOCK)
    if app_mode == "exit":
        close_app()

def convert_timestamp(ed_timestamp):
    utc_time = datetime.strptime(ed_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = pytz.utc.localize(utc_time)
    local_tz = get_localzone()
    local_time = utc_time.astimezone(local_tz)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

def log_mode():
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
    if not os.path.isfile('progress.json') and initialized == 0:
        #initial_list = {"aluminium":7143, "buildingfabricators":394, "ceramiccomposites":816, "cmmcomposite":6800, "computercomponents":98, "copper":390, "emergencypowercells":71, "evacuationshelter":203, "foodcartridges":139, "fruitandvegetables":97, "liquidoxygen":2455, "medicaldiagnosticequipment":46, "nonleathalweapons":33, "polymers":672, "powergenerators":70, "semiconductors":101, "steel":10659, "structuralregulators":665, "superconductors":134, "surfacestabilisers":603, "survivalequipment":57, "landenrichmentsystems":69, "titanium":5498}
        initial_list = {}
        item_amount = int(prompt("How many items do you plan on buying? \n"))
        i = 0
        for i in range(item_amount):
            key = prompt("Commodity name in all lower case and no spaces: \n")
            value = prompt("Amount needed: \n")
            key = key.strip()
            value = value.strip()
            key = key.replace(" ", "")
            key = key.replace("-", "")
            initial_list[key.lower()] = int(value)
        formatted_list = json.dumps(initial_list, indent=4)
        with open("progress.json", "w") as outfile:
            outfile.write(formatted_list)
        print("created progress file")
        print_list()
        initialized = 1
    elif initialized == 0:
        with open('progress.json', 'r') as openfile:
            initial_list = json.load(openfile)
            formatted_list = json.dumps(initial_list, indent=4)
            initialized = 1
            clear_screen()
            ship_cargo_space = int(prompt("Type the cargo capacity of your ship:\n> ", cursor=CursorShape.BLINKING_BLOCK))
            clear_screen()
            print_list()
    if input_started == 0:
        start_user_input()
        input_started = 1
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
                                #print("Materials:")
                                #for material, amount in initial_list.items():
                                #    print(f"    {material.capitalize()}: {amount}")
                                ##print(formatted_list)
                                #print("\n" + "-" * 60)
                                print_list()
                                print(curr_material.capitalize() + " remaining: " + str(new_amount))
                            elif event.get('event') == "Shutdown":
                                game_shutdown()
                except json.JSONDecodeError:
                    print(f"Skipping invalid line: {line}")
                    continue
def print_list():
    global ship_cargo_space
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
        print(f"    {material.capitalize()}: {amount}")
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
    print("Need to create file")
    progress_list = {}
    copy_progress = prompt("Copy from shopping list? (Progress.json) y/n \n> ", cursor=CursorShape.BLINKING_BLOCK)
    if copy_progress == "y":
        shutil.copyfile('progress.json', 'Construction_progress.json')
    elif copy_progress == "n":
        item_amount = int(prompt("How many different commodities do you need for construction? \n> ", cursor=CursorShape.BLINKING_BLOCK))
        for i in range(item_amount):
            key = prompt("Commodity name in all lower case and no spaces: \n")
            value = prompt("Amount needed: \n")
            key = key.strip()
            value = value.strip()
            key = key.replace(" ", "")
            progress_list[key.lower()] = int(value)
        formatted_list = json.dumps(progress_list, indent=4)
        with open("Construction_progress.json", "w") as outfile:
            outfile.write(formatted_list)

def colonisation_tracker():
    global opened_json
    global journal_folder
    global ship_docked
    global docked_at_construction
    global input_started
    global updated_cargo
    global initialized
    global ship_cargo_space
    if initialized == 0:
        clear_screen()
        ship_cargo_space = int(prompt("Type the cargo capacity of your ship:\n> ", cursor=CursorShape.BLINKING_BLOCK))
        print_construction_progress()
        print("Helpful comands:\nhelp\noverride-docked\noverride-docked-construction")
        initialized = 1
    if not os.path.isfile("Construction_progress.json"):
        with open("Construction_progress.json", "w") as progress_file:
            create_progress_tracking()
    # Start user input if not started
    if input_started == 0:
        start_user_input()
        input_started = 1
    cargo_file = os.path.join(journal_folder, "Cargo.json")
    for line in lines:
        try:
            curr_event = ndjson.loads(line.strip())
            for event in curr_event:
                if event.get('event') == "Docked":
                    print("Docked at a station")
                    ship_docked = True
                    if "colonisationcontribution" in event.get('StationServices', []):
                        print("Docked at a construction ship, tracking deliveries.")
                        docked_at_construction = True
                    else:
                        docked_at_construction = False
                elif event.get('event') == "Undocked":
                    ship_docked = False
                    docked_at_construction = False
                    print("Undocked from station")
                elif event.get('event') == "Shutdown":
                    game_shutdown()
        except json.JSONDecodeError:
            print(f"Skipping invalid line: {line}")
            continue
    if ship_docked:
        try:
            with open(cargo_file, "r") as cargo:
                cargo_data = json.load(cargo)
                current_cargo_list = cargo_data.get("Inventory", [])
                current_cargo_data = {item['Name']: item['Count'] for item in current_cargo_list}
                if current_cargo_data != updated_cargo:
                    #print("Cargo change detected")
                    for item_name, item_count in current_cargo_data.items():
                        if docked_at_construction:
                            if item_name not in updated_cargo:
                                print_construction_progress()
                                print(f"New cargo detected: {item_name} - {item_count} tonnes")
                            elif item_count > updated_cargo.get(item_name, 0):
                                print_construction_progress()
                                print(f"Bought/transferred {item_name}: {item_count - updated_cargo[item_name]} tonnes")
                            elif item_count < updated_cargo.get(item_name, 0):
                                print_construction_progress()
                                delivered_amount = updated_cargo[item_name] - item_count
                                print(f"Delivered: {delivered_amount} tonnes of {item_name}")
                                # Update Construction_progress.json
                                try:
                                    if os.path.isfile("Construction_progress.json"):
                                        with open("Construction_progress.json", "r") as progress_file:
                                            progress_data = json.load(progress_file)
                                    else:
                                        progress_data = {}
                                    # Update delivered amount
                                    if item_name in progress_data:
                                        progress_data[item_name] -= delivered_amount
                                    else:
                                        progress_data[item_name] = delivered_amount
                                    # Write updated progress to file
                                    with open("Construction_progress.json", "w") as update_file:
                                        json.dump(progress_data, update_file, indent=4)
                                except (json.JSONDecodeError, FileNotFoundError) as e:
                                    print(f"Error updating Construction_progress.json: {e}")
                        #print stuff for getting stuff from your carrier or buying it
                        elif ship_docked and not docked_at_construction:
                            print("Docked at regular sation/fleet carrier")
                            if item_name not in updated_cargo:
                                print_construction_progress()
                                print(f"New cargo detected: {item_name} - {item_count} tonnes")
                            elif item_count > updated_cargo.get(item_name, 0):
                                print_construction_progress()
                                print(f"Bought/transferred {item_name}: {item_count - updated_cargo[item_name]} tonnes")
                            elif item_count < updated_cargo.get(item_name, item_count):
                                print_construction_progress()
                                print(f"Stored: {updated_cargo[item_name] - item_count} tonnes of {item_name}")
                    if ship_docked and not docked_at_construction:
                        for item_name in list(updated_cargo.keys()):
                            if item_name not in current_cargo_data:
                                removed_amount = updated_cargo[item_name]
                                print_construction_progress()
                                print(f"Stored: {removed_amount} tonnes of {item_name} (Fully removed)")
                    if docked_at_construction:
                        for item_name in list(updated_cargo.keys()):
                            if item_name not in current_cargo_data:
                                removed_amount = updated_cargo[item_name]
                                try:
                                    if os.path.isfile("Construction_progress.json"):
                                        with open("Construction_progress.json", "r") as progress_file:
                                            progress_data = json.load(progress_file)
                                    else:
                                        progress_data = {}
                                    # Update delivered amount
                                    if item_name in progress_data:
                                        progress_data[item_name] -= removed_amount
                                    else:
                                        progress_data[item_name] = removed_amount
                                    # Write updated progress to file
                                    with open("Construction_progress.json", "w") as update_file:
                                        json.dump(progress_data, update_file, indent=4)
                                except (json.JSONDecodeError, FileNotFoundError) as e:
                                    print(f"Error updating Construction_progress.json: {e}")
                                print_construction_progress()
                                print(f"Delivered: {removed_amount} tonnes of {item_name}")
                        
                    updated_cargo = current_cargo_data  # Update cargo state
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading cargo file: {e}")
    time.sleep(0.1)

#def check_if_removed():
#    global updated_cargo
#    for item_name in list(updated_cargo.keys()):
#        if item_name not in current_cargo_data:
#            removed_amount = updated_cargo[item_name]
#            print_construction_progress()
#            print(f"Stored: {removed_amount} tonnes of {item_name} (Fully removed)")

def print_construction_progress():
    global ship_cargo_space
    global total
    total = 0
    clear_screen()
    timestamp = generate_one_time_timestamp()
    print("\n" + "-" * 60)
    print(timestamp)
    print("\n" + "-" * 60)
    try:
        with open('Construction_progress.json', "r") as progress:
            progress_data = json.load(progress)
            for item, count in progress_data.items():
                total += int(count)
                print(f"{item}: {count}")
        print("\n" + "-" * 60)
        trips_left = total/ship_cargo_space
        trips_left = math.ceil(trips_left)
        print(f"{trips_left} trips left")
        print("\n" + "-" * 60)
    except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error reading cargo file: {e}")

clear_screen()
print('ED Colonisation helper v0.4.1-alpha \n Type "help" for a list of commands')
if not os.path.isfile('config.ini'):
    path = input("Input game journal file path without quotes:  \n")
    config = configparser.ConfigParser() #initiates config parser
    config['JOURNAL_PATH'] = {'path': path} #creates section, key and value
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Config file created. Please restart the program.")
    time.sleep(1)
    close_app()
else:
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
    input_started = 0
    initialized = 0
    just_started = 1
    #time.sleep(0.5)
    try:
        with open(journal_file_path) as f:
            f.seek(0, os.SEEK_END)
            while True:
                lines = f.readlines()
                if not lines and just_started == 0:
                    time.sleep(0.1)
                    continue
                if app_mode == "1":
                    just_started = 0
                    if input_started == 0:
                        start_user_input()
                        input_started = 1
                    log_mode()
                elif app_mode == "2":
                    just_started = 0
                    tracking_mode()
                elif app_mode == "3":
                    just_started = 0
                    #delivery_tracker()
                    colonisation_tracker()
    except json.JSONDecodeError:
        print(f"Json decode error")
                
                
