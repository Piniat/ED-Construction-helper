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
            max_item_length = max(len(item) for item in progress_data)
            for item, count in progress_data.items():
                total += int(count)
                if count > 0:
                    print(f"{item.capitalize():<{max_item_length}}: {count:>{5}}")
                elif count < 0:
                    print(f"✔!  {item.capitalize():<{max_item_length - 3}}: {count:>{5}} - This shouldn't happen...")
                elif count == 0:
                    print(f"✔  {item.capitalize():<{max_item_length - 3}}: {count:>{5}}")
        print("\n" + "-" * 60)
        trips_left = total/state.ship_cargo_space
        trips_left = math.ceil(trips_left)
        print(f"{trips_left} trips left\n")
        if state.percent_complete == None:
            print("Percentage will be displayed on game journal update")
        else:
            #progress_bar = '█' * int(state.percent_complete * 0.2)  # Bar length will be out of 20 (adjust if needed)
            #remaining_bar = '░' * (20 - len(progress_bar))
            #print(f"Progress: [{progress_bar}{remaining_bar}] {state.percent_complete:.2f}%")
            print(f"Progress: {state.percent_complete}")
        print("\n" + "-" * 60)
        for item in state.contributed_display_name:
             print(f"{state.contributed_display_amount[loops]} tonnes of {state.contributed_display_name[loops]} delivered")
             loops += 1
             state.contributed_display_name.clear()
             state.contributed_display_amount.clear()
    except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error reading cargo file: {e}")