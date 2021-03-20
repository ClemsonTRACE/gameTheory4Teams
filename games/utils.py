from tensorforce.agents import PPOAgent, DQNAgent, VPGAgent
import subprocess
import numpy as np
import os
from tqdm import tqdm



#game = "3pd"
#agentType = "ppo"

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
	},
	"3pd": {
		"states": {
			"type":'float', "shape": (10,3, 1,) 
		},
		"actions": {
			"type": "int", "num_values": 2
		}
	}
}

def get_agent(game, agentType):
	count = 1

	base_path = '.'
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

	if game == "3pd":
		try:
			agent.restore(directory=checkpointPath, filename=None)
			print("restoration successful")
		except Exception as e:
			agent.initialize()
			for x in tqdm(range(1000001)):
				testState = np.full(config[game]["states"]["shape"], None)

				for i in range(10):
					moveA = agent.act(testState)
					moveB = agent.act(testState)
					moveC = agent.act(testState)
					rewards = payoffs(game, [moveA, moveB, moveC])
					if i < 9:
						agent.observe(reward=rewards[0], terminal=False)
						agent.observe(reward=rewards[1], terminal=False)
						agent.observe(reward=rewards[2], terminal=False)
					else: 
						agent.observe(reward=rewards[0], terminal=False)
						agent.observe(reward=rewards[1], terminal=False)
						agent.observe(reward=rewards[2], terminal=True)
					testState[i] = [[moveA], [moveB], [moveC]]
				if x%1000 == 0:
					# checkpointPath = "../games/agents/" + game + "/" + agentType + "/"
					agent.save(directory=checkpointPath, filename=None)
					# print("saving successful")
	else:
		try:
			agent.restore(directory=checkpointPath, filename=None)
			print("restoration successful")
		except Exception as e:
			# try:
			# 	checkpointPath = base_path + "/agents/" + game + "/" + agentType + "/"
			# 	agent.restore(directory=checkpointPath, filename=None)
			# 	print("restoration successful after second attempt")
			# except Exception as e:
			# 	a = subprocess.check_output("ls games/", shell=True)
			# 	print(a)
			# 	print(os.getcwd(), "vs", subprocess.check_output("pwd", shell=True))
			# 	checkpointPath = "./games/agents/" + game + "/" + agentType + "/"
			# 	print(checkpointPath)
			# 	agent.restore(directory=checkpointPath, filename=None)
			# 	print("restoration successful after third attempt")
			agent.initialize()

			for x in tqdm(range(count)):

				testState = np.full(config[game]["states"]["shape"], 0)

				for i in range(10):
					moveA = agent.act(testState)
					moveB = agent.act(testState)
					rewards = payoffs(game, [moveA, moveB])
					if i < 10:
						agent.observe(reward=rewards[0], terminal=False)
						agent.observe(reward=rewards[1], terminal=False)
					else: 
						agent.observe(reward=rewards[0], terminal=False)
						agent.observe(reward=rewards[1], terminal=True)

					testState[i] = [[moveA], [moveB]]
			checkpointPath = "./games/agents/" + game + "/" + agentType + "/"
			agent.save(directory=checkpointPath, filename=None)
			print("saving successful")

	return agent

def payoffs(game, moves):
	
	payoff_config = {
		"bos": {
			0: {
				0: (3, 2),
				1: (1, 1)
			},
			1: {
				0: (0, 0),
				1: (2, 3)
			}
		},
		"pd": {
			0: {
				0: (-1, -1),
				1: (-3, 0)
			},
			1: {
				0: (0, -3),
				1: (-2, -2)
			}
		},
		"hawkdove": {
			0: {
				0: (-2, -2),
				1: (-1, 1)
			},
			1: {
				0: (1, -1),
				1: (0, 0)
			}
		},
		"3pd": {
			0: {
				0: {
					0: (7, 7, 7),
					1: (3, 3, 9)
				},
				1: {
					0: (3, 9, 3),
					1: (0, 5, 5)
				}
			},
			1: {
				0: {
					0: (9, 3, 3),
					1: (5, 0, 5)
				},
				1: {
					0: (5, 5, 0),
					1: (1, 1, 1)
				}
			}
		}
	}

	if len(moves) > 2:
		_payoffs = payoff_config[game][moves[0]][moves[1]][moves[2]]
	else:
		humanMove = moves[0]
		aiMove = moves[1]
		_payoffs = payoff_config[game][humanMove][aiMove]

	return _payoffs

def setup():
	gameList = ["3pd"]
	agentList = ["ppo", "vpg", "dqn"]

	swarm = {}
	for game in gameList:
		swarm[game] = {}
		for agentType in agentList:
			print(game, agentType)
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


