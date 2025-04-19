import math
import json
from modules import state, generate_time_timestamp, clean_screen, ship_cargo_ask

def print_list():
    if state.ship_cargo_space == 0:
        ship_cargo_ask.request_ship_cargo()
    state.total = 0
    with open('progress.json', 'r') as openfile:
        initial_list = json.load(openfile)
    timestamp = generate_time_timestamp.generate_one_time_timestamp()
    clean_screen.clear_screen()
    print("\n" + "-" * 60)
    #print("this is the intended timestamp in print_shopping_list")
    print(f"Timestamp: {timestamp}")
    print("\n" + "-" * 60)
    print("Shopping list mode")
    print("\n" + "-" * 60)
    print("Materials:")
    max_item_length = max(len(item) for item in initial_list)
    for material, amount in initial_list.items():
        state.total += amount
        if amount > 0:
            print(f"{material.capitalize():<{max_item_length}}: {amount}")
        elif amount == 0:
            print(f"✔  {material.capitalize():<{max_item_length - 3}}: {amount}")
        elif amount < 0:
            print(f"✔!  {material.capitalize():<{max_item_length - 4}}: {amount} - overstock!")
    print("\n" + "-" * 60)
    trips_left = state.total/state.ship_cargo_space
    trips_left = math.ceil(trips_left)
    print(f"{trips_left} total trips left")
    print("\n" + "-" * 60)