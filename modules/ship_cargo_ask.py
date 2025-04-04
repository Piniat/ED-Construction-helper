from prompt_toolkit import prompt
from modules import state

def request_ship_cargo():
    state.ship_cargo_space = int(prompt("How much cargo space does your ship have? \n> "))
