
from modules.CONSTANTS import Nick
from modules.apiCalls import fetch_all_players
from modules.parse_player_data import parse_player_data 
import modules.sqlmanager as sqlmanager

bedwars = sqlmanager.bedwars()

async def get_players_from_uuids(uuids: list):
    unknown = []
    known = {}
    for uuid in uuids.values():
        uuid = uuid
        if uuid == "None":
            known[uuid] = Nick
            continue
        if await bedwars.check(uuid):
            user = await bedwars.fetchlatest(uuid)
            known[uuid] = { "prefix": user[0], "suffix": user[1],
                            "tab"   : user[2], "above" : user[3]}
        else:
            unknown.append(uuid)
    if unknown:
        ret = await fetch_all_players(unknown)
        for j in ret:
            data = parse_player_data(j[1], j[0])
            known[j[0]] = data
            await bedwars.insert(
                uuid = j[0], prefix = data["prefix"], 
                suffix=data["suffix"], tab=data["tab"], 
                above=data["above"])
    return known
