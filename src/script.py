# ----------------------------------------------------------------------
#								Imports
# ----------------------------------------------------------------------

import os
import re
import sys
import cv2
import json
import time
import requests
import pyautogui
import pytesseract 
import numpy as np
import pyperclip as pc
from PIL import Image 
from pynput.keyboard import Key, Controller


# ----------------------------------------------------------------------
#								Globals
# ----------------------------------------------------------------------

pyautogui.FAILSAFE = True
TOKEN = ''


# ----------------------------------------------------------------------
#								Class
# ----------------------------------------------------------------------
class Members():
	def __init__(self):
		self.token = TOKEN
		self.header = {
			'Accept' : 'application/json',
			'authorization' : 'Bearer ' + self.token 
		}
		
		self.positions = {
			'game_area' : 			(1373, 35),
			'my_clan' : 			(809, 66),
			'find_new_members': 	(516, 733),
			'filter_wars': 			(396, 298),
			'filter_league': 		(802, 296),
			'filter_trophy': 		(1249,301),
			'search_suggested': 	(1548,426),
			'player_area': 			(253, 501),	
			'player_code': 			(757, 286),
			'copy': 				(946, 300),
		}

		self.keyboard = Controller()
		self.added = 0
		self.count = 0
		self.invited = []
		
		self.start()	

	def start(self):
		self.count = input('Number of players to invite: ')
		time.sleep(5)
		for _ in range(20):
			for i in range(3):
				if i == 0:
					if self.begin('war') == 1:
						self.leave()
						return
				if i == 1:
					if self.begin('league') == 1:
						self.leave()
						return
				if i == 2:
					if self.begin('trophy') == 1:
						self.leave()
						return

	def begin(self, search):
		# navigate to member area
		time.sleep(1)
		pyautogui.click(self.positions['game_area'])
		time.sleep(1)

		self.keyboard.press('g')
		self.keyboard.release('g')
		time.sleep(1)

		pyautogui.click(self.positions['my_clan'])
		time.sleep(1)

		pyautogui.click(self.positions['find_new_members'])
		time.sleep(1)		

		# select filter
		if search == "war":
			time.sleep(1)
			pyautogui.click(self.positions['filter_wars'])
			time.sleep(1)

		if search == "league":
			time.sleep(1)
			pyautogui.click(self.positions['filter_league'])
			time.sleep(1)

		if search == "trophy":
			time.sleep(1)
			pyautogui.click(self.positions['filter_trophy'])
			time.sleep(1)		

		# Search
		pyautogui.click(self.positions['search_suggested'])
		time.sleep(1)

		pyautogui.moveTo(self.positions['player_area'])
		time.sleep(1)		

		# Invite Players
		self.last_pos = self.positions['player_area']
		for x in range(40):
			# click profile
			pyautogui.click()
			time.sleep(0.5)
			
			try:
				pyautogui.moveTo(pyautogui.position().x, pyautogui.position().y + 10)
			except Exception as e:
				continue	

			pyautogui.click()
			time.sleep(1.5)		

			# invite
			done = self.invite()
			if (done == 1):
				return 1

		return self.finished()

	def invite(self):
		# invite player if they meet all qualifications
		if self.filter() == True:
			status = self.send_invite()
			if status == 1:
				return 1 # finished adding players

		time.sleep(1)
		self.get_next()

	def send_invite(self):
		try:
			x, y = pyautogui.locateCenterOnScreen('invite.png', confidence=.8)
			pyautogui.click(x, y)
		except Exception as e:
			return

		self.added += 1
		print("[invited] " + str(self.added))
		if (int(self.added) >= int(self.count)):
			print("[FINISHED]")
			return 1		

	def get_next(self):
		# Go back to player menu
		self.keyboard.press(Key.esc)
		self.keyboard.release(Key.esc)
		time.sleep(1)

		# 4. reposition mouse to last position
		pyautogui.moveTo(self.last_pos)
		time.sleep(1)

		# 5. scroll to next profile / check if scrolled
		pyautogui.scroll(-60)
		time.sleep(1)

		# 6. update last position
		self.last_pos = pyautogui.position()
		time.sleep(1)

	def finished(self):
		# Added all players from filter
		time.sleep(1)
		self.keyboard.press(Key.esc)
		self.keyboard.release(Key.esc)
		
		time.sleep(1)
		self.keyboard.press(Key.esc)
		self.keyboard.release(Key.esc)	
		return 0

	def leave(self):
		# finished inviting all players
		try:
			x, y = pyautogui.locateCenterOnScreen('exit.png', confidence=.8)
			pyautogui.click(x, y)
		except Exception as e:
			print('failed to exit')		

	# ----------------------------------------------------------------------
	#						Provide Player Filtering
	# ----------------------------------------------------------------------
	def filter(self):
		# filter driver function
		self.get_info()
		
		# passes all filters
		try:
			f_clan = self.clan()
			f_name = self.name()
			# f_location = self.location()
			f_trophies = self.trophies()
			f_troops = self.troops()
			f_heros = self.heros()

			if f_clan == False or f_name == False:
				return False

		except Exception as e:
			return False

		self.invited.append(str(self.player.get('name')))
		return True

	def get_info(self):
		# copy player id
		time.sleep(1)
		pyautogui.click(self.positions['player_code'])
		time.sleep(0.7)
		pyautogui.click(self.positions['copy'])

		# get player information
		player_id = str(pc.paste())
		search = f'https://api.clashofclans.com/v1/players/%23{player_id[1:]}'.format()
		self.player = requests.get(search, headers = self.header).json()

	def clan(self):
		# Do they pass clan filtering
		try:
			c = self.player.get('clan')
			name = c['name']
			if len(name) > 1:
				return False
		except Exception as e:
			return True
		return True

	def location(self):
		# Do they pass location filtering
		# allowed country codes : countryCode
		allowed = [
			'US',
			'GB',
			'VI',
			'CH',
			'NZ',
			'NL',
			'MA',
			'ME',
			'JO',
			'JE',
			'IT',
			'GL',
			'GR',
			'GE',
			'CA',
			'AU',
			'BS',
			'BE',
			'',
			'',
			''
		]
		
		return True

	def name(self):
		# Do they pass name filtering
		name = str(self.player.get('name'))
		if name in self.invited:
			return False

		RE = re.compile(u'⺙⺛⻳⿕々〩〸〺〻㐀䶵鿃豈鶴侮頻並龎áéíóúüñ¿¡', re.UNICODE)
		good = RE.sub('', name)
		if name != good:
			return False

		return True

	def hall(self):
		# Do they town hall requirement
		th = self.player.get('townHallLevel')
		if int(th) < 8:
			return False
		return True

	def trophies(self):
		th = self.player.get('townHallLevel')
		trophies = int(self.player.get('trophies'))

		# Do they pass trophy requirements
		if (th == 7):
			if trophies < 1000:
				return False

		if (th == 8):
			if trophies < 1300:
				return False

		if (th == 9):
			if trophies < 1800:
				return False

		if (th == 10):
			if trophies < 2100:
				return False

		if (th == 11):
			if trophies < 2400:
				return False

		return True

	def troops(self):
		th = self.player.get('townHallLevel')
		dragon = self.player.get('troops')[8]['level']

		# Do they pass troop requirements
		if (th == 7):
			if dragon < 2:
				return False

		if (th == 8 or th == 9):
			if dragon < 3:
				return False
		
		if (th == 10):
			if dragon < 4:
				return False
		
		if (th == 11 or th > 11):
			if dragon < 5:
				return False

		return True

	def heros(self):
		th = self.player.get('townHallLevel')
		king = self.player.get('heroes')[0]['level']

		# Do they pass hero requirements		
		if (th == 7):
			if king < 4:
				return False

		if (th == 8):
			if king < 8:
				return False

		if (th == 9 or th == 10 or th == 11):
			queen = self.player.get('heroes')[1]['level']

			if (th == 9):
				if king < 15:
					return False
				if queen < 15:
					return False
				
			if (th == 10):
				if king < 25:
					return False
				if queen < 25:
					return False

			if (th == 11):
				if king < 35:
					return False
				if queen < 35:
					return False

		return True


clash = Members()