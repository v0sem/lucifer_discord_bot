import discord
import youtube_dl
import asyncio
from discord.ext import commands

VOICE_ERROR = 'You fucked up somehow, wowee'

TOKEN = 'NTU5ODA2OTYyNjAzMjYxOTky.D3q0yw.C0noUcSN3AyC_LA-wqX5JoVJObw'
client = commands.Bot(command_prefix = '~')

songs = asyncio.Queue()
play_next_song = asyncio.Event()
players = {}
title = ''

async def audio_player_task():
	while True:
		play_next_song.clear()
		current = await songs.get()
		global title 
		title = current.title
		players[title] = current
		current.start()
		await play_next_song.wait()


def toggle_next():
    client.loop.call_soon_threadsafe(play_next_song.set)

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
async def play(ctx, url):
	if not client.is_voice_connected(ctx.message.server):
		voice = await client.join_voice_channel(ctx.message.author.voice_channel)
	else:
		voice = client.voice_client_in(ctx.message.server)

	player = await voice.create_ytdl_player(url, ytdl_options={'default_search': 'auto'}, after=toggle_next)

	await songs.put(player)
	await client.say(player.title + ' queued')

@client.command(pass_context=True)
async def pause(ctx):
	players[title].pause()
	await client.say(title + ' paused')

@client.command(pass_context=True)
async def resume(ctx):
	players[title].resume()
	await client.say(title + ' resumed')

@client.command(pass_context=True)
async def skip(ctx):
	players[title].stop()
	await client.say('Skipped')


client.loop.create_task(audio_player_task())
client.run(TOKEN)

