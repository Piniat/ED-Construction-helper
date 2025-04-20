# ED Construction helper
This app was made to track deliveries to colonisation constructions (colonisation megaships or construction sites) and track the gathering of materials using a shopping list. It's basically a self updating spreadsheet.<br>
The app can currently:<br>
<ul>
  <li>Track deliveries to constructions</li>
  <li>Track the collection of items via marketbuy events</li>
  <li>Tell you the amount of trips remaining based on your ships cargo capacity</li>
  <li>Tell you the amount of trips remaining for the last bought item based on your ships cargo capacity (only for shopping list)</li>
  <li>Edit the shopping/delivery list in-app</li>
  <li>Create a shopping/delivery list</li>
  <li>Removing shopping/delivery list</li>
  <li>Print out events in a live journal monitoring mode (no practical use)</li>
  <li>Automatically detect updates, download and install them</li>
</ul>
<br>
The app has a simple TUI (Text-based user interface) featuring autocomplete to help avoid typos.<br>

## Installation
You can install the provided windows/linux release or (for the most up to date but also possibly buggier version) clone the repository and run main.py<br>
```
git clone https://github.com/Piniat/ED-Construction-helper.git
cd ED-Construction-helper
```
Install dependencies
```
pip install -r requirements
```
## Usage
Launch using the executable file in the packaged release or if you cloned the repo:
```
python __main__.py
```
When first launching the app will ask for the game journal file location. The journal location is stored in config.ini, should the event tracking not work or any errors occur delete that file and retry.
<br>
<br>
When first choosing the shopping list mode you will ne asked to input how many items you need to buy, after which you will be asked to input the name and quantity of each item.<br>
For the delivery list you have the option of auto-creating one from the journal logs when docked at a construction, auto copying from the shopping list or manually making one (both of which will get overwritten by construction journal events once docked at one)
<br>
<br>
Updates can be disabled by editing config.ini and setting the value of [AUTO_UPDATE] to false
<br>
config.ini also stores the journal folder path, app version (though honestly it isn't really used), updater version and if the user has launched the app for the first time.
## Commands
The app uses commands to function. These consist of:
<ul>
  <li>help - displays a list of commands</li>
  <li>delivery-tracker: Switches to Construction Progress tracking Mode</li>
  <li>shopping-list: Switches to Shopping List tracking Mode</li>
  <li>journal-monitor: Switches to Journal Monitoring Mode. No use other than seeing the logged events</li>
  <li>edit-shopping-list: Allows you to edit your shopping list in-app</li>
  <li>edit-construction-progress: Allows you to edit your construction progress (changes will get overwritten by construction site journal events)</li>
  <li>edit-ship-cargo: Allows you to update your ship's cargo space</li>
  <li>reset-progress: Resets the shopping list or construction progress data</li>
  <li>exit: Exits the application</li>
</ul>
