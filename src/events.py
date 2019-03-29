import discord
from discord.ext import commands
import event_manager

IMAGENES_DIR = 'images/'
ADDED_MSG = ' Added correctly OwO'
DELETED_MSG = ' Deleted correctly UwU'

class Events:
	def __init__(self, client):
		self.client = client
	
	@commands.command(pass_context=True)
	async def horario(self, ctx):
		"""Enseña el horario del grupo de informatica de la UAM
		Depende del nombre del grupo"""
		try:
			await self.client.send_file(ctx.message.channel, 
				IMAGENES_DIR + ctx.message.content[9:12] + '.png')
		except Exception as e:
			await self.client.say(event_manager.format_error_message('horario group'))
	
	@commands.command(pass_context=True)
	async def examenes(self, ctx):
		"""Enseña los proximos examenes
		Es una foto, pueden haber ocurrido ya"""
		try:
			await self.client.send_file(ctx.message.channel, 
				IMAGENES_DIR + 'examenes.jpeg')
		except Exception as e:
			await self.client.say(event_manager.format_error_message('No se que leches ha salido mal'))

	@commands.command()
	async def show_all(self):
		"""Enseña todos los eventos guardados"""
		await self.client.say(event_manager.read_events())
	
	@commands.command()
	async def show(self):
		"""Enseña los proximos eventos"""
		await self.client.say(event_manager.pretty_events())
	
	@commands.command()
	async def add(self, name, day, month, year):
		"""Añade un evento a la lista"""
		try:
			event_manager.add_event(name, day, month, year)
			await self.client.say(ADDED_MSG)
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'add' + ' name day month year'))
	
	@commands.command()
	async def search_name(self, name):
		"""Busca un evento dado un nombre"""
		try:
			await self.client.say(event_manager.search_events_name(name))
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'search_name' + '  name'))
	
	@commands.command()
	async def search_day(self, day):
		"""Busca un evento dado un dia"""
		try:
			await self.client.say(event_manager.search_events_day(day))
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'search_day' + '  day'))
	
	@commands.command()
	async def search_month(self, month):
		"""Busca un evento dado un mes"""
		try:

			await self.client.say(event_manager.search_events_month(month))
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'search_month' + '  month'))

	@commands.command()
	async def search_year(self, year):
		"""Busca un evento dado un año"""
		try:
			await self.client.say(event_manager.search_events_year(year))
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'search_year' + '  year'))

	@commands.command()
	async def delete(self, uid):
		"""Elimina un evento"""
		try:
			event_manager.del_event(uid)

			await self.client.say(DELETED_MSG)
		except Exception as e:
			print(e)
			await self.client.say(event_manager.format_error_message(
				'del' + ' uid'))


def setup(client):
	client.add_cog(Events(client))
