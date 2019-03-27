from django.shortcuts import render
from .utils import get_agent, payoffs
import json
from django.http import JsonResponse, HttpResponse
from pprint import pprint
from .models import Game
from django.core import serializers


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

		try:
			r = json.loads(request.body)
			r = json.loads(r)
		except:
			r = request.body.decode('utf-8')
			r = json.dumps(r)
			r = json.loads(r)
			r = json.loads(r)
		pprint(r)

		epoch = str(r["epoch"])
		turn = str(r["turn"])

		testState = list(r["gameState"][epoch].values())
		testState = [testState]
		action = agent.act(testState)

		stuff = payoffs(gameType, action, r["move"])

		r["gameState"][epoch][turn] = [int(r["move"]), int(action)]
		r["payoffs"][epoch][turn] = [stuff[0], stuff[1]]
		r["turn"] = int(turn) + 1

		if int(turn) == int(r["numTurns"]): 
			if int(epoch) == int(r["numEpochs"]):
				r["status"] = True
				#add the datasaving part here
				Game.objects.create(
					game_type = r["game"],
					opponent = r["opponent"],
					model = r["model"],
					status = r["status"],
					numEpochs = r["numEpochs"],
					numTurns = r["numTurns"],
					gameState = r["gameState"],
					payoffs = r["payoffs"],
					epoch = r["epoch"],
					turn = r["turn"],
					surveyID = r["surveyID"],
				)
			else:
				r["turn"] = 0
				r["epoch"] = int(epoch) + 1

		agent.close()
		
		pprint(r)

		# return render(request, "bos.html", {"agent": agentType})
		return JsonResponse(r)

def pull(request):
	dataPoints = Game.objects.values()
	stuff = {}
	i = 0
	for el in dataPoints:
		stuff[i] = el
		i += 1

	return JsonResponse(stuff)

def centipede(request, agentType):
	return render(request, "centipede.html")

def ultimatum(request, agentType):
	return render(request, "ultimatum.html")