import asyncio
import websockets
import json

# stepA
async def stepA():
    async with websockets.connect("wss://stream.binance.com/stream?streams=btcusdt@depth5@100ms/btcusdt@trade") as websocket:
        f = open('stream-data-binance.txt', 'w')

        while 1:
            data = json.loads(await websocket.recv())

            if data['stream'] == 'btcusdt@trade':
                editedData = 'btcusdt@trade, ' + str({k:v for k,v in data['data'].items() if k in ['p', 'q']})
            else:
                editedData = 'btcusdt@depth5@100ms, ' + str(data['data']) 

            f.write(str(editedData) + "\n")

        f.close();

asyncio.get_event_loop().run_until_complete(stepA())


# stepB
async def stepB():
     async with websockets.connect("wss://api.upbit.com/websocket/v1") as websocket:
        inputStr = input('Enter your input: ')

        f = open('stream-data-upbit.txt', 'w')

        while 1:
            await websocket.send(inputStr)

            data = json.loads(await websocket.recv())
            editedData = 'btckrw@orderbook, ' + str(data['orderbook_units'])

            f.write(str(editedData) + "\n")

        f.close();

asyncio.get_event_loop().run_until_complete(stepB())


# stepC
async def stepC_A(callback):
    async with websockets.connect("wss://stream.binance.com/stream?streams=btcusdt@depth5@100ms/btcusdt@trade") as websocket:
        while 1:
            data = json.loads(await websocket.recv())

            if data['stream'] == 'btcusdt@trade':
                editedData = 'btcusdt@trade, ' + str({k:v for k,v in data['data'].items() if k in ['p', 'q']})
            else:
                editedData = 'btcusdt@depth5@100ms, ' + str(data['data']) 

            await callback(editedData)


async def stepC_B(callback):
     async with websockets.connect("wss://api.upbit.com/websocket/v1") as websocket:
        while 1:
            await websocket.send('[{"ticket":"UNIQUE_TICKET"},{"type":"orderbook","codes":["KRW-BTC"]}]')

            data = json.loads(await websocket.recv())
            editedData = 'btckrw@orderbook, ' + str(data['orderbook_units'])

            await callback(editedData)


f = open('stream-data-multi.txt', 'w')

async def response_message(*args, **kwargs):
    f.write(str(args) + "\n")

if __name__ == '__main__':
    tasks = [
        asyncio.ensure_future(stepC_A(response_message)),
        asyncio.ensure_future(stepC_B(response_message))
    ]

    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))




