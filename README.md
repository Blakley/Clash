# Clash

Clash Of Clans clan-member invitation automation

## Features
 * Ability to invite and filter players to your clan via: townhall, player rank, and troop rank
 * Can modify code to add additional filter parameters such as by builderhall

## Info
By default, some of the core functionality is based upon `pyautogui.position()` which is a function
in the `pyautogui` module that allows you to get the (x, y) coordinates of your mouse.
We use this function to get the values of specific Clash of Clans buttons and input areas.

Below is a code snippet that shows how buttons from the game are assigned to (x, y) coordinate pairs on the screen.
You can adjust these values if you experience any issue or if your screen size differs.
```
self.positions = {
			'game_area' : 			(1373, 35),
			'my_clan' : 			(809, 66),
			'find_new_members': 	(516, 733),
}
```


## Dependencies

You will need to have both `bluestacks5` and `pip` installed on your system and then install the following using pip
```
$ pip install cv2
$ pip install PIL
$ pip install numpy
$ pip install pynput
$ pip install pyautogui
$ pip install pyperclip
$ pip install pytesseract
```

## Usage
1. Simply have Clash of Clans running in BlueStacks5, then run the following:
   - execute `python clash.py`
2. After executing the command, switch to the BlueStacks5 instance and after 5 seconds, the program will begin execution