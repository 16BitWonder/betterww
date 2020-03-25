### About

Better Wind Waker  

This is an ISO patcher for The Legend of Zelda: The Wind Waker based on [LagoLunatic's wwrando](https://github.com/LagoLunatic/wwrando).

**This adds features from the Wind Waker Randomizer to an ISO without randomization.**  
Intended to make a more enjoyable casual experience reflecting many quality of life changes made for Wind Waker HD.  

*The download button above is for source code, not the application.*  
**[Download the program here](https://github.com/WideBoner/betterww/releases)**  

You can toggle the following on/off:
* Swift Sail replaces Sail  
* Instant text boxes  
* Faster block moving  
* Faster grapple hook  
* Faster rolling speed  
* Faster crawling, climbing, NPC chat zoom  
* Tingle chests without tingle tuner 
* Turn while swinging or grappling
* Reveal full sea chart 
* Free-roam boat  
* No song replays  
* Invert camera  
* Remove intro video  
* Faster ballad of gales  
* Brisk Sail (even faster sail)


**Custom Player Models**  

Allows you to customize Link, but "casual" outfits will only be seen before getting the tunic or if playing Second Quest 

Models can be found on [the github repository](https://github.com/Sage-of-Mirrors/Custom-Wind-Waker-Player-Models), on [GameBanana](https://gamebanana.com/games/6173), or the [ WW Randomizer Discord](https://discord.gg/r2963mt)  
Add them to the models folder.

### Other Tweaks

You can apply the [Widescreen Patch](https://www.dropbox.com/s/5huyf6r3drynq1c/The%20Legend%20of%20Zelda%20The%20Wind%20Waker%20Widescreen.zip?dl=1) before running this  

You can apply the [Female Pronoun Patch](http://slothsoft.tumblr.com/post/36097890951/the-legend-of-zelda-the-wind-waker-pronoun) before running this  

If using Dolphin you can use [Hypatia's HD Texture Pack](https://onthegreatsea.tumblr.com/DOWNLOADS)

**Gecko codes you may want to use (by Ralf and wiiztec)**  
Included is an optional file with these Gecko codes that I like to use:  

* Second set of equipped items (D-pad down to switch)   
* Hero Mode (Take double damage, no heart drops)  
* Items don't disappear  
* Unrestricted Camera  
* No Heart Beeping Noise  
* Blur off  


### Download

See the [releases page](https://github.com/brainfubar/wwrando/releases) to download zip files containing the program and assets. Both 32-bit and 64-bit versions are available.

### Information

This program only supports the North American Gamecube version of Wind Waker. (MD5: d8e4d45af2032a081a0f446384e9261b)  

This works on Gamecube/Wii/Dolphin.
The European and Japanese versions of Wind Waker won't work, and neither will Wind Waker HD.

If you're going to play on emulator, you should use the latest development version of Dolphin which can be found at the top of this page: https://dolphin-emu.org/download/

### Running from source

Download and install git from here: https://git-scm.com/downloads  
Then clone this repository with git by running this in a command prompt:  
`git clone https://github.com/LagoLunatic/wwrando.git`  

Download and install Python 3.6.6 from here: https://www.python.org/downloads/release/python-366/  
"Windows x86-64 executable installer" is the one you want if you're on Windows, "macOS 64-bit installer" if you're on Mac.  

Open the wwrando folder in a command prompt and install dependencies by running:  
`py -3.6 -m pip install -r requirements.txt` (on Windows)  
`python3 -m pip install -r requirements.txt` (on Mac)  

Then run the randomizer with:  
`py -3.6 wwrando.py` (on Windows)  
`python3 wwrando.py` (on Mac)  

In addition, follow this if you want to use PyInstaller to build a distributable version of the randomizer:  
* Install one of PyInstaller's dependencies manually: `py -3.6 -m pip install pywin32-ctypes==0.2.0`  
* Install PyInstaller: `py -3.6 -m pip install PyInstaller==3.4`  
* Then to make a build in the `dist` directory: `build.bat`  

### Discord Server

If you have any questions or are looking for people to play/race with, why not join the official Wind Waker Randomizer Discord server?  
https://discord.gg/r2963mt

### Credits

wwrando:  
The randomizer was created and programmed by LagoLunatic, with help from:  
MelonSpeedruns (game design, graphic design)  
Hypatia (textures)  
SageOfMirrors (file format documentation)  
LordNed (file format documentation)  
CryZe (event flag documentation)  

betterww:  
brainfubar (His wwrando fork was used to make this)  
MelonSpeedruns (Original design for Brisk Sail)  
JarheadHME (Help getting releases working and updating)
