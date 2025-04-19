from . import state, exit_app, elite_timestamp
import time

def template():
    print("\n" + "-" * 60)
    timestamp = state.event.get('timestamp')
    ed_timestamp=timestamp
    print(f"{'Timestamp':<20}: {elite_timestamp.convert_timestamp(ed_timestamp)}")
    print(f"{'event':<20}: {state.event.get('event')}")

def unhandled_event():
    print("\n" + "-" * 60)
    print("[Unhandled event]: " + state.event.get('event'))

def game_shutdown():
    template()
    print("\nGame shutdown detected. Exiting...")
    time.sleep(1)
    exit_app.close_app()
        
def start_jump():
    template()
    print(f"{'Destination':<20}: {state.event.get('StarSystem')}")
    print(f"{'Star type':<20}: {state.event.get('StarClass')}")

def docked():
    template()
    print(f"{'Station Name':<20}: {state.event.get('StationName')}")
    print(f"{'Station Type':<20}: {state.event.get('StationType')}")

def undocked():
    template()
    print(f"{'Station Name':<20}: {state.event.get('StationName')}")
    print(f"{'Station Type':<20}: {state.event.get('StationType')}")

def docking_cancelled():
    template()
    print(f"{'Station Name':<20}: {state.event.get('StationName')}")
    print(f"{'Station Type':<20}: {state.event.get('StationType')}")

def docking_denied():
    template()
    print(f"{'Station Name':<20}: {state.event.get('StationName')}")
    print(f"{'Station Type':<20}: {state.event.get('StationType')}")
    print(f"{'Reason':<20}: {state.event.get('Reason')}")

def docking_granted():
    template()
    print(f"{'Station Name':<20}: {state.event.get('StationName')}")
    print(f"{'Station Type':<20}: {state.event.get('StationType')}")
    print(f"{'Pad':<20}: {state.event.get('LandingPad')}")

def docking_timeout():
    template()
    print(f"{'Station Name':<20}: {state.event.get('StationName')}")
    print(f"{'Station Type':<20}: {state.event.get('StationType')}")

def music():
    template()
    print(f"{'Music Track':<20}: {state.event.get('MusicTrack')}")

def commander():
    template()
    print(f"{'Name':<20}: {state.event.get('Name')}")
    print(f"{'Player id':<20}: {state.event.get('FID')}")

def resurrect():
    template()
    print(f"{'Option':<20}: {state.event.get('Option')}")
    print(f"{'Cost':<20}: {state.event.get('Cost')}")
    print(f"{'Bankrupt':<20}: {state.event.get('Bankrupt')}")

def death():
    template()
    print(f"{'Killer name':<20}: {state.event.get('KillerName')}")
    print(f"{'Killer ship':<20}: {state.event.get('KillerShip')}")
    print(f"{'Killer rank':<20}: {state.event.get('KillerRank')}")

def friends():
    template()
    print(f"{'Name':<20}: {state.event.get('Name')}")
    print(f"{'Status':<20}: {state.event.get('Status')}")

def materials():
    template()
    raw_array = state.event.get('Raw')
    print("\n" + "*" * 30 + "\n Raw")
    for name in raw_array:
        print(f"{name['Name']:<20}: {name['Count']}")
    manu_array = state.event.get('Manufactured')
    print("\n" + "*" * 30 + "\n Manufactured")
    for name in manu_array:
        print(f"{name['Name']:<20}: {name['Count']}")
    encoded_array = state.event.get('Encoded')
    print("\n" + "*" * 30 + "\n Encoded")
    for name in encoded_array:
        print(f"{name['Name']:<20}: {name['Count']}")
    
def header():
    template()
    print(f"{'Part':<20}: {state.event.get('part')}")
    print(f"{'Language':<20}: {state.event.get('language')}")
    print(f"{'Game version':<20}: {state.event.get('gameversion')}")
    print(f"{'Build':<20}: {state.event.get('build')}")

def rank():
    template()
    print(f"{'Combat':<20}: {state.event.get('Combat')}")
    print(f"{'Trade':<20}: {state.event.get('Trade')}")
    print(f"{'Exploration':<20}: {state.event.get('Explore')}")
    print(f"{'CQC':<20}: {state.event.get('CQC')}")

def marketbuy():
    template()
    print(f"{'MarketID':<20}: {state.event.get('MarketID')}")
    print(f"{'Type':<20}: {state.event.get('Type')}")
    print(f"{'Count':<20}: {state.event.get('Count')}")
    print(f"{'Buy Price':<20}: {state.event.get('BuyPrice')}")
    print(f"{'Total Cost':<20}: {state.event.get('TotalCost')}")

def missionaccepted():
    template()
    print(f"{'Type':<20}: {state.event.get('LocalisedName')}")
    print(f"{'Faction':<20}: {state.event.get('Faction')}")
    print(f"{'Mission ID':<20}: {state.event.get('MissionID')}")
    print(f"{'Influence':<20}: {state.event.get('Influence')}")
    print(f"{'Reputation':<20}: {state.event.get('Reputation')}")
    print(f"{'Reward':<20}: {state.event.get('Reward')}CR")
    print(f"{'Wing':<20}: {state.event.get('Wing')}")

def missioncompleted():
    template()
    print(f"{'Name':<20}: {state.event.get('Name')}")
    print(f"{'Faction':<20}: {state.event.get('Faction')}")
    print(f"{'Mission ID':<20}: {state.event.get('MissionID')}")
    print(f"{'Reward':<20}: {state.event.get('Reward')}CR")