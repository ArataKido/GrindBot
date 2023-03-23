import concurrent.futures
import aiohttp
import asyncio
import sys
import os

from api import BaseRequests
from datetime import datetime


class Menu(BaseRequests):
#TODO Do i rly need a class??
#TODO Dont rly like how the current menu looks like.
# Need to come up with better UI

#TODO data is being retrieved in json format which is not rly readable for users.
#Need to find better way to provide data.


	menu_options = "1:Clans\n2:Users\
					\n3:Emission\n4:Region\
					\n5:Auction\n6:Quit\n>> "
	clan_options = "1:List of Clans\n2:Clan Members\
					\n3:Clan information\n4:Back to menu\
					\n>> "
	auction_options = "1:Active lots\n2:Item history\
		\n3:Back to menu\n>> "
	profile_options = "1:List of Characters\n2:Characters Profile\
	\n3:Back to menu\n>> "

	def create_loop(self, method ):
		loop = asyncio.get_running_loop()
		loop.run_in_executor(None, method)
		return loop

	async def clans(self):
		user_input = input(f"Please select one of the options\n{self.clan_options}")

		match int(user_input):
			case 1:
				await self.clan_list()
			case 2:
				clan_id = input('Please provide clans id to get information about its members \n>> ')
				await self.clan_members(region='ru', clan_id=clan_id)
			case 3:
				clan_id = input('Please write clans id which you want to look up\n>> ')
				await self.clan_info(region='ru', clan_id=clan_id)
			case 4:
				await self.menu()
			case _:
				print('Wrong input! Please try again')

	async def auction(self):
		user_input = input(f"Please select one of the options\n{self.auction_options}")
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
		user_input = input(f"Please select one of the options\n{self.profile_options}")
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


	async def menu(self):
		user_input = input(f'Welcome to StalcBot!\nPlease select one of the following options.\n{self.menu_options}')
		while True:
			match int(user_input):
				case 1:
					await asyncio.create_task(self.clans())
				case 2:
					await asyncio.create_task(self.profiles())
				case 3:
					await asyncio.create_task(self.last_emission())
					await asyncio.create_task(self.menu())
				case 4:
					await asyncio.create_task(self.regions())
				case 5:
					await asyncio.create_task(self.auction())
				case 6:
					sys.exit(0)
				case _:
					print('Wrong input! Please try it again')



menu = Menu()
asyncio.run(menu.menu())