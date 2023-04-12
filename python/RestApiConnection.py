import requests
from requests.structures import CaseInsensitiveDict

API_BASE_URL = "https://iosoccer.com:44380/api/"
HEADERS = {
    "Content-Type": "application/json",
}


def get_tournaments():
    tournaments_url = f"{API_BASE_URL}tournaments/"
    response = requests.get(tournaments_url, headers=HEADERS)
    if response.status_code == 200:
        tournaments = response.json()
        active_tournaments = [t for t in tournaments if not t['hasEnded']]
        for t in active_tournaments:
            print(t['id'], "|", t['name'])
    else:
        response.raise_for_status()


def get_match(tournament_id):
    match_url = f"{API_BASE_URL}match"
    data = {
        "page": 1,
        "pageSize": 8,
        "filters": {
            "timePeriod": 0,
            "includeUpcoming": True,
            "includePast": False,
            "includeUnpublished": False,
            "includePlaceholders": True,
            "tournamentId": tournament_id,
        },
        "sortBy": "KickOff",
        "sortOrder": "ASC"
    }
    response = requests.post(match_url, headers=HEADERS, json=data)
    response.raise_for_status()
    parsed_match = response.json()
    return parsed_match


def connect_to_rest_api(tournament_id):
    url_tournament = f"{API_BASE_URL}tournaments/{tournament_id}/current-phase"
    parsed_api_match = get_match(tournament_id)
    return tournament_id, url_tournament, parsed_api_match



def headers():
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    return headers
