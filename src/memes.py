import discord
from discord.ext import commands

MUSIC = 'database/music/'

class Memes:

	def __init__(self, client):
		self.client = client

	@commands.command(pass_context=True)
	async def viva(self, ctx):
		"""Por Españita"""
		server = ctx.message.server
		voice_client = self.client.voice_client_in(server)
		if voice_client != None:
			await voice_client.disconnect()
		channel = ctx.message.author.voice.voice_channel
		voice_client = await self.client.join_voice_channel(channel)

		player = voice_client.create_ffmpeg_player(MUSIC + 'HimnoEspana.mp3')
		player.start()
		await self.client.say('~Viva España~')

def setup(client):
	client.add_cog(Memes(client))
