import json


def update_json(fixtures, h2h, standings, results, team1, team2):
    with open("C:\\Streamer kit\\IOS_VTF.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data["name"] = f"{team1}-{team2}"
    i = 0
    for source in data["sources"]:
        if source["name"] == "Fixtures":
            source["settings"]["url"] = fixtures
        if source["name"] == "H2H":
            source["settings"]["url"] = h2h
        if source["name"] == "Standings URL":
            source["settings"]["url"] = standings
        if source["name"] == "Results URL":
            source["settings"]["url"] = results

    with open(f"C:\\Streamer kit\\{team1}-{team2}.json", "w") as jsonFileWrite:
        json.dump(data, jsonFileWrite)


