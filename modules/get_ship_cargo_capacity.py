import ndjson
from . import state

def find_last_cargo_capacity():
    with open(state.journal_file_path, 'r') as f:
        reader = ndjson.reader(f)
        for event in reader:
            if event.get("event") == "Loadout":
                state.ship_cargo_space = event.get("CargoCapacity")