import os
from . import state

def clear_screen(output_widget=None):
    if output_widget is not None:
        output_widget.clear()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

