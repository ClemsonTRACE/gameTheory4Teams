import requests
import json 

stuff = {"gameState": {
	"0": [2, 1], "1": [2, 1], "2": [2, 1]
	},
	"move": 1
} 

# r = requests.post("http://localhost:8000/games/bos/ppo", json=json.dumps(stuff))

r = requests.post("http://localhost:8000/games/twoByTwo/pd/ppo", json=json.dumps(stuff))

print(r.json())
