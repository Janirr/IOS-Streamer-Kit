import json
import os


def update_json(fixtures, h2h, standings, results, team1, team2, root_path):
    delete_unused_json_files(root_path)

    file_path = root_path + "/IOS_VTF.json"

    with open(file_path, "r", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)

    data["name"] = f"{team1}-{team2}"

    for source in data["sources"]:
        if source["name"] == "Fixtures":
            source["settings"]["url"] = fixtures
        elif source["name"] == "H2H":
            source["settings"]["url"] = h2h
        elif source["name"] == "Standings URL":
            source["settings"]["url"] = standings
        elif source["name"] == "Results URL":
            source["settings"]["url"] = results

    with open(file_path, "w", encoding="utf-8") as jsonFileWrite:
        json.dump(data, jsonFileWrite, indent=4, ensure_ascii=False)


def delete_unused_json_files(root_path):
    for filename in os.listdir(root_path):
        if filename.endswith(".json") and not filename.startswith("IOS_VTF"):
            os.remove(os.path.join(root_path, filename))
