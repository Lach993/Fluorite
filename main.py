from quart import Quart, request, send_file
import asyncio
import io
from modules.get_uuids_from_names import get_uuids_from_names, get_uuid_from_name
from modules.get_players_from_uuids import get_players_from_uuids
from modules.countlines import countlines
import lightbulb
import os
# import sys
import modules.sqlmanager as sqlmanager
# import io
# stdout = io.StringIO()
# sys.stdout = stdout
loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)

print(countlines("."))

bot = lightbulb.Bot(
    token=os.environ.get("Discord"),
    insensitive_commands=True,
    prefix="F."
    )

# set up sql manager
loop.run_until_complete(sqlmanager.init())

sqlcapes = sqlmanager.cape()
sqlcosmetics = sqlmanager.cosmetics()
sqlstone = sqlmanager.stone()

app = Quart(__name__)

@app.route("/api/bedwars/get", methods=["GET"])
async def bedwars_get():
    names = request.args.get('names', type=str).split(",")
    uuids = await get_uuids_from_names(names)
    players = await get_players_from_uuids(uuids)
#     print(names, uuids, players)
    ret = {}
    for name, uuid in uuids.items():
        ret[name] = players[uuid]
    return ret


@app.route("/api/capes/get", methods=["GET"])
async def cape_get():
    name = request.args.get('name', type=str)
    uuid = await get_uuid_from_name(name)
    
#     print(uuid)
    uuid = uuid[0]
#     print(uuid)
    if await sqlcapes.check(uuid):
        cape = await sqlcapes.fetchlatest(uuid)
    else:
        return None
    return await send_file(
        io.BytesIO(cape[0]),
            mimetype='image/png',
            as_attachment=False,
            attachment_filename='cape.png')

@app.route("/api/cosmetics/get", methods=["GET"])
async def cosmetics_get():
    names = request.args.get('names', type=str).split(",")
    uuids = await get_uuids_from_names(names)
    ret = {}
    for name, uuid in uuids.items():
        if await sqlcosmetics.check(uuid):
            wings, tophat = await sqlcosmetics.fetchlatest(uuid)
            ret[name] = {"wings": wings, "tophat": tophat}
        else:
            ret[name] = {"wings": 0, "tophat": 0}
    return ret

@app.route("/api/cosmetics/put", methods=["GET", "PUT"])
async def cosmetics_put():
    name = request.args.get('name', type=str)
    tophat = request.args.get('tophat', type=int, default=0)
    wings = request.args.get('wings', type=int, default=0)
    uuid = await get_uuid_from_name(name)
    await sqlcosmetics.insert(uuid=uuid, tophat=int(tophat), wings=int(wings))
    return ""

@app.route("/api/stone/put", methods=["PUT", "GET"])
async def stone_put():
    name = request.args.get("name", type=str)
    num = request.args.get("num", type=int, default=0)
    uuid = await get_uuid_from_name(name)
    await sqlstone.insert(uuid=uuid, num=num)
    return ""

@app.route("/api/stone/get", methods=["GET"])
async def stone_get():
    name = request.args.get("name", type=str)
    uuid = await get_uuid_from_name(name)
    return str(await sqlstone.countall(uuid=uuid))

@bot.command(name="fetchlines")
async def fetchlines(ctx):
    return await ctx.respond(countlines("."))
#     stdout.seek(0)
#     await ctx.respond(attachment=stdout.read())

if __name__ == '__main__':
    loop.create_task(bot.start())
    app.run(
        host='0.0.0.0',
        loop=loop,
#         debug=True,
        port=80
    )
