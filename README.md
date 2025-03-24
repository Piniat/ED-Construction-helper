# ED Construction helper
This app was made to track deliveries to colonisation constructions (colonisation megaships or construction sites) and track the gathering of materials using a shopping list. It's basically a self updating spreadsheet.<br>
### Important! Run the app after starting elite dangerous or it'll read outdated journal files.<br>
The app can currently:<br>
<ul>
  <li>Track deliveries to constructions</li>
  <li>Track the collection of items via marketbuy events</li>
  <li>Tell you the amount of trips remaining based on your ships cargo capacity</li>
  <li>Tell you the amount of trips remaining for the last bought item based on your ships cargo capacity</li>
  <li>Edit the shopping/delivery list in-app</li>
  <li>Create a shopping/delivery list</li>
  <li>Removing shopping/delivery list</li>
  <li>Print out events in a live journal monitoring mode (mostly a debug feature)</li>
</ul>
<br>
The app has a simple TUI (Text-based user interface) featuring autocomplete to help avoid typos.<br>

## Installation
You can install the provided windows/linux release or (for the most up to date but also possibly buggier versio) clone the repository and run app.py<br>
```
git clone https://github.com/Piniat/ED-Construction-helper.git
cd ED-Construction-helper
```
Install dependancies
```
pip install -r requirements
```
## Usage
Launch using the execuatable file in the packaged release or if you cloned the repo:
```
python app.py
```
When first launching the app will ask for the game journal file location and exit. The journal location is stored in config.ini, should the event tracking not work or any errors occur delete that file and retry.
<br>
When first choosing the shopping or construction delivery list mode you will ne asked to input how many items you need to buy, after which you will be asked to input the name and quantity of each item.
## Commands
The app uses commands to function. These consist of:
<ul>
  <li>help - displays a list of commands</li>
  <li>app-mode-1: Switches to Construction Progress Mode</li>
  <li>app-mode-2: Switches to Shopping List Mode</li>
  <li>app-mode-3: Switches to Journal Monitoring Mode</li>
  <li>override-docked: Override the docked status for the app</li>
  <li>override-docked-construction: Override the docked status at a construction site</li>
  <li>edit-shopping-list: Allows you to edit your shopping list in-app</li>
  <li>edit-construction-progress: Allows you to edit your construction progress</li>
  <li>edit-ship-cargo: Allows you to update your ship's cargo space</li>
  <li>reset-progress: Resets the shopping list or construction progress data</li>
  <li>exit: Exits the application</li>
</ul>
