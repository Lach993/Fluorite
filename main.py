from flask import Flask, request
import copy
import json
import requests

app = Flask(__name__)

Nick = {
    "real": False,
    "finalKills": 0,
    "finalDeaths": 0,
    "level": 0,
    "star": 0,
    "fkdr": 0.0,

    "prefix": "NICKED",
    "suffix": "",
    "tab": "NICKED",
    "above": ""
}

@app.route("/api/get", methods=["GET"])
def prase():
    global data
    global Nick
    
    name = request.args.get("name")
    if name:
        uuid = get_uuid(name)
    if uuid == None:
        return json.dumps(Nick)
    user = get_player(uuid)

    bedwars = user['player']['stats']['bedwars'] 
    star = user['player']['achievements']['bedwars_level']
    wins = bedwars["wins_bedwars"]
    losses = bedwars["losses_bedwars"]
    finalDeaths = bedwars["final_deaths_bedwars"]
    finalKills = bedwars["final_kills_bedwars"]
    version = user['player']['mcVersionRp'] 

    if finalKills == 0:
        fkdr = "0%"
    elif finalDeaths == 0:
        fkdr = "inf%"
    else:
        fkdr = f"{round(finalKills/finalDeaths, 4)*100}%"

    # wlr = 0
    if name.lower() in ["_lach", "jh1236"]:
        prefix = "Fluorite"
    if name.lower() in ["Dolorrev"]:
        prefix = "Fireball King"
    else:
        prefix = "Pleb"
    data = {
        "real": True,
        "finalKills": finalKills,
        "finalDeaths": finalDeaths,
        "wins": wins,
        "losses": losses,
        "level": "Yes.",
        "star": star,
        "fkdr": fkdr,

        "prefix": prefix,
        "suffix": "<3",
        "tab": "FKDR {} - {}☆ - {}".format(fkdr, str(star), version),
        "above": "Bedwars Star {}".format(str(star))
        }

    return json.dumps(data)


    # kills = bedwars["kills_bedwars"]
    # bedsBroken = bedwars["beds_broken_bedwars"]
    # bedsLost = bedwars["beds_lost_bedwars"]
    # death = bedwars["deaths_bedwars"]
        
def get_uuid(uuid):
    return requests.get(f"https://api.mojang.com/users/profiles/minecraft/{uuid}")["id"]

def get_player(uuid):
    key = "03ad10e3-ce0a-4490-9f38-c5d7546ac246"
    return(f"https://api.hypixel.net/player?key={key}&uuid={uuid}")



if __name__ == '__main__':
    app.run(debug=True)
