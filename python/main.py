import json
import os
import requests
from imageFunctions import download_logos
from RestApiConnection import connect_to_rest_api, headers
from teamNames import asign_team_names
from displayMatchesForTournament import show_matches_for_tournament
from createLineup import make_lineups

current_path = os.path.abspath('')

if os.path.abspath('') != 'C:\\Streamer kit\\python':
    print('Your Streamer kit isn\'t located in C:\\Streamer kit, please change it!')

tournament_id, url_tournament, parsed_api_match = connect_to_rest_api()
resp_tournament = requests.get(url_tournament, headers=headers())

if resp_tournament.status_code == 200:
    json_array_current_tournament = resp_tournament.text
    parsed_current_tournament = json.loads(json_array_current_tournament)
    week = parsed_current_tournament["name"]
else:
    week = ''

txt_path = os.path.join(current_path, 'text-files')

with open(os.path.join(txt_path, 'TeamHome.txt'), 'w') as home_team_name, \
        open(os.path.join(txt_path, 'TeamAway.txt'), 'w') as away_team_name, \
        open(os.path.join(txt_path, 'tournamentName.txt'), 'w') as tournament_name, \
        open(os.path.join(txt_path, 'bigtournamentName.txt'), 'w') as big_tournament_name, \
        open(os.path.join(txt_path, 'Head_to_Head_link.txt'), 'w') as h2h_link, \
        open(os.path.join(txt_path, 'matchweek.txt'), 'w') as match_week, \
        open(os.path.join(txt_path, 'fixtures.txt'), 'w') as fixtures, \
        open(os.path.join(txt_path, 'standings.txt'), 'w') as standings:
    if show_matches_for_tournament(parsed_api_match) > 0:
        choice = int(input('Type the number of the match: '))
        make_lineups()
        match = parsed_api_match['items'][choice]
        download_logos(match)
        team1, team2 = asign_team_names(match)
        tournament = match['tournament']['name'].split()
        name_of_tournament = f'{tournament[1]} {tournament[2]}'
        tournament_name.write(name_of_tournament)
        big_tournament_name.write(f'{tournament[1]}\n{tournament[2]}')
        home_team_name.write(team1)
        away_team_name.write(team2)
        match_week.write(week)
        h2h_link.write(
            f'https://www.iosoccer.com/team-head-to-head/{match["teamHome"]["teamCode"]}/{match["teamAway"]["teamCode"]}')
        fixtures.write(f'https://www.iosoccer.com/tournament/{tournament_id}/fixtures')
        standings.write(f'https://www.iosoccer.com/tournament/{tournament_id}/standings')
    else:
        input('\nThere are no games to get the data from, press Enter to quit.')
