import json
import os
import requests
from imageFunctions import download_logos
from RestApiConnection import connect_to_rest_api, headers, get_tournaments
from teamNames import asign_team_names
from displayMatchesForTournament import show_matches_for_tournament
from updateJson import update_json

def replace_in_json_file(json_path, find_str, replace_str):
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_content = content.replace(find_str, replace_str)

    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Replaced all '{find_str}' with '{replace_str}' in {json_path}")

current_path = os.path.abspath('')
path_general = os.path.dirname(current_path)
path_general = path_general.replace('\\', '/')
json_file_path = path_general + "/IOS_VTF.json"
old_root_path = 'C:/Streamer kit'
old_python_path = 'C:\\Streamer kit\\python'

if os.path.abspath('') != old_python_path:
    replace_in_json_file(json_file_path, old_root_path, path_general)

get_tournaments()
id_trnmt = input("Enter the id of the tournament: ")
tournament_id, url_tournament, parsed_api_match = connect_to_rest_api(id_trnmt)
resp_tournament = requests.get(url_tournament, headers=headers())

if resp_tournament.status_code == 200:
    json_array_current_tournament = resp_tournament.text
    week = json.loads(json_array_current_tournament)["name"]
else:
    week = ''

txt_path = os.path.join(current_path, 'text-files')

with open(os.path.join(txt_path, 'TeamHome.txt'), 'w') as home_team_name, \
        open(os.path.join(txt_path, 'TeamAway.txt'), 'w') as away_team_name, \
        open(os.path.join(txt_path, 'tournamentName.txt'), 'w') as tournament_name, \
        open(os.path.join(txt_path, 'bigtournamentName.txt'), 'w') as big_tournament_name, \
        open(os.path.join(txt_path, 'matchweek.txt'), 'w') as match_week:
    if show_matches_for_tournament(parsed_api_match) > 0:
        choice = int(input('Type the number of the match: '))
        match = parsed_api_match['items'][choice]
        download_logos(match)
        team1, team2 = asign_team_names(match)
        tournament = match['tournament']['name'].split()
        name_of_tournament = f'{tournament[0]} {tournament[1]}'
        tournament_name.write(name_of_tournament)
        big_tournament_name.write(f'{tournament[0]}\n{tournament[1]}')
        home_team_name.write(team1)
        away_team_name.write(team2)
        match_week.write(week)
        away_code = match["teamAway"]["teamCode"]
        home_code = match["teamHome"]["teamCode"]
        h2h_link = f'https://www.iosoccer.com/team-head-to-head/{match["teamHome"]["teamCode"]}/{match["teamAway"]["teamCode"]}'
        fixtures = f'https://www.iosoccer.com/tournament/{tournament_id}/fixtures'
        results = f'https://www.iosoccer.com/tournament/{tournament_id}/results'
        standings = f'https://www.iosoccer.com/tournament/{tournament_id}/standings'
        update_json(fixtures, h2h_link, standings, results, team1, team2, path_general)
        input('\nSuccess! Press Enter to quit.')
    else:
        input('\nThere are no games to get the data from, press Enter to quit.')
