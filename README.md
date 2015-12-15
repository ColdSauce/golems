# Golems
golems is a rougelike game that teaches kids about logic and programming. A person starts with a robot that they can program before they get into combat. The robot, then, becomes completely autonomous during a Pokemon type of battle. Although golems is intended to be run on the [OLPC XO](https://en.wikipedia.org/wiki/OLPC_XO), it can be played on any modern operating system. 

# Contributing
Check out CONTRIBUTING.md to find out how you can start contributing! 

# IRC channel
Check out #golems on freenode if you have any questions about anything from contributing to getting the game up and running on an XO.

# Building & Playing It
## Windows
Fetch yourself a copy of Python 2.7 from [Python.org's website](https://www.python.org/downloads/) and Pygame for Windows from [Pygame.org's website](http://www.pygame.org/download.shtml).  Provided you allowed both installers access to your PATH, just open up a Command Prompt window (as in, open the Start Menu, type in `cmd`, and press Enter), navigate to where the repository is on your computer, and run `python testgame.py`.

## Mac
TODO: Have a guide on how to build and play Golems for Mac

## Linux
Fetch yourself a copy of Python 2.7 and Pygame using your package distributor of your choice (ie `apt-get`, `yum`, and the like), open up a terminal, and execute `python testgame.py`.

## Sugar
Sugar already comes with the requisite Python and Pygame installed.  Open up the Terminal Activity, move into the directory with the repository, and execute `python testgame.py` to test it without any additional Sugar stuff.

Alternatively, you may install it to your local machine by way of `sudo ./setup.py install` from within the same directory, and it will pop into your Home Menu (represented by the singular dot).
