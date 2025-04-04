from modules import clean_screen, state, generate_time_timestamp
import json
import math

def print_construction_progress():
    loops = 0
    total = 0
    clean_screen.clear_screen()
    timestamp = generate_time_timestamp.generate_one_time_timestamp()
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
        trips_left = total/state.ship_cargo_space
        trips_left = math.ceil(trips_left)
        print(f"{trips_left} trips left")
        print("\n" + "-" * 60)
        if state.docked_at_construction:
            for item in state.item_name_list:
                if state.item_name_list[loops] == "terrainenrichmentsystems":
                    print(f"Delivered {state.item_count_list[loops]} of Landenrichmentsystems")
                print(f"Delivered {state.item_count_list[loops]} of {state.item_name_list[loops]}")
                loops += 1
            state.item_name_list.clear()
            state.item_count_list.clear()
            loops = 0 
    except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error reading cargo file: {e}")
