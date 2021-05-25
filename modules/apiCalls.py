import aiohttp
import asyncio
import os

async def fetch(session, url, relation = None):
    try:
        async with session.get(url) as response:
            resp = await response.json()
    except:
        resp = None
    return [relation, resp]

async def fetch_all_names(names):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for name in names:
            tasks.append(
                fetch(
                    session,
                    f"https://api.mojang.com/users/profiles/minecraft/{name}",
                    name

                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=False)
        for j in responses:
            if j[1] == None:
                j[1] = {"name": j[0], "id": "None"}
        return responses

async def fetch_all_players(uuids):
    key = os.environ.get("Hypixel")
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for uuid in uuids:
            tasks.append(
                fetch(
                    session,
                    f"https://api.hypixel.net/player?key={key}&uuid={uuid}",
                    uuid
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=False)
        return responses