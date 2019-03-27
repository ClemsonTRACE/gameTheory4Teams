from django.db import models
from jsonfield import JSONField

# Create your models here.
class Game(models.Model):
	game_type = models.CharField(max_length=300)
	opponent = models.CharField(max_length=300)
	model = models.CharField(max_length=300)
	status = models.BooleanField()
	numEpochs = models.FloatField()
	numTurns = models.FloatField()
	gameState = JSONField()
	payoffs = JSONField()
	epoch = models.FloatField()
	turn = models.FloatField()
	surveyID = models.CharField(max_length=300)