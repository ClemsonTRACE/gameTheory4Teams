from tensorforce.agents import PPOAgent, DQNAgent, VPGAgent
import subprocess
import numpy as np
import os


# game = "bos"
# agentType = "ppo"

def get_agent(game, agentType):

	base_path = os.getcwd()
	checkpointPath = base_path + "/games/agents/" + game + "/" + agentType + "/"

	config = {
		"bos": {
			"states": {
				"type":'float', "shape": (3,2, 1,) 
			},
			"actions": {
				"type": "int", "num_values": 2
			}
		},
		"pd": {
			"states": {
				"type":'float', "shape": (3,2, 1,) 
			},
			"actions": {
				"type": "int", "num_values": 2
			}
		},
		"hawkdove": {
			"states": {
				"type":'float', "shape": (3,2, 1,) 
			},
			"actions": {
				"type": "int", "num_values": 2
			}
		}
	}

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
	except Exception as e:
		print("\nrestoriation failed\n")
		# print(e)
		agent.initialize()
		for i in range(10):
			testState = np.full(config[game]["states"]["shape"], 0)
			agent.act(testState)
			agent.observe(reward=1, terminal=False)
		agent.save(directory=checkpointPath, filename=None)


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

if __name__ == "__main__":


	gameList = ["bos", "pd", "hawkdove"]
	agentList = ["ppo", "vpg", "dqn"]

	for game in gameList:
		subprocess.call("mkdir agents/" + game, shell=True)
		for agentType in agentList:
			subprocess.call("mkdir agents/" + game + "/" + agentType, shell=True)
			get_agent(game, agentType)
