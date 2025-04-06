from prompt_toolkit import prompt
from modules import state
from prompt_toolkit.cursor_shapes import CursorShape

def request_ship_cargo():
    try:
        state.ship_cargo_space = int(prompt("How much cargo space does your ship have? \n> ", cursor=CursorShape.BLINKING_BLOCK))
    except:
        print("Error, please give a valid number")
        request_ship_cargo()
