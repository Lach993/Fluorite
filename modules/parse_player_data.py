
import json
from modules.CONSTANTS import Nick


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
    version = user['player']['mcVersionRp'] if 'mcVersionRp' in user['player'] else "?"
    if version != "?":
        version  = ".".join(version.split(".")[:2])
    if finalKills == 0: fkdr = "0%"
    elif finalDeaths == 0: fkdr = "inf%"
    else: fkdr = f"{round(finalKills/finalDeaths*100, 2)}%"
    
    if uuid.strip() in ["f1c3965e278f457c8e05c41852eb8314", "443baadc5349495aa735a7d31c684042"]: #_LACH, jh1236
        prefix = "Fluorite"
    elif uuid.strip() in ["568f0a95813e4767b75bc601b693bb39"]: # Dolorrev
        prefix = "Fireball King"
    else:
        prefix = "Pleb"
    if int(star) > 99:
        star =   star ##impliment colours later
    return {
        "prefix": prefix,
        "suffix": "<3",
        "tab": "{} - {}â˜† - {}".format(fkdr, str(star), version),
        "above": "BW Star {}".format(str(star))
        }
