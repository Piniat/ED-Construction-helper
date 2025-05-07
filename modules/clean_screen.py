import os
from . import state

def clear_screen(gui_output=None):
    if state.is_gui == False:
        os.system('cls' if os.name == 'nt' else 'clear')

