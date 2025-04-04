from . import state, start_input, elite_timestamp, event_handler
import json
import ndjson

def log_mode():
    if state.input_started == False:
        print("attempting to start input")
        start_input.start_user_input()
        state.input_started = True
        print("Logging active!")
    for line in state.lines:
                try:
                    curr_event = ndjson.loads(line.strip())
                    for state.event in curr_event:
                        timestamp = state.event.get('timestamp')
                        ed_timestamp=timestamp
                        state.formatted_timestamp = elite_timestamp.convert_timestamp(ed_timestamp)
                        #convert_timestamp(ed_timestamp)
                        if state.event.get('event') == "Shutdown":
                            event_handler.game_shutdown()
                        elif state.event.get('event') == "StartJump":
                            event_handler.start_jump()
                        elif state.event.get('event') == "Docked":
                            event_handler.docked()
                        elif state.event.get('event') == "Undocked":
                            event_handler.undocked()
                        elif state.event.get('event') == "DockingCancelled":
                            event_handler.docking_cancelled()
                        elif state.event.get('event') == "DockingDenied":
                            event_handler.docking_denied()
                        elif state.event.get('event') == "DockingGranted":
                            event_handler.docking_granted()
                        elif state.event.get('event') == "DockingTimeout":
                            event_handler.docking_timeout()
                        elif state.event.get('event') == "Music":
                            event_handler.music()
                        elif state.event.get('event') == "Commander":
                            event_handler.commander()
                        elif state.event.get('event') == "Resurrect":
                            event_handler.resurrect()
                        elif state.event.get('event') == "Friends":
                            event_handler.friends()
                        elif state.event.get('event') == "Materials":
                            event_handler.materials()
                        elif state.event.get('event') == "fileheader":
                            event_handler.header()
                        elif state.event.get('event') == "Rank":
                            event_handler.rank()
                        elif state.event.get('event') == "MarketBuy":
                            event_handler.marketbuy()
                        else:
                            event_handler.unhandled_event()
                except json.JSONDecodeError:
                    print(f"Skipping invalid line: {line}")
                    continue