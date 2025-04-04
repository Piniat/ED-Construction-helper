from modules import state, exit_app
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit import prompt

def app_mode_selection():
    state.app_mode = prompt("Select app mode: \n 1-Colonisation construction tracker \n 2-Shopping list \n 3-Journal monitor \n exit-exits the app \n : ", cursor=CursorShape.BLINKING_BLOCK)
    if state.app_mode == "exit":
        exit_app.close_app()
    elif state.app_mode not in ["1", "2", "3"]:
        print("Invalid mode. Please select 1, 2, or 3.")
        app_mode_selection()