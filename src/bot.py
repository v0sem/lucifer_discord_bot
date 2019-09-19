import discord
# import youtube_dl
# import asyncio
import os
# import random
from discord.ext import commands

TOKEN = 'NTU5ODA2OTYyNjAzMjYxOTky.XYPHcQ.XsO7X7xk_cfYD33V3LSLlrOKfBg'
client = discord.client
bot = commands.Bot(command_prefix='*')

PLAYLISTS_PATH = 'C:/Users/psr19/PycharmProjects/lucifer_discord_bot/database/playlists/'
DESCRIPTION = 'with your soul'
VOICE_ERROR = 'You fucked up somehow, wowee'

extensions = []


@bot.event
async def on_ready():
    print('Bot online and ready.')
    game = discord.Game("With your soul")
    await bot.change_presence(activity=game)

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(extension + " loaded")
        except Exception as e:
            print("{} can't be loaded --> {}".format(extension, e))


# Main Music Functions
@bot.command(pass_context=True)
async def join(ctx):
    """Joins the voice channel you are currently in
    Lucifer gets angry if you are not in a voice channel"""
    try:
        ch = ctx.message.author.voice.channel
        await ch.connect()
        await ctx.message.channel.send('Joined voice channel')
    except discord.ClientException:
        print(e)
        await ctx.message.channel.send('This is not okay dude')


@bot.command(pass_context=True)
async def leave(ctx):
    """Leaves the channel if its in one"""
    server = ctx.message.guild.voice_client
    if server is None:
        await ctx.message.channel.send('This is not okay dude')
    else:
        await server.disconnect()


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

