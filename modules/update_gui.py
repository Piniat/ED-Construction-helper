from . import state

def update_lists(self):
    self.list_updated.emit("")
    self.information_panel.emit("")
    self.list_updated.emit(self.html_output)
    self.percent_html_updated.emit(self.str_percent)
    self.information_panel.emit('<html><head/><body><p><span style=" font-size:12pt;">' + self.extra + '</span></p></body></html>')
    self.progress_updated.emit(state.percent_complete)
    self.html_output = ""
    self.extra = ""

def display_journal_logs(self):
    all_events = ""
    count = 0
    for item in state.new_list:
        count += 1
    if count >= 100:
        state.new_list = []
    if (state.switched == True) or (state.initialized == False):
        state.new_list = []
        self.information_panel.emit("")
        #state.new_list += "Journal log mode <br>"
        state.new_list.append("Journal log mode <br>")
    else:
        #state.new_list += "Event: " + self.event + "<br>"
        state.new_list.append("Event: " + self.event + "<br>")
        print(state.new_list)
    all_events = "".join(state.new_list)
    self.list_updated.emit(all_events)
