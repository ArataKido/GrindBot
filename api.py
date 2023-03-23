import aiohttp
import asyncio
from config import DEMO_URL, PROD_URL, APP_TOKEN, USER_TOKEN


class BaseRequests():
	#TODO refactor whole class and use one session for all methods
	# instead of making new session in each method
	headers = {
		'Authorization': f'Bearer {USER_TOKEN}'
		}
	region = 'ru'
	clan_id = '647d6c53-b3d7-4d30-8d08-de874eb1d845'
	character = ''
	item = 'y1q9'

	async def regions(self):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get('/regions') as response:
				return await response.json()

	async def emission(self, region):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/emission',  headers=self.headers) as response:
				return await response.json()


	# Metods for getting information about clans
	async def clan_info(self, clan_id=clan_id, region=region, ):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/clan/{clan_id}/info', headers=self.headers) as response:
				return await response.json()

	async def clan_list(self, region=region):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/clans/', headers=self.headers) as response:
				return await response.json()

	async def clan_members(self, region=region, clan_id=clan_id):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/clan/{clan_id}/members', headers=self.headers) as response:
				return await response.json()

	# Metods for getting information about Users characters

	async def profile(self, region=region, character=character):
		#TODO For some reason this method does work, need to check it with abvadabra
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/character/by-name/{character}/profile', headers=self.headers) as response:
				return await response.json()

	async def list_of_chars(self, region=region,):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/characters', headers=self.headers) as response:
				return await response.json()

	# Metods for getting information about auction
	async def auction_item_history(self, region=region, item=item):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/auction/{item}/history', headers=self.headers) as response:
				return await response.json()

	async def auction_lots(self, region=region, item=item):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/auction/{item}/lots', headers=self.headers) as response:
				return await response.json()
