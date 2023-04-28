import aiohttp
import asyncio
import os
import json

from dotenv import dotenv_values
from parcer import get_file_links


class SetUp:
	def __init__(self):
		config = dotenv_values('.env')
		self.PROD_URL = config['PROD_URL']
		self.APP_TOKEN = config['APP_TOKEN']
		self.session = aiohttp.ClientSession(self.PROD_URL)
		self.db = self.get_db()
		self.headers = {
			'Authorization': f'Bearer {self.APP_TOKEN}'
			}

	def get_db(self):
		if not os.path.exists('db.json'):
			get_file_links()
		with open('db.json', 'r', encoding='utf-8') as db:
			return json.load(db)

class BaseRequest(SetUp):
	async def regions(self):
		async with self.session.get('/regions') as response:
			return await response.json()

	async def emission(self):
		async with self.session.get(f'emission',  headers=self.headers) as response:
			return await response.json()

	# Metods for getting information about clans
	async def clan_info(self, clan_id):
		async with self.session.get(f'clan/{clan_id}/info', headers=self.headers) as response:
				return await response.json()

	async def clan_list(self):
			async with self.session.get(f'clans', headers=self.headers) as response:
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