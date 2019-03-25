import discord
import youtube_dl
from discord.ext import commands

VOICE_ERROR = 'You fucked up somehow, wowee'

TOKEN = 'NTU5ODA2OTYyNjAzMjYxOTky.D3q0yw.C0noUcSN3AyC_LA-wqX5JoVJObw'
client = commands.Bot(command_prefix = '~')

players = {}

@client.event
async def on_ready():
	print('Bot online and ready.')

@client.command(pass_context=True)
async def join(ctx):
	try:
		ch = ctx.message.author.voice.voice_channel
		await client.join_voice_channel(ch)
		await client.send_message(ctx.message.channel, 'Joined voice channel')
	except Exception as e:
		await client.send_message(ctx.message.channel,'This is not okay dude')

@client.command(pass_context=True)
async def leave(ctx):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	if voice_client == None:
		await client.say('This is not okay dude')
	else:
		await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, *url):

	query =' '.join(url)

	try:
		server = ctx.message.server
		voice_client = client.voice_client_in(server)
		player = await voice_client.create_ytdl_player(query, ytdl_options={'default_search': 'auto'})
		players[server.id] = player
		player.start()
	except Exception as e:
		print(e)
		await client.send_message(ctx.message.channel,
			VOICE_ERROR)

client.run(TOKEN)