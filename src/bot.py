import discord
import youtube_dl
import asyncio
import os
from discord.ext import commands

VOICE_ERROR = 'You fucked up somehow, wowee'

TOKEN = ''
client = commands.Bot(command_prefix = '*')

PLAYLISTS_PATH = 'database/playlists/'
DESCRIPTION = 'with your soul'
MUSIC = 'database/music/'

names = asyncio.Queue()
songs = asyncio.Queue()
play_next_song = asyncio.Event()
players = {}
extensions = ['events', 'memes']


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
		print(extension + " loaded")

######################## Main Music Functions ##############################

async def audio_player_task():
	while True:
		try:
			play_next_song.clear()
			current = await songs.get()
			title = await names.get()
			players[1] = current
			await client.change_presence(game=discord.Game(name=title))
			current.start()
			await play_next_song.wait()
			await client.change_presence(game=discord.Game(name=DESCRIPTION))
			os.remove(MUSIC + title + '.opus')
		except Exception as e:
			print(e)
			continue



def toggle_next():
    client.loop.call_soon_threadsafe(play_next_song.set)

@client.command(pass_context=True)
async def join(ctx):
	"""Joins the voice channel you are currently in
	Lucifer gets angry if you are not in a voice channel"""
	try:
		ch = ctx.message.author.voice.voice_channel
		voice = await client.join_voice_channel(ch)
		await client.send_message(ctx.message.channel, 'Joined voice channel')
	except Exception as e:
		print(e)
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
	Adds the song to a queue and starts playing the queue
	[URLS ARE NOT SUPPORTED NOW]"""
	query =' '.join(url)
	if not client.is_voice_connected(ctx.message.server):
		voice = await client.join_voice_channel(ctx.message.author.voice_channel)
	else:
		voice = client.voice_client_in(ctx.message.server)
		
	outtmpl = MUSIC + query + '.%(ext)s'

	ydl_opts = {
		'format': 'bestaudio',
		'outtmpl': outtmpl,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'opus',
			'preferredquality': '192',
   		}],
		'default_search': 'auto'
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([query])
	try:
		player = voice.create_ffmpeg_player(MUSIC + query + '.opus', after=toggle_next)
	except Exception as e:
		print(e)
		await client.say('There was something wrong, maybe you used a url')
		return

	await names.put(query)
	await songs.put(player)
	await client.say(query + ' queued')

@client.command()
async def pause():
	"""Pauses the song currently playing"""
	try:
		players[1].pause()
		await client.say('Paused')
	except Exception as e:
		print(e)
		await client.say("There *probably* isn't any song playing")

@client.command()
async def resume():
	"""Resumes the song if its paused"""
	try:
		players[1].resume()
		await client.say('Resumed')
	except Exception as e:
		print(e)
		await client.say("There *probably* ins't any song paused")

@client.command()
async def skip():
	"""Skips to the next song in the queue"""
	try:
		players[1].stop()
		await client.say('Skipped')
	except Exception as e:
		print(e)
		await client.say('Something went wrong')

@client.command(pass_context=True)
async def create_playlist(ctx, playlist_name):
	"""Creates an empty playlist file"""
	try:
		file = open(PLAYLISTS_PATH + ctx.message.server.id + playlist_name + '.txt', 'r')
		await client.say('Playlist ' + playlist_name + ' already exists')
	except Exception as e:
		file = open(PLAYLISTS_PATH + ctx.message.server.id + playlist_name + '.txt', 'w')
		await client.say('Playlist ' + playlist_name + ' created')

@client.command(pass_context=True)
async def delete_playlist(ctx, playlist_name):
	"""Delets playlist with the given name"""
	try:
		os.remove(PLAYLISTS_PATH + ctx.message.server.id + playlist_name + '.txt')
		await client.say('Playlist is no more')
	except Exception as e:
		print(e)
		await client.say('Playlist (probably) is still alive')

@client.command(pass_context=True)
async def add_to_playlist(ctx, playlist_name, *song_name):
	"""Adds a song to a playlist, duh"""
	try:
		file = open(PLAYLISTS_PATH + ctx.message.server.id + playlist_name + '.txt', 'r')
		file.close()
		file = open(PLAYLISTS_PATH + ctx.message.server.id + playlist_name + '.txt', 'a')

		file.write(' '.join(song_name) + '\n')
		await client.say(' '.join(song_name) + ' was added to ' + playlist_name)
		file.close()
	
	except Exception as e:
		print(e)
		await client.say('Playlist most likely does not exist')

@client.command(pass_context=True)
async def remove_from_playlist(ctx, playlist_name, *song):
	song_name = ' '.join(song)

	try:
		with open(PLAYLISTS_PATH + ctx.message.server.id + playlist_name + '.txt', 'r') as f:
			lines = f.readlines()
		with open(PLAYLISTS_PATH + ctx.message.server.id + playlist_name + '.txt', 'w') as f:
			for line in lines:
				if line.strip("\n") != song_name:
					f.write(line)
				else:
					 await client.say(song_name + ' deleted')
		f.close()
	except Exception as e:
		print(e)
		await client.say('You probably messed up somewhere')


@client.command(pass_context=True)
async def playlist(ctx, playlist_name):
	"""Adds all songs from playlist_name into queue"""
	try:
		file = open(PLAYLISTS_PATH + ctx.message.server.id + playlist_name + '.txt', 'r')
		all_songs = file.read()
		query = all_songs.split("\n")
		if not client.is_voice_connected(ctx.message.server):
			voice = await client.join_voice_channel(ctx.message.author.voice_channel)
		else:
			voice = client.voice_client_in(ctx.message.server)
		for song in query:
			print(song)
			if len(song) > 2:
				outtmpl = MUSIC + song + '.%(ext)s'
				ydl_opts = {
					'format': 'bestaudio',
					'outtmpl': outtmpl,
					'postprocessors': [{
						'key': 'FFmpegExtractAudio',
						'preferredcodec': 'opus',
						'preferredquality': '192',
			   		}],
					'default_search': 'auto'
				}
				with youtube_dl.YoutubeDL(ydl_opts) as ydl:
					ydl.download([song])
				try:
					player = voice.create_ffmpeg_player(MUSIC + song + '.opus', after=toggle_next)
				except Exception as e:
					print(e)
					await client.say('There was a problem with' + song)
					continue

				await songs.put(player)
				await names.put(song)
		await client.say(playlist_name + ' is queued')
	
	except Exception as e:
		print(e)
		await client.say('Playlist doesnt exist or isnt reachable')

client.loop.create_task(audio_player_task())
client.run(TOKEN)

