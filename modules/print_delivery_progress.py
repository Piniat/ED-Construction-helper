#from modules import clean_screen, state, generate_time_timestamp
import json
import math
from . import state, create_timestamp
import json

def print_construction_progress(self):
    loops = 0
    total = 0
    self.html_output = ""
    self.extra = ""
    self.trips = ""
    self.html_output += f"<hr>{create_timestamp.generate_one_time_timestamp()}<hr>"
    #self.html_output += "<hr>Mode: Delivery Tracking<br>"

    try:
        with open('Construction_progress.json', "r") as progress:
            progress_data = json.load(progress)
            max_item_length = max(len(item) for item in progress_data)
            for item, count in progress_data.items():
                if item != "dontprint":
                    total += int(count)
                    if count > 0:
                        self.html_output += f"{item.capitalize():<{max_item_length}}: {count:>{5}}<br>"
                    elif count < 0:
                        self.html_output += f"✔!  {item.capitalize():<{max_item_length - 4}}: {count:>{5}} - This shouldn't happen...<br>"
                    elif count == 0:
                        self.html_output += f"✔  {item.capitalize():<{max_item_length - 3}}: {count:>{5}} <br>"
                else:
                    self.html_output += "No progress file found. Please dock at construction to generate file"
        #self.html_output += "<hr>"
        trips_left = total/state.ship_cargo_space
        trips_left = math.ceil(trips_left)
        if trips_left != 1:
             self.trips = f"Trips left: {trips_left}"
        else:
              self.trips = f"{trips_left} trip left"
        #self.extra += "<hr><br>"
        if state.percent_complete is None:
            self.percent = '<html><head/><body><p><span style=" font-size:16pt; font-weight:700;">Awaiting data...</span></p></body></html>'
        else:
            state.percent_complete = round(state.percent_complete, 1)
            bar_length = 50
            percent_intiger = int(state.percent_complete)
            display_percent = str(state.percent_complete)
            self.str_percent = str('<html><head/><body><p><span style=" font-size:16pt; font-weight:700;">' + display_percent + '%</span></p></body></html>')
            if percent_intiger == 0:
                 block = 0
            else:
                 block = int((bar_length * percent_intiger) / 100)
            progress = "#" * block + "-" * (bar_length - block)
            self.percent = state.percent_complete
        for item in state.contributed_display_name:
            self.extra += f"{state.contributed_display_amount[loops]} tonnes of {state.contributed_display_name[loops]} delivered <br>"
            loops += 1
        state.contributed_display_name.clear()
        state.contributed_display_amount.clear()
        state.ready_to_update = True
    except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error reading cargo file: {e}")