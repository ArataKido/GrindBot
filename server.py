import asyncio
import sys
import logging

from menu import Menu

async def handle_client(reader, writer):
    menu = Menu()
    await menu.menu(reader, writer)

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
