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
    print("Delivery tracking mode")
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
                        print(f"    ✔!  Landenrichmentsystems: {count} - Landenrichmentsystems")
                    else:
                        print(f"    ✔!  {item.capitalize()}: {count} - Overdelivered! Did someone else help deliver?")
                elif count == 0:
                    if item == "terrainenrichmentsystems":
                        print(f"    ✔  Landenrichmentsystems: {count} - Landenrichmentsystems")
                    else:
                        print(f"    ✔  {item.capitalize()}: {count}")
        print("\n" + "-" * 60)
        trips_left = total/state.ship_cargo_space
        trips_left = math.ceil(trips_left)
        print(f"{trips_left} trips left\n")
        print(f"{state.percent_complete}% of construction complete")
        print("\n" + "-" * 60)
        #if state.contributed_display_name != []:
        for item in state.contributed_display_name:
             print(f"{state.contributed_display_amount[loops]} tonnes of {state.contributed_display_name[loops]} delivered")
             loops += 1
             state.contributed_display_name.clear()
             state.contributed_display_amount.clear()
    except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error reading cargo file: {e}")
