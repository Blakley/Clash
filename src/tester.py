import re
import json
import requests

TOKEN = 'your_clash_api_token' 
header = {
	'Accept' : 'application/json',
	'authorization' : 'Bearer ' + TOKEN
}

player_id = 'player_id'

search = f'https://api.clashofclans.com/v1/players/%23{player_id[1:]}'.format()

player = requests.get(search, headers = header).json()

print(json.dumps(player, sort_keys=False, indent=4))
