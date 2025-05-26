import math
import json
from . import state, create_timestamp

def print_list(self):
    self.html_output = ""
    self.extra = ""
    self.trips = ""
    self.str_percent = ""
    self.html_output += f"<hr>{create_timestamp.generate_one_time_timestamp()}<hr>"
    state.total = 0
    with open('Shopping_list.json', 'r') as openfile:
        initial_list = json.load(openfile)
    max_item_length = max(len(item) for item in initial_list)
    for material, amount in initial_list.items():
        state.total += amount
        if amount > 0:
            self.html_output += f"{material.capitalize():<{max_item_length}}: {amount}<br>"
        elif amount == 0:
            self.html_output += f"✔  {material.capitalize():<{max_item_length - 3}}: {amount}<br>"
        elif amount < 0:
            self.html_output += f"✔!  {material.capitalize():<{max_item_length - 4}}: {amount} - overstock!<br>"
    trips_left = state.total/state.ship_cargo_space
    trips_left = math.ceil(trips_left)
    if trips_left != 1:
        self.trips = f"Trips left: {trips_left}"
    else:
        self.trips = f"{trips_left} trip left"
    self.str_percent = '<html><head/><body><p><span style=" font-size:16pt; font-weight:700;">Unavailable</span></p></body></html>'
    state.ready_to_update = True