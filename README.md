Custom Map Loader
-----------

A quick and dirty command-line implementation of NoxPhoenix's project by the same name, found [here](https://github.com/NoxPhoenix/custom-map-loader/), written in Python

Setup & Installation
-----------
* Download the project by clicking "Code" -> "Download ZIP"
* Extract the CustomMapLoader.py from the downloaded archive
* Optionally, for Linux systems
* * Put CustomMapLoader.py in your `/usr/bin` as `custommaploader`
* * Either create a symlink, or move the file directly
* From here on, `custommaploader` will be used to denote the executable. Replace with `./CustomMapLoader.py` or `python CustomMapLoader.py` as needed
* Run `custommaploader setup maps (/path/to/folder)`, where the path is a folder containing all of your custom map folders
* Run `custommaploader setup rocketleague (path/to/folder)`, where the path is your `rocketleague` folder
* * On Linux systems, this is likely `~/.local/share/Steam/steamapps/common/rocketleague`
* * On Windows systems, this is likely `C:/Program Files(x86)/Steam/steamapps/common/rocketleague`
* * On Windows Epic client, this may be `C:/Program Files/Epic Games/rocketleague`
* To see your available custom maps to choose from, run `custommaploader list`
* To load a custom map, run `custommaploader setmap (map)`, where `map` is one of the options from `custommaploader list`
* The script will replace your Underpass map with the custom map, backing up the orginal Underpass map in the process
* If you ever want to restore the original Underpass, just run `custommaploader setmap Underpass`

Uninstallation
-----------
* First, run `custommaploader setmap Underpass` to restore the original Underpass map
* Delete `CustomMapLoader.py`
* If you put it in `/usr/bin`, delete it from there as well
* Delete `.custommaploaderrc` from your home directory
* * On Linux systems, this will usually be `/home/[user]`
* * On Windows systems, this will usually be `C:/Users/[user]`