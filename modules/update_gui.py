from . import state

def update_lists(self):
    self.list_updated.emit("")
    self.list_updated.emit(self.html_output)
    self.information_panel.emit("")
    self.percent_html_updated.emit(self.str_percent)
    self.information_panel.emit('<html><head/><body><p><span style=" font-size:12pt;">' + self.extra + '</span></p></body></html>')
    self.progress_updated.emit(state.percent_complete)
    self.html_output = ""
    self.extra = ""

def display_journal_logs(self):
    if (state.switched == True) or (state.initialized == False):
        state.new_list = ""
        self.information_panel.emit("")
        state.new_list += "Journal log mode <br>"
    else:
        state.new_list += "Event: " + self.event + "<br>"
        print(state.new_list)
    self.list_updated.emit(state.new_list)
