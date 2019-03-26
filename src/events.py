import discord
import event_manager
from discord.ext import commands

IMAGENES_DIR = 'images/'
ADDED_MSG = ' Added correctly OwO'
DELETED_MSG = ' Deleted correctly UwU'

class Events:
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def viva(self):
		await self.client.say('~Viva España~')
	
	@commands.command(pass_context=True)
	async def horario(self, ctx):
		try:
			await self.client.send_file(ctx.message.channel, 
				IMAGENES_DIR + ctx.message.content[9:12] + '.png')
		except Exception as e:
			await self.client.say(event_manager.format_error_message('horario group'))

	@commands.command()
	async def show_all(self):
		await self.client.say(event_manager.read_events())
	
	@commands.command()
	async def show(self):
		await self.client.say(event_manager.pretty_events())
	
	@commands.command()
	async def add(self, *args):
		try:
			event_manager.add_event(args[0], args[1], args[2], args[3])
			await self.client.say(ADDED_MSG)
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'add' + ' name day month year'))
	
	@commands.command()
	async def search_name(self, name):
		try:
			await self.client.say(event_manager.search_events_name(name))
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'search_name' + '  name'))
	
	@commands.command()
	async def search_day(self, day):
		try:
			await self.client.say(event_manager.search_events_day(day))
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'search_day' + '  day'))
	
	@commands.command()
	async def search_month(self, month):
		try:

			await self.client.say(event_manager.search_events_month(month))
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'search_month' + '  month'))

	@commands.command()
	async def search_year(self, year):
		try:
			await self.client.say(event_manager.search_events_year(year))
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'search_year' + '  year'))

	@commands.command()
	async def delete(self, uid):
		try:
			event_manager.del_event(uid)

			await self.client.say(DELETED_MSG)
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'del' + ' uid'))


def setup(client):
	client.add_cog(Events(client))