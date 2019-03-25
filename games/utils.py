from tensorforce.agents import PPOAgent, DQNAgent, VPGAgent
import subprocess

# game = "bos"
# agentType = "ppo"

def get_agent(game, agentType):

	checkpointPath = "agents/" + game + "/" + agentType

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

	# def select_agent(agent, game):
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


	try:
		agent.restore(directory=checkpointPath, filename=None)
	except:
		agent.initialize()


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
				1: (0, 3)
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

