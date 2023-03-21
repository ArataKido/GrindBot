import aiohttp
import asyncio
from config import DEMO_URL, PROD_URL, APP_TOKEN, USER_TOKEN


class BaseRequests():
	#TODO refactor whole class and use one session for all methods
	# instead of making new session in each method
	session = None
	headers = 	{
		'Authorization': f'Bearer {USER_TOKEN}'
		}

	async def regions(self):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get('/regions') as response:
				print(await response.json())

	async def emission(self, region):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/emission',  headers=self.headers) as response:
				print(await response.json())


	# Metods for getting information about clans
	async def clan_info(self, region, clan_id):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/clan/{clan_id}/info', headers=self.headers) as response:
				print(await response.json(), end='\n\n')

	async def clan_list(self, region):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/clans/', headers=self.headers) as response:
				print(await response.json(),end='\n\n')

	async def clan_members(self, region, clan_id):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/clan/{clan_id}/members', headers=self.headers) as response:
				print(await response.json(), end='\n\n')

	# Metods for getting information about Users characters

	async def profile(self, region, character):
		#TODO For some reason this method does work, need to check it with abvadabra
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/character/by-name/{character}/profile', headers=self.headers) as response:
				print(await response.json(), end='\n\n')

	async def list_of_chars(self, region,):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/characters', headers=self.headers) as response:
				print(await response.json(), end='\n\n')

	# Metods for getting information about auction
	async def auction_item_history(self, region, item):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/auction/{item}/history', headers=self.headers) as response:
				print(await response.json(), end='\n\n')

	async def auction_lots(self, region, item):
		async with aiohttp.ClientSession(DEMO_URL) as session:
			async with session.get(f'/{region}/auction/{item}/lots', headers=self.headers) as response:
				print(await response.json(), end='\n\n')



# loop.run_until_complete(obj.clan_list(region='ru'))
obj = BaseRequests()
loop = asyncio.get_event_loop()
# loop.run_until_complete(obj.clan_list(region='ru' ))
# loop.run_until_complete(obj.clan_info(region='ru', clan_id='647d6c53-b3d7-4d30-8d08-de874eb1d845' ))
# loop.run_until_complete(obj.clan_members(region='ru', clan_id='647d6c53-b3d7-4d30-8d08-de874eb1d845' ))
# loop.run_until_complete(obj.list_of_chars(region='ru' ))
# loop.run_until_complete(obj.profile(region='ru', character='Test-2' ))
# loop.run_until_complete(obj.regions ())
# loop.run_until_complete(obj.emission (region='ru'))
loop.run_until_complete(obj.auction_lots (region='ru', item='y1q9'))
loop.run_until_complete(obj.auction_item_history (region='ru', item='y1q9'))
