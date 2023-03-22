from api import BaseRequests

import aiohttp
import asyncio
import datetime

class Menu(BaseRequests):
#TODO Dont rly like how the current menu looks like.
# Need to come up with better UI

#TODO Do i rly need a class??

	menu_options = """
1: Clans
2: Users
3: Emission
4: Region
5: Auction
	"""
	clan_options = """
1:List of Clans
2:Clan Members
3:Clan information
"""
	auction_options = """
1: Active lots
2: Item history
	"""
	profile_options = """
1: List of Characters
2: Characters Profile
"""

	async def menu(self):
		user_input = input(f'Welcome to StalcBot!\nPlease select one of the following options.\n{self.menu_options}\n')

	async def clans(self):
		user_input = input(f"Please select one of the options\n {self.clan_options}")

	async def auction(self):
		user_input = input(f"Please select one of the options\n {self.auction_options}")

	async def profiles(self):
		user_input = input(f"Please select one of the options\n {self.profile_options}")

	async def last_emission(self, loop, region='ru' ):
		emission = await (self.emission(region=region))
		print( datetime.datetime.strptime(emission['currentStart'], '%H:%M:%S %d/%m/%y'))


menu = Menu()
loop = asyncio.get_event_loop()
loop.run_until_complete(menu.last_emission(loop))