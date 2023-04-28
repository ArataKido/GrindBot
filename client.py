import asyncio

async def send_request():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    # Send menu option to the server
    writer.write(b'1\n')
    await writer.drain()

    # Read and print the response from the server
    response = await reader.read()
    print(response.decode())

    # Close the connection
    writer.close()
    await writer.wait_closed()

asyncio.run(send_request())
