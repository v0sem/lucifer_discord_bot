import discord
from discord.ext import commands

TRIVIA = 'database/trivia/questions.txt'
puntuations = {}

class Trivia:

	def __init__(self, client):
		self.client = client
	
	def getQuestionAnswers():
		
		return{
			'question': question,
			'a': a,
			'b': b,
			'c': c,
			'd': d,
			'answer': answer
		}

def setup(client):
	client.add_cog(Trivia(client))