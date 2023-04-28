import aiohttp
import asyncio
import os
import json

from parce import get_file_links


class BaseRequests():
	#TODO refactor whole class and use one session for all methods
	# instead of making new session in each method


	def __init__(self):
		if not os.path.exists('utils/db.json'):
			get_file_links()
		with open('db.json', 'r', encoding='utf-8') as db:
			self.db = json.load(db)

		self.session = aiohttp.ClientSession(PROD_URL)
		headers = {
			'Authorization': f'Bearer {APP_TOKEN}'
			}


	async def regions(self):
		async with aiohttp.ClientSession(PROD_URL) as session:
			async with session.get('/regions') as response:
				return await response.json()

	async def emission(self,):
		async with self.session.get(f'emission',  headers=self.headers) as response:
			return await response.json()


	# Metods for getting information about clans
	async def clan_info(self, clan_id,):
		async with self.session.get(f'clan/{clan_id}/info', headers=self.headers) as response:
				return await response.json()

	async def clan_list(self,):
			async with self.session.get(f'clans/', headers=self.headers) as response:
				return await response.json()

	async def clan_members(self, clan_id):
		async with self.session.get(f'clan/{clan_id}/members', headers=self.headers) as response:
				if response.status != 200:
					return 'You cannot view members of this clan because you dont have character there '
				return response.json()

	# Metods for getting information about Users characters

	async def profile(self, character):
		async with self.session.get(f'character/by-name/{character}/profile', headers=self.headers) as response:
				return await response.json()

	async def list_of_chars(self,):
		async with self.session.get(f'characters', headers=self.headers) as response:
				return await response.json()

	# Metods for getting information about auction
	async def auction_item_history(self, item):
		try:
			item_id =  self.db[item]
		except KeyError:
			return False
		async with self.session.get(f'auction/{item_id}/history', headers=self.headers) as response:
			if response.status == 400:
				return False
			return await response.json()

	async def auction_lots(self, item):
		try:
			item_id =  self.db[item]
		except KeyError:
			return False
		async with self.session.get(f'auction/{item_id}/lots', headers=self.headers) as response:
			if response.status == 400:
				return False
			return await response.json()