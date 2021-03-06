# Piratebot
A pirate ship bot. Lets you fight other users and upgrade your ship. Sail on captain! 

## Installation

PirateBot was created on python 3.6. no other versions were tested (3.7 now works with rewrite)

### discord.py
PirateBot relies on discord.py, an API wrapper for Discord written in Python. 

It's available at https://github.com/Rapptz/discord.py 

Documentation to be found at 
https://discordpy.readthedocs.io/en/rewrite/index.html
and https://discordpy.readthedocs.io/en/latest/ (I'm using the rewrite but sometimes its easier to find stuff in the other repo)

to install on most systems enter the following
```buildoutcfg
python3 -m pip install -U discord.py
```
>This didn't work for me and kept installing version 0.16 when I needed to use version 1.0 (the rewrite)
> If it doesn't work for you I had to do this:

```bash
$ git clone https://github.com/Rapptz/discord.py
$ cd discord.py
$ python3 -m pip install -U .[voice]
```

discord.py also has the following dependencies 
- Python 3.4.2+
- `aiohttp` library
- `websockets` library
- `PyNaCl` library (optional, for voice only)
    - On Linux systems this requires the `libffi` library. You can install in
      debian based systems by doing `sudo apt-get install libffi-dev`.

Usually `pip` will handle these for you.

### PirateBot

Follow https://discordpy.readthedocs.io/en/rewrite/discord.html to set up a discord bot 

Once you get your Token create a file in the PirateBot directory called tokenfile.py

in that file enter `TOKEN = 'placeyourtokenhere'` including the quotes

This file is kept separate because displaying your token publicly is generally a bad idea

### Run

to run, simply execute `python3 pirate_ship.py` and if everything else is well, you should be logged in and able to talk to your bot in your channel. Enjoy.

## Commands
```
A pirate ship bot. Lets you fight other users and upgrade your ship. Sail on captain! 
Prefix is $

Pirate:
  fight   starts a fight with someone in chat
  ship    look at your ship's info or create one if you're new
  upgrade Upgrade your ship
​No Category:
  help    Shows this message.

Type $help command for more info on a command.
You can also type $help category for more info on a category.
```
