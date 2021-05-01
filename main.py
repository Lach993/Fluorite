
from flask import Flask, request
import sqlite3
import json

import requests

app = Flask(__name__)

con = sqlite3.connect('main.db')
cur = con.cursor()
cur.execute('''DROP TABLE users''')
cur.execute('''CREATE TABLE users
               (uuid text, data text)''')

cur.execute('''DROP TABLE names''')
cur.execute('''CREATE TABLE names
               (uuid text, name text)''')
con.commit()
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

@app.route("/", methods=["GET"])
def home():
    return {"hello": "world"}

@app.route("/api/get", methods=["GET"])
def prase():
    con = sqlite3.connect('main.db')
    cur = con.cursor()
    global data
    global Nick
    
    name = request.args.get("name")
    
    if name:
        cur.execute("select uuid from names where name == ?", (name,))
        uuid = cur.fetchone()
        if not uuid:
            uuid = get_uuid(name)
            cur.execute("INSERT INTO names (name, uuid) VALUES (?, ?) ", (name, uuid))
            con.commit()
            print(f"wrote {name} to names db")
        else:
            uuid = uuid[0]
    else:
        uuid = None
    if uuid == None:
        return json.dumps(Nick)

    cur.execute("Select data from users where uuid == ?", (uuid,))
    user = cur.fetchone()
    if not user:
        user = get_player(uuid)
    else:
        return user[0]

    user = json.loads(user)
    if user['player'] == None:
        return json.dumps(Nick)
    stats = user['player']['stats']
    bedwars = stats['Bedwars'] if 'Bedwars' in stats else dict()
    star = user['player']['achievements']['bedwars_level'] if 'bedwars_level' in user['player']['achievements'] else 0
    wins = bedwars["wins_bedwars"] if 'wins_bedwars' in bedwars else 0
    losses = bedwars["losses_bedwars"] if 'losses_bedwars' in bedwars else 0
    finalDeaths = bedwars["final_deaths_bedwars"] if  'final_deaths_bedwars' in bedwars else 0
    finalKills = bedwars["final_kills_bedwars"] if 'final_kills_bedwars' in bedwars else 0
    version = user['player']['mcVersionRp'] if 'mcVersionRp' in user['player'] else "Unknown"

    if finalKills == 0:
        fkdr = "0%"
    elif finalDeaths == 0:
        fkdr = "inf%"
    else:
        fkdr = f"{round(finalKills/finalDeaths, 4)*100}%"

    # wlr = 0
    print(name, name.strip().lower(), name.strip().lower() in ["_lach", "jh1236"])
    if name.strip().lower() in ["_lach", "jh1236"]:
        prefix = "Fluorite"
    elif name.strip().lower() in ["Dolorrev"]:
        prefix = "Fireball King"
    else:
        prefix = "Pleb"
    data = {
        "real": True,
        "finalKills": finalKills,
        "finalDeaths": finalDeaths,
        "wins": wins,
        "losses": losses,
        "level": 0,
        "star": star,
        "fkdr": fkdr,

        "prefix": prefix,
        "suffix": "<3",
        "tab": "FKDR {} - {}☆ - {}".format(fkdr, str(star), version),
        "above": "Bedwars Star {}".format(str(star))
        }
    cur.execute("INSERT INTO users (uuid, data) VALUES (?, ?) ", (uuid, json.dumps(data)))
    con.commit()
    print(f"wrote {name} to db")
    return json.dumps(data)
        
def get_uuid(uuid):
    try:
        return requests.get(f"https://api.mojang.com/users/profiles/minecraft/{uuid}").json()["id"]
    except:
        return None
def get_player(uuid):
    key = "03ad10e3-ce0a-4490-9f38-c5d7546ac246"
    return requests.get(f"https://api.hypixel.net/player?key={key}&uuid={uuid}").text

@app.route("/api/admin/reset", methods=["GET"])
def reset():
    con = sqlite3.connect('main.db')
    cur = con.cursor()
    cur.execute('''DROP TABLE users''')
    cur.execute('''CREATE TABLE users (uuid text, data text)''')

    cur.execute('''DROP TABLE names''')
    cur.execute('''CREATE TABLE names (uuid text, name text)''')
    con.commit()




if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80
    )
