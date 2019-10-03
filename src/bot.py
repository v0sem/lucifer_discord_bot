from __future__ import unicode_literals
from threading import Lock, Thread
import discord
import youtube_dl
# import asyncio
import os
# import random
from discord.ext import commands

TOKEN = ''
client = discord.client
bot = commands.Bot(command_prefix='*')

PLAYLISTS_PATH = 'database/playlists/'
DESCRIPTION = 'with your soul'
VOICE_ERROR = 'You fucked up somehow'
MUSIC = 'database/music/tmp/'

extensions = []
mutex = Lock()

def queue(voice_ch, save):
    mutex.acquire()
    try:
        voice_ch.play(discord.FFmpegPCMAudio(MUSIC + save + '.mp3'))

        while voice_ch.is_playing() or voice_ch.is_paused():
            pass
    finally:
        mutex.release()    

@bot.event
async def on_ready():
    print('Bot online and ready.')
    game = discord.Game("With your soul")
    await bot.change_presence(activity=game)

@bot.event
async def on_disconnect():
    for file_ in os.listdir(MUSIC):
        file_path = os.path.join(MUSIC, file_)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(extension + " loaded")
        except Exception as e:
            print("{} can't be loaded --> {}".format(extension, e))


@bot.command(pass_context=True)
@commands.is_owner()
async def out(ctx):
    await ctx.bot.logout()

# Main Music Functions
@bot.command(pass_context=True)
async def join(ctx):
    """Joins the voice channel you are currently in
    Lucifer gets angry if you are not in a voice channel"""
    try:
        ch = ctx.message.author.voice.channel
        await ch.connect()
        await ctx.message.channel.send('Joined voice channel')
    except (discord.ClientException, AttributeError) as e:
        print(e)
        await ctx.message.channel.send('This is not okay dude')


@bot.command(pass_context=True)
async def leave(ctx):
    """Leaves the channel if its in one"""
    voice_ch = ctx.message.guild.voice_client
    if voice_ch is None:
        await ctx.message.channel.send('This is not okay dude')
    else:
        await voice_ch.disconnect()

@bot.command(pass_context=True)
async def play(ctx, *song_name):
    """Plays the requested song"""
   
    voice_ch = ctx.message.guild.voice_client
    
    if voice_ch is None:
        await join.invoke(ctx)

    voice_ch = ctx.message.guild.voice_client
    if voice_ch is None:
        return
    
    query = ' '.join(song_name)
    save = ''.join(song_name)
    outtmpl = MUSIC + save + '.%(ext)s'

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'defaultsearch': 'ytsearch'
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['ytsearch:'+ query])
    
    #voice_ch.play(discord.FFmpegPCMAudio(MUSIC + save + '.mp3'))
    thread = Thread(target = queue, args = (voice_ch, save))
    thread.start()


# Playlist functions
@bot.command(pass_context=True)
async def create_playlist(ctx, playlist_name):
    """Creates an empty playlist file"""
    try:
        path = PLAYLISTS_PATH + playlist_name
        path = os.path.realpath(path)
        file = open(path + '.txt', 'r')
        await ctx.message.channel.send('Playlist ' + playlist_name + ' already exists')
        file.close()
    except FileNotFoundError:
        open(path + '.txt', 'w+')
        await ctx.message.channel.send('Playlist ' + playlist_name + ' created')


@bot.command(pass_context=True)
async def delete_playlist(ctx, playlist_name):
    """Delets playlist with the given name"""
    try:
        os.remove(PLAYLISTS_PATH + playlist_name + '.txt')
        await ctx.message.channel.send('Playlist is no more')
    except FileNotFoundError:
        print(e)
        await ctx.message.channel.send('Playlist (probably) is still alive or didn\'t exist in the first place')


@bot.command(pass_context=True)
async def add_to_playlist(ctx, playlist_name, *song_name):
    """Adds a song to a playlist, duh"""
    try:
        file = open(PLAYLISTS_PATH + playlist_name + '.txt', 'r')
        file.close()
        file = open(PLAYLISTS_PATH + playlist_name + '.txt', 'a')

        file.write(' '.join(song_name) + '\n')
        await ctx.message.channel.send(' '.join(song_name) + ' was added to ' + playlist_name)
        file.close()

    except FileNotFoundError:
        print(e)
        await ctx.message.channel.send('Playlist most likely does not exist')


@bot.command(pass_context=True)
async def remove_from_playlist(ctx, playlist_name, *song):
    song_name = ' '.join(song)

    try:
        with open(PLAYLISTS_PATH + playlist_name + '.txt', 'r') as f:
            lines = f.readlines()
        with open(PLAYLISTS_PATH + playlist_name + '.txt', 'w') as f:
            for line in lines:
                if line.strip("\n") != song_name:
                    f.write(line)
                else:
                    await ctx.message.channel.send(song_name + ' deleted')
        f.close()
    except FileNotFoundError:
        print(e)
        await ctx.message.channel.send('You probably messed up somewhere')


@bot.command(pass_context=True)
async def show_playlist(ctx, playlist_name):
    try:
        with open(PLAYLISTS_PATH + playlist_name + '.txt', 'r') as f:
            lines = f.readlines()
            await ctx.message.channel.send('Playlist ' + playlist_name + ' contains:')
            for line in lines:
                line.strip('\n')
                await ctx.message.channel.send('- ' + line)
    except FileNotFoundError:
        print(e)
        await ctx.message.channel.send('Are you sure about that?')


@bot.command(pass_context=True)
async def show_all_playlist(ctx):
    try:
        for filename in os.listdir(PLAYLISTS_PATH):
            await ctx.message.channel.send(filename)
    except FileNotFoundError:
        print(e)
        await ctx.message.channel.send('Something went wrong')


bot.run(TOKEN)

