from . import state

def set_journal_mode():
    state.app_mode = "journal"
    state.switched = True
    state.initialized = False

def set_delivery_tracker():
    state.app_mode = "delivery"
    state.switched = True
    state.initialized = False