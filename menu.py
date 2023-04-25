import asyncio
import sys
import os
import json

from api import BaseRequests
from datetime import datetime


class Serializers():
#TODO Find better name for this class. Lol
	"""Purpose of this class is to proses json which is
		returned by api and print required information to user in most
		readable way

	"""
	async def clan_list_serializer(self, clans:dict):
		#TODO need to validate len of clans data
		n = 1
		print('============= LIST OF CLANS =============')
		for clan in clans['data']:
			print(n)
			print(f"\nClan [{clan['tag']}] {clan['name']}\nMembers: {clan['memberCount']}\
	 				\nFaction: {clan['alliance']}\nLeader: {clan['leader']}")
			n += 1
		print('=========================================')

	async def active_lots_serializers(self, lots:dict):
		if len(lots['lots']) != 0 :
			for lot in lots['lots']:
				print(f"Item: {lot['itemId']}\nBet price: {lot.get('startPrice')}\nBuyout : {lot.get('buyoutPrice')}")
			return True
		print("There is no such item on auction!")
		#TODO REMOVE THIS PRINT, DONT LET NICLAS SEE THIS.

class Menu:
#TODO Do i rly need a class??

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
	serializer = Serializers()
	request = BaseRequests()

	async def clans(self):
		user_input = input(f"\nPlease select one of the options\n{self.clan_options}")

		match user_input:
			case '1':
				clans =  await self.request.clan_list()
				if not clans:
					return print("Something went wrong")
				await self.serializer.clan_list_serializer(clans=clans)
			case '2':
				clan_id = input('Please provide clans id to get information about its members \n>> ')
				if not clan_id:
					return print('ACHTUNG!!! YOUR MESSAGE IS EMPTY!')
				members = await self.request.clan_members(region='ru', clan_id=clan_id)
			case '3':
				clan_id = input('Please write clans id which you want to look up\n>> ')
				if not clan_id:
					return print('ACHTUNG!!! YOUR MESSAGE IS EMPTY!')
				clan = await self.request.clan_info(region='ru', clan_id=clan_id)
			case '4':
				await self.menu()
			case _:
				print('Wrong input! Please try again')
				await self.clans()

	async def auction(self):
		user_input = input(f"\nPlease select one of the options\n{self.auction_options}")
		match user_input:
			case '1':
				item = input('Please enter the name of a item you are searching for \n>> ')
				if not item:
					return print('ACHTUNG!!! YOUR MESSAGE IS EMPTY!')
				lots = await self.request.auction_lots(item=item)
				if not lots:
					return print('Item was not found')
				await self.serializer.active_lots_serializers(lots=lots)
			case '2':
				item  = input('Please enter the name of a item you are searching for \n>> ')
				history = await self.request.auction_item_history(item=item)
				if not history:
					return print('Item was not found')
				print(history)
			case '3':
				await self.menu()
			case _:
				print('Wrong input! Please try again')
				await self.auction()

	async def profiles(self):
		user_input = input(f"\nPlease select one of the options\n{self.profile_options}")
		match user_input:
			case '1':
				chars = await self.request.list_of_chars()
				print(chars)
			case '2':
				user_input = input('Please write characters name\n>> ')
				profile = await self.request.profile(character=user_input)
				print(profile)
			case '3':
				await self.menu()
			case _:
				print('Wrong input! Please try again')
				await self.profiles()

	async def last_emission(self, region='ru' ):
		emission = await (self.request.emission(region=region))
		emission = emission['previousStart']
		emission = datetime.fromisoformat(emission.replace('Z', '+00:00'))
		emission = emission.strftime("%H:%M:%S")
		print(f'Last emission was at : {emission}')


	async def menu(self):
		#TODO Check if session is being closed
		print('\nWelcome to StalcBot!')
		user_input = input(f'Please select one of the following options.\n{self.menu_options}')
		while True:
			match user_input:
				case '1':
					await asyncio.create_task(self.clans())
				case '2':
					await asyncio.create_task(self.profiles())
				case '3':
					await asyncio.create_task(self.last_emission())
					await asyncio.create_task(self.menu())
				case '4':
					await asyncio.create_task(self.regions())
				case '5':
					await asyncio.create_task(self.auction())
				case '6':
					sys.exit(0)
				case _:
					print('\nWrong input! Please try it again\n')
					await asyncio.create_task(self.menu())



menu = Menu()
asyncio.get_event_loop().run_until_complete(menu.menu())
