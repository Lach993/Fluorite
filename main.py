from flask import Flask, request
import sqlite3
import json
import aiohttp
import asyncio
import requests

app = Flask(__name__)

con = sqlite3.connect('main.db')
cur = con.cursor()
cur.execute('''DROP TABLE users''')
cur.execute('''CREATE TABLE users
               (uuid text, prefix text, suffix text, tab text, above text)''')
cur.execute('''DROP TABLE names''')
cur.execute('''CREATE TABLE names
               (uuid text, name text)''')
con.commit()
Nick = {
    "prefix": "NICKED",
    "suffix": "Bad",
    "tab": "NICKED",
    "above": "Lol, imagine not being Nicked"
   }

@app.route("/api/get", methods=["GET"])
def group():
    names = request.args.get('names', type=str).split(",")
    uuids = get_uuids_from_names(names)
    players = get_players_from_uuids(uuids)
    print(names, uuids, players)
    ret = {}
    for name, uuid in uuids.items():
        ret[name] = players[uuid]
    return ret

def get_uuids_from_names(names: list) -> dict:
    unkown = []
    known = {}
    con = sqlite3.connect('main.db')
    cur = con.cursor()
    for name in names:
        cur.execute("select uuid from names where name == ?", (name,))
        uuid = cur.fetchone()
        if not uuid:
            unkown.append(name)
        else:
            known[name] = uuid[0]
    if len(unkown) > 0:
        ret = asyncio.run(fetch_all_names(unkown))
        for j in ret:
            name = j[0]
            uuid = j[1]["id"]
            print(uuid)
            known[name] = uuid
            cur.execute("INSERT INTO names (name, uuid) VALUES (?, ?) ", (name, uuid))
        con.commit()

    return known

def get_players_from_uuids(uuids: list):
    unkown = []
    known = {}
    con = sqlite3.connect('main.db')
    cur = con.cursor()
    for uuid in uuids.values():
        cur.execute("Select prefix, suffix, above, tab from users where uuid == ?", (uuid,))
        user = cur.fetchone()
        if not user:
            unkown.append(uuid)
        else:
            print(user)
            known[uuid] = {
                "prefix": user[0], 
                "suffix": user[1], 
                "above": user[2], 
                "tab": user[3]}
            print(f"fetched {uuid} from db")
    if len(unkown) > 0:
        ret = asyncio.run(fetch_all_players(unkown))
        for j in ret:
            print(unkown)
            fin = parse_player_data(j[1], j[0])
            
            known[j[0]] = fin
            print(fin)
            cur.execute("INSERT INTO users (uuid, prefix, suffix, above, tab) VALUES (?, ?, ?, ?, ?) ", 
                         (j[0], fin["prefix"], fin["suffix"], fin["above"], fin["tab"]))
        con.commit()

    return known

def parse_player_data(user:str, uuid):
    global Nick
    if user['success'] == False:
        return json.dumps(Nick)
    if user['player'] == None: 
        return json.dumps(Nick)
    stats = user['player']['stats']
    bedwars = stats['Bedwars'] if 'Bedwars' in stats else dict()
    star = user['player']['achievements']['bedwars_level'] if 'bedwars_level' in user['player']['achievements'] else 0
    finalDeaths = bedwars["final_deaths_bedwars"] if  'final_deaths_bedwars' in bedwars else 0
    finalKills = bedwars["final_kills_bedwars"] if 'final_kills_bedwars' in bedwars else 0
    version = user['player']['mcVersionRp'] if 'mcVersionRp' in user['player'] else "Unknown"

    if finalKills == 0: fkdr = "0%"
    elif finalDeaths == 0: fkdr = "inf%"
    else: fkdr = f"{round(finalKills/finalDeaths*100, 2)}%"
    
    if uuid.strip() in ["f1c3965e278f457c8e05c41852eb8314", "443baadc5349495aa735a7d31c684042"]: #_LACH, jh1236
        prefix = "Fluorite"
    elif uuid.strip() in ["568f0a95813e4767b75bc601b693bb39"]: # Dolorrev
        prefix = "Fireball King"
    else:
        prefix = "Pleb"

    return {
        "prefix": prefix,
        "suffix": "<3",
        "tab": "FKDR {} - {}☆ - {}".format(fkdr, str(star), version),
        "above": "Bedwars Star {}".format(str(star))
        }

async def fetch(session, url, relation = None):
    async with session.get(url) as response:
        resp = await response.json()
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
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

async def fetch_all_players(uuids):
    key = "03ad10e3-ce0a-4490-9f38-c5d7546ac246"
    
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
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=80
    )
