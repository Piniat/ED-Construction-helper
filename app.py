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
    time.sleep(1)
    return newest_file

def user_input():
    time.sleep(1)
    global app_mode
    while True:
        with patch_stdout():
            usr_input = prompt("> ", cursor=CursorShape.BLINKING_BLOCK)
            if usr_input == "exit":
                print("Exiting program...")
                time.sleep(1)
                close_app()
            elif usr_input == "help":
                print("List of commands: \n exit - exits the program \n app-mode-1 - switches app to journal monitoring mode \n app-mode-2 - switches to app to shopping list mode \n edit-shopping-list - allows you to edit shopping list in-app")
            elif usr_input == "app-mode-1":
                app_mode = "1"
            elif usr_input == "app-mode-2":
                app_mode = "2"
            elif usr_input == "edit-shopping-list":
                edit_list()
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
            #writefile.write(formatted_list)
        print("done!")
        print_list()
        #print("Working on it! For now please edit the progress.json to change remaining needed values and add/remove stuff)")
            

def start_user_input():
    t1 = threading.Thread(target=user_input, daemon=True)
    t1.start()
                
def close_app():
    os._exit(0)

def app_mode_selection():
    global app_mode
    app_mode = prompt("Select app mode: \n 1-Journal monitor \n 2-Shopping list (W.I.P) \n 3-W.I.P \n exit-exits the app \n : ", cursor=CursorShape.BLINKING_BLOCK)
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
                                print("Materials:")
                                for material, amount in initial_list.items():
                                    print(f"    {material.capitalize()}: {amount}")
                                #print(formatted_list)
                                print("\n" + "-" * 60)
                                print(curr_material.capitalize() + " remaining: " + str(new_amount))
                            elif event.get('event') == "Shutdown":
                                game_shutdown()
                except json.JSONDecodeError:
                    print(f"Skipping invalid line: {line}")
                    continue
def print_list():
    with open('progress.json', 'r') as openfile:
        initial_list = json.load(openfile)
    timestamp = generate_one_time_timestamp()
    clear_screen()
    print("\n" + "-" * 60)
    print(f"Timestamp: {timestamp}")
    print("\n" + "-" * 60)
    print("Materials:")
    for material, amount in initial_list.items():
        print(f"    {material.capitalize()}: {amount}")
    print("\n" + "-" * 60)

def generate_one_time_timestamp():
    local_tz = get_localzone()
    now = datetime.now(local_tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()
print('ED Colonisation helper v0.3.0-alpha (added editing shopping list) \n Type "help" for a list of commands')
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
    input_started = 0
    initialized = 0
    global t1
    just_started = 1
    time.sleep(0.5)
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
            else:
                just_started = 0
                print("Unimplemented")
                
