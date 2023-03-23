from api import BaseRequests
from datetime import datetime

import aiohttp
import asyncio

class Menu(BaseRequests):
#TODO Dont rly like how the current menu looks like.
# Need to come up with better UI

#TODO Do i rly need a class??

	menu_options = """
1:Clans
2:Users
3:Emission
4:Region
5:Auction
6:Quit
	"""
	clan_options = """
1:List of Clans
2:Clan Members
3:Clan information
4:Back to menu
"""
	auction_options = """
1:Active lots
2:Item history
3:Back to menu
	"""
	profile_options = """
1:List of Characters
2:Characters Profile
3:Back to menu
"""


	async def clans(self):
		user_input = input(f"Please select one of the options\n {self.clan_options}")

		match int(user_input):
			case 1:
				await self.clan_list()
			case 2:
				await self.clan_members()
			case 3:
				await self.clan_info()
			case 4:
				await self.menu()
			case _:
				print('Wrong input! Please try again')

	async def auction(self):
		user_input = input(f"Please select one of the options\n {self.auction_options}")
		match int(user_input):
			case 1:
				await self.auction_lots()
			case 2:
				await self.auction_item_history()
			case 3:
				await self.menu()
			case _:
				print('Wrong input! Please try again')

	async def profiles(self):
		user_input = input(f"Please select one of the options\n {self.profile_options}")
		match int(user_input):
			case 1:
				await self.list_of_chars()
			case 2:
				await self.profile()
			case 3:
				await self.menu()
			case _:
				print('Wrong input! Please try again')

	async def last_emission(self, region='ru' ):
		emission = await (self.emission(region=region))
		emission = emission['previousStart']
		emission = datetime.fromisoformat(emission.replace('Z', '+00:00'))
		emission = emission.strftime("%H:%M:%S")
		print(f'Last emission was at : {emission}')
		return emission

	async def menu(self):
		user_input = input(f'Welcome to StalcBot!\nPlease select one of the following options.\n{self.menu_options}\n')
		# while True:
		match int(user_input):
			case 1:
				await self.clans()

			case 2:
				await self.profiles()
			case 3:
				await self.last_emission()
			case 4:
				await self.regions()
			case 5:
				await self.auction()
			# case 6:
			# 	break
			case _:
				print('Wrong input! Please try it again')


menu = Menu()
# loop = asyncio.get_event_loop()
asyncio.run(menu.menu())
