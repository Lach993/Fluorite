import modules.sqlmanager as sqlmanager
from modules.apiCalls import fetch_all_names

sqlusers = sqlmanager.users()

async def get_uuids_from_names(names: list) -> dict:
    unknown = []
    known = {}
    for name in names:
        if await sqlusers.check(name=name):
            uuid = await sqlusers.fetchlatest(name=name)
            known[name] = uuid[0]
            continue
        unknown.append(name)
        
    if unknown:
        ret = await fetch_all_names(unknown)
        for name, r in ret:
            uuid = r["id"]
            await sqlusers.insert(uuid=uuid, name=name)
            known[name] = uuid
    return known


async def get_uuid_from_name(name:str) -> dict:
    if await sqlusers.check(name=name):
        return (await sqlusers.fetchlatest(name=name))
        
    _, r = (await fetch_all_names([name]))[0]
    uuid = r["id"]
    
    await sqlusers.insert(uuid=uuid, name=name)
    return uuid[0]
    