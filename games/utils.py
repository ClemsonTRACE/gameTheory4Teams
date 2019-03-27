from tensorforce.agents import PPOAgent, DQNAgent, VPGAgent
import subprocess
import numpy as np
import os
from tqdm import tqdm



# game = "bos"
# agentType = "ppo"

config = {
	"bos": {
		"states": {
			"type":'float', "shape": (10,2, 1,) 
		},
		"actions": {
			"type": "int", "num_values": 2
		}
	},
	"pd": {
		"states": {
			"type":'float', "shape": (10,2, 1,) 
		},
		"actions": {
			"type": "int", "num_values": 2
		}
	},
	"hawkdove": {
		"states": {
			"type":'float', "shape": (10,2, 1,) 
		},
		"actions": {
			"type": "int", "num_values": 2
		}
	}
}

def get_agent(game, agentType):

	base_path = os.getcwd()
	checkpointPath = base_path + "/games/agents/" + game + "/" + agentType + "/"

	if agentType == "vpg":
		agent = VPGAgent(
		    states= config[game]["states"],
		    actions= config[game]["actions"],
		    memory=1000,
		    network="auto",
		)
	elif agentType == "ppo":
		agent = PPOAgent(
		    states= config[game]["states"],
		    actions= config[game]["actions"],
		    memory=1000,
		    network="auto",
		)
	elif agentType == "dqn":
		agent = DQNAgent(
		    states= config[game]["states"],
		    actions= config[game]["actions"],
		    memory=1000,
		    network="auto",
		)


	try:
		agent.restore(directory=checkpointPath, filename=None)
		print("restoration successful")
	except Exception as e:
		try:
			checkpointPath = base_path + "/agents/" + game + "/" + agentType + "/"
			agent.restore(directory=checkpointPath, filename=None)
			print("restoration successful after second attempt")
		except Exception as e:
			checkpointPath = base_path + "/games/agents/" + game + "/" + agentType + "/"
			agent.restore(directory=checkpointPath, filename=None)
			print("restoration successful after second attempt")
		# agent.initialize()


		# for x in tqdm(range(10000)):

		# 	testState = np.full(config[game]["states"]["shape"], 0)

		# 	for i in range(10):
		# 		moveA = agent.act(testState)
		# 		moveB = agent.act(testState)
		# 		rewards = payoffs(game, moveA, moveB)
		# 		if i < 10:
		# 			agent.observe(reward=rewards[0], terminal=False)
		# 			agent.observe(reward=rewards[1], terminal=False)
		# 		else: 
		# 			agent.observe(reward=rewards[0], terminal=True)
		# 			agent.observe(reward=rewards[1], terminal=True)

		# 		testState[i] = [[moveA], [moveB]]

		# agent.save(directory=checkpointPath, filename=None)
		# print("saving successful")

	return agent


def payoffs(game, aiMove, humanMove):
	
	config = {
		"bos": {
			1: {
				0: (3, 2),
				1: (1, 1)
			},
			0: {
				0: (2, 3),
				1: (0, 0)
			}
		},
		"pd": {
			1: {
				0: (-3, 0),
				1: (-1, -1)
			},
			0: {
				0: (-2, -2),
				1: (0, -3)
			}
		},
		"hawkdove": {
			1: {
				0: (1, -1),
				1: (-2, -2)
			},
			0: {
				0: (0, 0),
				1: (-1, 1)
			}
		}
	}

	return config[game][aiMove][humanMove]

def setup():
	gameList = ["bos", "pd", "hawkdove"]
	agentList = ["ppo", "vpg", "dqn"]

	swarm = {}
	for game in gameList:
		swarm[game] = {}
		for agentType in agentList:
			swarm[game][agentType] = get_agent(game, agentType)

	return swarm

if __name__ == "__main__":
	# gameList = ["bos", "pd", "hawkdove"]
	# agentList = ["ppo", "vpg", "dqn"]

	# subprocess.call("mkdir agents/", shell=True)
	# for game in gameList:
	# 	subprocess.call("mkdir agents/" + game, shell=True)
	# 	for agentType in agentList:
	# 		subprocess.call("mkdir agents/" + game + "/" + agentType, shell=True)
	# 		get_agent(game, agentType)
	a = setup()
	print(a)


