import json
import requests
import shutil
from requests.structures import CaseInsensitiveDict
import sys
import os
from PIL import Image
import webbrowser


def get_resized_img(img_path, video_size):
    img = Image.open(img_path)
    width, height = video_size  # these are the MAX dimensions
    video_ratio = width / height
    img_ratio = img.size[0] / img.size[1]
    if video_ratio >= 1:  # the video is wide
        if img_ratio <= video_ratio:  # image is not wide enough
            width_new = int(height * img_ratio)
            size_new = width_new, height
        else:  # image is wider than video
            height_new = int(width / img_ratio)
            size_new = width, height_new
    else:  # the video is tall
        if img_ratio >= video_ratio:  # image is not tall enough
            height_new = int(width / img_ratio)
            size_new = width, height_new
        else:  # image is taller than video
            width_new = int(height * img_ratio)
            size_new = width_new, height
    return img.resize(size_new, resample=Image.LANCZOS)


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist
    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)
    r = requests.get(url, stream=True)
    if r.ok:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


def override_where():
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    return os.path.abspath("cacert.pem")


if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where
    import requests.utils
    import requests.adapters

    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()

# Check if streamer kit is located in the right directory
path_py = os.path.abspath("")
path_general = path_py[:-7]
if path_py != "C:\Streamer kit\python":
    print("Your Streamer kit isn't located in C:\Streamer kit, please change it!")

# Headers settings for JSON
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

# List of all tournaments on API
api_tournaments = "https://iosoccer.com:44380/api/tournaments/"
resp_tournaments = requests.get(api_tournaments, headers=headers)

# If success
if resp_tournaments.status_code == 200:
    # Full list of tournaments
    parsed_tournaments = json.loads(resp_tournaments.text)
    for tournaments in parsed_tournaments:
        if not tournaments['hasEnded']:
            print(tournaments['id'], "|", tournaments['name'])

# User has to write the id of the tournament that he is interested in
tournament_id = input("Enter the id of the tournament: ")
# url_tournament will include the tournament_id specified by the user
url_tournament = "https://iosoccer.com:44380/api/tournaments/" + tournament_id + "/current-phase"
data_match = """
{
  "page": '1',
  "pageSize": '8',
  "filters": {
    "timePeriod": '0',
    "includeUpcoming": 'true',
    "includePast": 'false',
    "includeUnpublished": 'false',
    "includePlaceholders": 'true',
    "tournamentId": 'variable',
  },
  "sortBy": "KickOff",
  "sortOrder": "ASC"
}
"""
# Set the tournamentId in data_match to tournament_id specified by the user
data_match = data_match.replace('variable', tournament_id)

api_match = "https://iosoccer.com:44380/api/match"
response = requests.post(api_match, headers=headers, data=data_match)
parsed_api_match = json.loads(response.text)
resp_tournament = requests.get(url_tournament, headers=headers)

# If success
if resp_tournament.status_code == 200:
    json_array_current_tournament = resp_tournament.text
    parsed_current_tournament = json.loads(json_array_current_tournament)
    matchweek_nr = parsed_current_tournament["name"]  # Matchweek [0-10]
    matchweek_nr = matchweek_nr.replace("Round", "Matchweek")  # Change it to Round [0-10]
else:
    matchweek_nr = ""

# Open Files
home_team_name = open(path_py + "/TeamHome.txt", "w")
away_team_name = open(path_py + "/TeamAway.txt", "w")
tournament_name = open(path_py + "/tournamentName.txt", "w")
big_tournament_name = open(path_py + "/bigtournamentName.txt", "w")
h2h_link = open(path_py + "/Head_to_Head_link.txt", "w")
matchweek = open(path_py + "/matchweek.txt", "w")
fixtures = open(path_py + "/fixtures.txt", "w")
standings = open(path_py + "/standings.txt", "w")

NumberOfMatches = 0
for i in range(len(parsed_api_match["items"])):
    match = parsed_api_match["items"][i]
    if match['teamAway'] and match['teamHome'] and match['kickOff']:
        NumberOfMatches += 1
        teamHomeName = match["teamHome"]["name"]
        teamAwayName = match["teamAway"]["name"]
        day = match['kickOff'][8:10]  # Day of the match
        month = match['kickOff'][5:7]  # Month of the match
        hour = str(int(match['kickOff'][11:13]) + 1)  # Change the hour to GMT +1
        minutes = match['kickOff'][14:-4]  # to see if it starts at :00 or :30.
        print(
            '{} | {} - {} | Date: {}.{} | Time: {}:{} (GMT+1)'
            .format(i, teamHomeName, teamAwayName, day, month, hour, minutes)
        )
if NumberOfMatches > 0:
    choice = int(input("Type the number of the match: "))
    match = parsed_api_match["items"][choice]
    # If the HOME team name is too long, display their teamCode.
    if len(match["teamHome"]["name"]) < 17:
        team1_name = match["teamHome"]["name"]
    else:
        team1_name = match["teamHome"]["teamCode"]
    # If the AWAY team name is too long, display their teamCode.
    if len(match["teamAway"]["name"]) < 17:
        team2_name = match["teamAway"]["name"]
    else:
        team2_name = match["teamAway"]["teamCode"]
    # Name of the tournament
    tournament = match["tournament"]["name"]
    # Path to download logos of the teams
    logoHome = match["teamHome"]['badgeImage']['mediumUrl']
    logoAway = match["teamAway"]['badgeImage']['mediumUrl']
    # Path where to put the files
    destination_home = path_general + "/teams/teamHome.png"
    destination_away = path_general + "/teams/teamAway.png"
    # Download them from their url and place them in the C:/Streamer kit/teams
    download(logoHome, "C:/Streamer kit/teams")
    download(logoAway, "C:/Streamer kit/teams")
    # Get name of the files by looking at the destination starting from the right
    HomeLogoName = logoHome.split("/")[-1]
    AwayLogoName = logoAway.split("/")[-1]
    # Full path to the downloaded logos (example: C:/Streamer kit/teams/1656.png)
    src_home = path_general + "/teams/" + HomeLogoName
    src_away = path_general + "/teams/" + AwayLogoName
    # Copy the file with different names: TeamHome.png and TeamAway.png
    shutil.copyfile(src_home, destination_home)
    shutil.copyfile(src_away, destination_away)
    tournament = tournament.split(" ")
    name_of_tournament = tournament[1] + " " + tournament[2]
    # Get the Head-to-Head URL to display it afterwards in OBS
    h2h = "https://www.iosoccer.com/team-head-to-head/" + match["teamHome"]["teamCode"] + "/" + \
          match["teamAway"]["teamCode"]
    # Write team names into TeamHome and TeamAway files
    home_team_name.write(team1_name)
    away_team_name.write(team2_name)
    # Write the name of tournament
    tournament_name.write(name_of_tournament)
    # Split the tournament into 2 words [by "\n"]
    big_tournament_name.write(tournament[1] + "\n")
    big_tournament_name.write(tournament[2])
    matchweek.write(matchweek_nr)
    # Write H2H link
    h2h_link.write(h2h)
    # Write urls for standings and fixtures
    fixtures.write("https://www.iosoccer.com/tournament/" + str(tournament_id) + "/fixtures")
    standings.write(("https://www.iosoccer.com/tournament/" + str(tournament_id) + "/standings"))
    # Resize Image Home into 256x256px
    size = 256, 256
    im = get_resized_img(destination_home, size)
    im.save(path_general + '/teams/' + 'teamHome.png')
    # Resize Image Away into 256x256px
    im2 = get_resized_img(destination_away, size)
    im2.save(path_general + '/teams/' + 'teamAway.png')
    # Open the stream manager to change the title of the stream
    url = 'https://dashboard.twitch.tv/u/iosoccer/stream-manager'
    webbrowser.open(url)
else:
    # If there is nothing to get from the tournament specified by user
    x = input("\nThere are no games to get the data from, press Enter to quit. ")
# Close the files
home_team_name.close()
away_team_name.close()
tournament_name.close()
big_tournament_name.close()
h2h_link.close()
matchweek.close()
fixtures.close()
standings.close()
