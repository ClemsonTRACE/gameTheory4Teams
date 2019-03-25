from django.shortcuts import render
from .utils import get_agent, payoffs
import json
from django.http import JsonResponse


# Create your views here.
def twoByTwo(request, gameType, agentType):
	agent = get_agent(gameType, agentType)


	if (request.method == "GET"):


		for i in range(10):
			testState = [[[2, 1], [2, 1], [2, 1]]]
			action = agent.act(testState)
			print("action", action)

			agent.observe(reward=1, terminal=False)


		return render(request, "bos.html", {"agent": agentType})


	elif(request.method == "POST"):
		r = json.loads(request.body)
		r = json.loads(r)
		print(r)

		print(r["gameState"])
		testState = list(r["gameState"].values())
		print(testState)
		testState = [testState]
		action = agent.act(testState)
		print("action", action)

		stuff = payoffs(gameType, action, r["move"])
		print("payoffs", stuff)

		# return render(request, "bos.html", {"agent": agentType})
		return JsonResponse(
			{
				"moves": [int(action), int(r["move"])],
				"payoffs": stuff
			}
		)

def centipede(request, agentType):
	return render(request, "centipede.html")

def ultimatum(request, agentType):
	return render(request, "ultimatum.html")