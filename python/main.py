import json
import requests
import shutil
from requests.structures import CaseInsensitiveDict
import sys
import os
from PIL import Image


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

url_match = "https://iosoccer.com:44380/api/match"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
url_tournaments = "https://iosoccer.com:44380/api/tournaments/"
resp_tournaments = requests.get(url_tournaments, headers=headers)
if resp_tournaments.status_code == 200:
    json_array_tournaments = resp_tournaments.text
    parsed_tournaments = json.loads(json_array_tournaments)
    for i in range(len(parsed_tournaments)):
        if parsed_tournaments[i]['tournamentSeries']['isActive']:
            print(parsed_tournaments[i]['id'], "|", parsed_tournaments[i]['name'])
path_py = os.path.abspath("")
path_general = path_py[:-7]
if path_py != "C:\Streamer kit\python":
    print("Your Streamer kit isn't located in C:\Streamer kit, please change it!")
tournament_id = int(input("Enter the id of the tournament: "))
url_current_tournament = "https://iosoccer.com:44380/api/tournaments/" + str(tournament_id) + "/current-phase"
data = """
{
  "page": '1',
  "pageSize": '10',
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
data = data.replace('variable', str(tournament_id))
resp = requests.post(url_match, headers=headers, data=data)
json_array = resp.text
parsed = json.loads(json_array)
resp_current_tournament = requests.get(url_current_tournament, headers=headers)

if resp_current_tournament.status_code == 200:
    json_array_current_tournament = resp_current_tournament.text
    parsed_current_tournament = json.loads(json_array_current_tournament)
    matchweek_nr = parsed_current_tournament["name"]
    matchweek_nr = matchweek_nr.replace("Round", "Matchweek")
else:
    matchweek_nr = ""
#Open Files
home_team_name = open(path_py + "/TeamHome.txt", "w")
away_team_name = open(path_py + "/TeamAway.txt", "w")
tournament_name = open(path_py + "/tournamentName.txt", "w")
big_tournament_name = open(path_py + "/bigtournamentName.txt", "w")
h2h_link = open(path_py + "/Head_to_Head_link.txt", "w")
matchweek = open(path_py + "/matchweek.txt", "w")
fixtures = open(path_py + "/fixtures.txt", "w")
standings = open(path_py + "/standings.txt", "w")

n = min(8, len(parsed["items"]))
x = 0
for i in range(n):
    match = parsed["items"][i]
    if match['teamAway'] is not None and match['teamHome'] is not None and match['kickOff'] is not None:
        x += 1
        hour = str(int(match['kickOff'][11:13]) + 1)
        teamHomeName = match["teamHome"]["name"]
        teamAwayName = match["teamAway"]["name"]
        day = match['kickOff'][8:10]
        month = match['kickOff'][5:7]
        minute = match['kickOff'][14:-4]
        print('{} | {} - {} | Date: {}.{} | Time: {}:{} (GMT+1) |'.format(i, teamHomeName, teamAwayName, day, month, hour, minute))
if x > 0:
    choice = int(input("Type the number of the match: "))
    tab = parsed["items"][choice]
    if len(tab["teamHome"]["name"]) < 17:  # If the HOME team name is too long, display their teamcode.
        team1_name = tab["teamHome"]["name"]
    else:
        team1_name = tab["teamHome"]["teamCode"]

    if len(tab["teamAway"]["name"]) < 17:  # If the AWAY team name is too long, display their teamcode.
        team2_name = tab["teamAway"]["name"]
    else:
        team2_name = tab["teamAway"]["teamCode"]

    tournament = tab["tournament"]["name"]

    logoHome = tab["teamHome"]['badgeImage']['mediumUrl']
    logoAway = tab["teamAway"]['badgeImage']['mediumUrl']

    destination_home = path_general + "/teams/teamHome.png"
    destination_away = path_general + "/teams/teamAway.png"

    download(logoHome, "C:/Streamer kit/teams")
    download(logoAway, "C:/Streamer kit/teams")

    HomeLogoName = logoHome.split("/")[-1]
    AwayLogoName = logoAway.split("/")[-1]

    src_home = path_general + "/teams/" + HomeLogoName
    src_away = path_general + "/teams/" + AwayLogoName

    shutil.copyfile(src_home, destination_home)
    shutil.copyfile(src_away, destination_away)

    tournament = tournament.split(" ")
    name_of_tournament = tournament[1] + " " + tournament[2]
    h2h = "https://www.iosoccer.com/team-head-to-head/" + tab["teamHome"]["teamCode"] + "/" + \
          tab["teamAway"]["teamCode"]
    # write everything into txt files
    home_team_name.write(team1_name)
    away_team_name.write(team2_name)
    tournament_name.write(name_of_tournament)
    big_tournament_name.write(tournament[1] + "\n")
    big_tournament_name.write(tournament[2])
    matchweek.write(matchweek_nr)
    h2h_link.write(h2h)
    fixtures.write("https://www.iosoccer.com/tournament/" + str(tournament_id) + "/fixtures")
    standings.write(("https://www.iosoccer.com/tournament/" + str(tournament_id) + "/standings"))
    # Image Home resize
    size = 256, 256
    im = get_resized_img(destination_home, size)
    im.save(path_general + '/teams/' + 'teamHome.png')
    im2 = get_resized_img(destination_away, size)
    im2.save(path_general + '/teams/' + 'teamAway.png')
else:
    x = input("\nThere are no games to get the data from, press Enter to quit. ")
home_team_name.close()
away_team_name.close()
tournament_name.close()
big_tournament_name.close()
h2h_link.close()
matchweek.close()
fixtures.close()
standings.close()
