import aiohttp
import os
import json

from dotenv import dotenv_values
from parcer import get_file_links
from typing import List, Dict

class SetUp:
	"""
	Purpose of this class is to prepare project for usage.
	When it initializes, it gets all required values from .env and
	additionally creates a session which will be used by api.
	"""
	def __init__(self) -> None:
		config = dotenv_values('.env')
		self.PROD_URL = config['PROD_URL']
		self.APP_TOKEN = config['APP_TOKEN']
		self.session =  aiohttp.ClientSession(self.PROD_URL)
		self.db = self.get_db()
		self.headers = {
			'Authorization': f'Bearer {self.APP_TOKEN}'
			}

	def get_db(self) -> dict :
		if not os.path.exists('db.json'):
			get_file_links()
		with open('db.json', 'r', encoding='utf-8') as db:
			return json.load(db)

class BaseRequest(SetUp):
	"""

	Args:
		SetUp (Obj): inheriting all

	Returns:
		Dict: Returns a dict which will be deserialized in menu and printed out for a user
	"""
	#Default values for api
	region = 'ru'
	clan_id = '647d6c53-b3d7-4d30-8d08-de874eb1d845'
	item = 'y1q9'


	async def regions(self):
		async with self.session.get('/regions') as response:
			self.session.close()
			return await response.json()

	async def emission(self, region):
		async with self.session.get(f'/{region}/emission',  headers=self.headers) as response:
			return await response.json()


	# Metods for getting information about clans
	async def clan_info(self, clan_id:str = clan_id, region:str = region, ) -> dict:
		async with self.session.get(f'/{region}/clan/{clan_id}/info', headers=self.headers) as response:
				return await response.json()

	async def clan_list(self, region:str = region) -> dict:
			async with self.session.get(f'/{region}/clans/', headers=self.headers) as response:
				return await response.json()

	async def clan_members(self, region=region, clan_id=clan_id):
		async with self.session.get(f'/{region}/clan/{clan_id}/members', headers=self.headers) as response:
				if response.status != 200:
					return 'You cannot view members of this clan because you dont have character there '
				return response.json()

	# Metods for getting information about Users characters

	async def profile(self, character, region=region) -> dict:
		async with self.session.get(f'/{region}/character/by-name/{character}/profile', headers=self.headers) as response:
				return await response.json()

	async def list_of_chars(self, region=region,) -> dict:
		async with self.session.get(f'/{region}/characters', headers=self.headers) as response:
				return await response.json()

	# Metods for getting information about auction
	async def auction_item_history(self, region=region, item=item) -> dict:
		try:
			item_id =  self.db[item] #searching items id by its name in db
		except KeyError:
			return False
		async with self.session.get(f'/{region}/auction/{item_id}/history', headers=self.headers) as response:
			if response.status == 400:
				return False
			return await response.json()

	async def auction_lots(self, region=region, item=item) -> dict:
		try:
			item_id =  self.db[item] #searching items id by its name in db
		except KeyError:
			return False
		async with self.session.get(f'/{region}/auction/{item_id}/lots', headers=self.headers) as response:
			if response.status == 400:
				return False
			return await response.json()