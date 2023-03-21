import aiohttp
import asyncio
from config import DEMO_URL, PROD_URL, APP_TOKEN, USER_TOKEN


class BaseRequests():
	session = None
	headers = 	{
		'Authorization': f'Bearer {USER_TOKEN}'
		}

	async def __init__(self, session):
		self.session = await session

	# async def start_session(self, *args, **kwargs):
	# 	async with aiohttp.ClientSession(DEMO_URL) as session:
	# 		self.session = session
	# 		return self.session

	async def clan_list(self, region):
		async with self.session.get(f'/{region}/clans/', headers=self.headers) as response:
			print(await response.json())

	async def clan_info(self, region, clan_id):
		async with self.session.get(f'/{region}/clan/{clan_id}/info', headers=self.headers) as response:
				print(await response.json())

	# async def clan_list(self, region):
	# 	async with aiohttp.ClientSession() as session:


# loop.run_until_complete(obj.clan_list(region='ru'))
async def requst(session):
	obj = await BaseRequests(session)
	loop = await asyncio.get_event_loop()
	loop.run_forever()
	loop.run_until_complete(obj.clan_list(region='ru' ))
	loop.run_until_complete(obj.clan_info(region='ru', clan_id=2 ))

async def main():
	async with aiohttp.ClientSession() as session:
		await requst(session)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())