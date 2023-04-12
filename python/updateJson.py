import json
import os


def update_json(fixtures, h2h, standings, results, team1, team2):
    delete_unused_json_files()
    with open("C:\\Streamer kit\\IOS_VTF.json", "r", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
    data["name"] = f"{team1}-{team2}"

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


def delete_unused_json_files():
    directory = r"C:\Streamer kit"
    for filename in os.listdir(directory):
        if filename.endswith(".json") and not filename.startswith("IOS_VTF"):
            os.remove(os.path.join(directory, filename))
