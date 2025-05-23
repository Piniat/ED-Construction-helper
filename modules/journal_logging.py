from . import state
import time
import json
import os

def display_event(self):
    self.event = ""
    with open(state.journal_file_path, "r") as f:
        f.seek(0, os.SEEK_END)  # start at end to only get new lines

        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            try:
                #self.event.clear()
                curr_event = json.loads(line.strip())
                state.event = curr_event
                print(state.event.get('event'))
                timestamp = state.event.get('timestamp')
                # You can convert timestamp here if needed

                event_name = state.event.get('event')

                if event_name == "Shutdown":
                    self.event = event_name + "\n"
                elif event_name == "StartJump":
                    self.event = event_name + "\n"
                elif event_name == "Docked":
                    self.event = event_name + "\n"
                elif event_name == "Undocked":
                    self.event = event_name + "\n"
                elif event_name == "DockingCancelled":
                    self.event = event_name + "\n"
                elif event_name == "DockingDenied":
                    self.event = event_name + "\n"
                elif event_name == "DockingGranted":
                    self.event = event_name + "\n"
                elif event_name == "DockingTimeout":
                    self.event = event_name + "\n"
                elif event_name == "Music":
                    self.event = event_name + "\n"
                elif event_name == "Commander":
                    self.event = event_name + "\n"
                elif event_name == "Resurrect":
                    self.event = event_name + "\n"
                elif event_name == "Friends":
                    self.event = event_name + "\n"
                elif event_name == "Materials":
                    self.event = event_name + "\n"
                elif event_name == "fileheader":
                    self.event = event_name + "\n"
                elif event_name == "Rank":
                    self.event = event_name + "\n"
                elif event_name == "MarketBuy":
                    self.event = event_name + "\n"
                elif event_name == "MissionAccepted":
                    self.event = event_name + "\n"
                elif event_name == "MissionCompleted":
                    self.event = event_name + "\n"
                elif event_name == "CarrierStats":
                    self.event = event_name + "\n"
                else:
                    self.event = event_name + "unhandled \n"

                print(self.event)

            except json.JSONDecodeError:
                print(f"Skipping invalid line: {line.strip()}")
                continue
