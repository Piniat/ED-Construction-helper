from . import state, usr_input
import threading

def start_user_input():
    state.input_thread = threading.Thread(target=usr_input.user_input, daemon=True)
    state.input_thread.start()