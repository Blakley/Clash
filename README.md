# Clash

Clash Of Clans clan-member invitation automation

## Features
 * Ability to invite and filter players to your clan via: townhall, player rank, and troop rank
 * Can modify code to add additional filter parameters such as by builderhall

## Understanding the Code
By default, some of the core functionality is based upon `pyautogui.position()` which is a function
in the `pyautogui` module that allows you to get the (x, y) coordinates of your mouse.
We use this function to get the values of specific Clash of Clans buttons and input areas.

Below is a code snippet that shows how buttons from the game are assigned to (x, y) coordinate pairs on the screen.
You can adjust these values if you experience any issue or if your screen resolution differs from 1920 by 1080.
 - Note: Run BlueStacks5 in full screen mode
```
self.positions = {
			'game_area' : (1373, 35),
			'my_clan' : (809, 66),
			'find_new_members': (516, 733),
}
```

To get the townhall and trophy amount of players, we use the offical Clash of Clans API
You will need to create a develeopers account to get started. [Clash API](https://developer.clashofclans.com/#/login)
After creating an account and obtaining your `clash api token`
change the following snippet of code to accept your token
```
self.token = 'your_clash_api_token'
```

Currently, we invite players that are th9 with 1000 trophies, we can easily edit this as well
as add other filters taken from the clash api

Below is a snippet that demonstrates how to filter members based on if their archer and barbarian are level 4 and above
```
troops = response.get('troops')
		barb = troops[0]
		archer = troops[1]
		if int(archer['level']) < 4 and int(barb['level']) < 4:
			return False 
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