from . import state, update_gui
import json

def display_event(self):
    if (state.switched == True) or (state.initialized == False):
        update_gui.display_journal_logs(self)
        state.initialized = True
        state.switched = False
    self.event = ""
    try:
        #self.event.clear()
        curr_event = json.loads(state.line.strip())
        self.event = curr_event
        print(self.event.get('event'))
        timestamp = self.event.get('timestamp')
        # You can convert timestamp here if needed
        event_name = self.event.get('event')
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
            self.event = event_name + "\n"
        update_gui.display_journal_logs(self)
        #print(self.event)
    except json.JSONDecodeError:
        print(f"Skipping invalid line: {state.line.strip()}")