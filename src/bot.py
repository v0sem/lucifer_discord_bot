import discord
import youtube_dl
import asyncio
import os
from discord.ext import commands

VOICE_ERROR = 'You fucked up somehow, wowee'

TOKEN = 'NTU5ODA2OTYyNjAzMjYxOTky.D3q0yw.C0noUcSN3AyC_LA-wqX5JoVJObw'
client = commands.Bot(command_prefix = '*')

PLAYLISTS_PATH = 'database/playlists/'
DESCRIPTION = ' with your soul'

songs = asyncio.Queue()
play_next_song = asyncio.Event()
players = {}
title = ''
extensions = ['events']

@client.event
async def on_ready():
	print('Bot online and ready.')
	await client.change_presence(game=discord.Game(name=DESCRIPTION))

if __name__ == "__main__":
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as e:
			print("{} can't be loaded --> {}".format(extension, e))


######################## Main Music Functions ##############################

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

@client.command(pass_context=True)
async def join(ctx):
	"""Joins the voice channel you are currently in
	Lucifer gets angry if you are not in a voice channel"""
	try:
		ch = ctx.message.author.voice.voice_channel
		await client.join_voice_channel(ch)
		await client.send_message(ctx.message.channel, 'Joined voice channel')
	except Exception as e:
		await client.send_message(ctx.message.channel,'This is not okay dude')

@client.command(pass_context=True)
async def leave(ctx):
	"""Leaves the channel if its in one"""
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	if voice_client == None:
		await client.say('This is not okay dude')
	else:
		await voice_client.disconnect()


@client.command(pass_context=True)
async def play(ctx, *url):
	"""Plays a song or looks up one on youtube
	Adds the song to a queue and starts playing the queue"""
	query =' '.join(url)
	if not client.is_voice_connected(ctx.message.server):
		voice = await client.join_voice_channel(ctx.message.author.voice_channel)
	else:
		voice = client.voice_client_in(ctx.message.server)

	player = await voice.create_ytdl_player(query, 
		ytdl_options={'default_search': 'auto'}, after=toggle_next)

	await songs.put(player)
	await client.say(player.title + ' queued')

@client.command()
async def pause():
	"""Pauses the song currently playing"""
	players[title].pause()
	await client.say(title + ' paused')

@client.command()
async def resume():
	"""Resumes the song if its paused"""
	players[title].resume()
	await client.say(title + ' resumed')

@client.command()
async def skip():
	"""Skips to the next song in the queue"""
	players[title].stop()
	await client.say('Skipped')

@client.command()
async def create_playlist(playlist_name):
	"""Creates an empty playlist file"""
	try:
		file = open(PLAYLISTS_PATH + playlist_name + '.txt', 'r')
		await client.say('Playlist ' + playlist_name + ' already exists')
	except Exception as e:
		file = open(PLAYLISTS_PATH + playlist_name + '.txt', 'w')
		await client.say('Playlist ' + playlist_name + ' created')

@client.command()
async def delete_playlist(playlist_name):
	"""Delets playlist with the given name"""
	try:
		os.remove(PLAYLISTS_PATH + playlist_name + '.txt')
		await client.say('Playlist is no more')
	except Exception as e:
		print(e)
		await client.say('Playlist (probably) is still alive')

@client.command()
async def add_to_playlist(playlist_name, *song_name):
	"""Adds a song to a playlist, duh"""
	try:
		file = open(PLAYLISTS_PATH + playlist_name + '.txt', 'r')
		file.close()
		file = open(PLAYLISTS_PATH + playlist_name + '.txt', 'a')

		file.write(' '.join(song_name) + '\n')
		await client.say(' '.join(song_name) + ' was added to ' + playlist_name)
		file.close()
	
	except Exception as e:
		print(e)
		await client.say('Playlist most likely does not exist')

client.loop.create_task(audio_player_task())
client.run(TOKEN)

