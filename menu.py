import asyncio
import sys


from api import BaseRequest
from datetime import datetime
from tabulate import tabulate


class DataSerializer:
#TODO Find better name for this class. Lol
#TODO Do i even need it now? anyways ill keep it for now idk why
    """This class is responsible for processing JSON returned by the API
    and printing the required information to the user in a readable format.
    """
    async def serialize(self, column_names:list[str], data:list[int, str]) -> None:
        print(tabulate(data, headers=column_names, tablefmt="grid", showindex="always"))



class Menu:
#TODO Do i rly need a class??

    MENU_OPTIONS = "1:Clans\n2:Users\
                    \n3:Emission\n4:Region\
                    \n5:Auction\n6:Quit\n>> "
    CLAN_OPTIONS = "1:List of Clans\n2:Clan Members\
                    \n3:Clan information\n4:Back to menu\
                    \n>> "
    AUCTION_OPTIONS = "1:Active lots\n2:Item history\
        \n3:Back to menu\n>> "
    PROFILE_OPTIONS = "1:List of Characters\n2:Characters Profile\
    \n3:Back to menu\n>> "

    def __init__(self,) -> None:
        self.serializer = DataSerializer()
        self.request = BaseRequest()

    async def clans(self) -> None:
        user_input = input(f"\nPlease select one of the options\n{self.CLAN_OPTIONS}")

        match user_input:
            case '1':

                clans =  await self.request.clan_list()

                if not clans:
                    return print("Something went wrong")
                column_names= ['Tag', 'Name', 'Members', 'Faction', 'Leader', 'ID']
                data = []
                for clan in clans['data']:
                    clan_info = [clan['tag'], clan['name'], clan['memberCount'],
                                    clan['alliance'], clan['leader'],clan['id']]
                    data.append(clan_info)
                await self.DataSerializer.serialize(column_names=column_names, data=data)
            case '2':
                print("Still Working On It")
                # clan_id = input('Please provide clans id to get information about its members \n>> ')
                # if not clan_id:
                # 	return print('ACHTUNG!!! YOUR MESSAGE IS EMPTY!')
                # members = await self.request.clan_members(region='ru', clan_id=clan_id)
            case '3':
                clan_id = input('Please write clans id which you want to look up\n>> ')
                if not clan_id:
                    return print('ACHTUNG!!! YOUR MESSAGE IS EMPTY!')
                clan = await self.request.clan_info(region='ru', clan_id=clan_id)

                column_names= ['Tag', 'Name', 'Members', 'Level', 'Faction', 'Leader', 'ID']
                data = [[clan['tag'], clan['name'], clan['memberCount'], clan['level'],
                        clan['alliance'], clan['leader'],clan['id']]]
                await self.DataSerializer.serialize(column_names=column_names, data=data)

            case '4':

                await self.menu()
            case _:

                print('Wrong input! Please try again')
                await self.clans()

    async def auction(self)-> None:
        user_input = input(f"\nPlease select one of the options\n{self.auction_options}")
        match user_input:
            case '1':
                item = input('Please enter the name of a item you are searching for \n>> ')
                if not item:
                    return print('ACHTUNG!!! YOUR MESSAGE IS EMPTY!')
                lots = await self.request.auction_lots(item=item)

                if lots and len(lots['lots']) != 0 :
                    column_names = ['ItemId', 'Start Price','Bet Price', 'Buyout']
                    data = []
                    for lot in lots['lots']:
                        lot_info = [lot['itemId'], lot.get('startPrice'), lot.get('currentPrice'), lot.get('buyoutPrice')]
                        data.append(lot_info)
                    await self.DataSerializer.serialize(column_names=column_names, data=data)

                else:
                    print("There is no such item on auction!")
            case '2':
                print('Still Working On It')
                # item  = input('Please enter the name of a item you are searching for \n>> ')
                # history = await self.request.auction_item_history(item=item)
                # if not history:
                # 	return print('Item was not found')
                # print(history)
            case '3':
                await self.menu()
            case _:
                print('Wrong input! Please try again')
                await self.auction()

    async def profiles(self) -> None:
        user_input = input(f"\nPlease select one of the options\n{self.PROFILE_OPTIONS}")
        match user_input:
            case '1':
                chars = await self.request.list_of_chars()
            case '2':

                user_input = input('Please write characters name\n>> ')
                character = await self.request.profile(character=user_input)

                column_names= ['Username', 'Alliance', 'Status', "Last Login" ]
                data = [[character['username'], character['alliance'], character['status'], character['lastLogin']]]
                await self.DataSerializer.serialize(column_names=column_names, data=data)
            case '3':
                await self.menu()
            case _:

                print('Wrong input! Please try again')
                await self.profiles()

    async def last_emission(self, region:str ='ru' )-> None:
        emission = await (self.request.emission(region=region))
        emission = emission['previousStart']
        emission = datetime.fromisoformat(emission.replace('Z', '+00:00'))
        emission = emission.strftime("%H:%M:%S")
        print(f'Last emission was at : {emission}')


    async def menu(self) -> None:
        #TODO Check if session is being closed
        print('\nWelcome to StalcBot!')
        user_input = input(f'Please select one of the following options.\n{self.MENU_OPTIONS}')
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

                    await asyncio.create_task(self.request.regions())
                case '5':

                    await asyncio.create_task(self.auction())
                case '6':

                    sys.exit(0)
                case _:
                    print('\nWrong input! Please try it again\n')
                    await asyncio.create_task(self.menu())



menu = Menu()
asyncio.get_event_loop().run_until_complete(menu.menu())
