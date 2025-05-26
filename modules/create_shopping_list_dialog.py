from . import state, create_progress_file
from dialogs import autocomplete_item_list_popup, quantity_dialog, item_count_dialog, copy_dialog
from PySide6.QtWidgets import QDialog
import re

def open_input_dialog(self):
    count_dialog = item_count_dialog.Item_count(self)
    if count_dialog.exec() == QDialog.Accepted:
        amount = count_dialog.get_input()
        print(amount)
        i = 0
        while i < amount:
            items = state.all_comodities
            dialog = autocomplete_item_list_popup.AutoCompleteInputDialog(items, parent=self)
            if dialog.exec() == QDialog.Accepted:
                self.text_user = dialog.get_input()
                key = dialog.get_input().lower().strip().replace(" ", "")
                key = re.sub(r'[^a-zA-Z0-9]', '', key)
                quant_dialog = quantity_dialog.Quantity(parent=self)
                if quant_dialog.exec() == QDialog.Accepted:
                    value = int(quant_dialog.get_input())
                    state.progress_list[key] = value
                    i += 1
        print(state.progress_list)
        create_progress_file.create_progress_tracking()
        #copy_list_dialog = copy_dialog.ListCopy(parent=self)
        #copy_list_dialog.exec()