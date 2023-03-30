def asign_team_names(match_json):
    if len(match_json["teamHome"]["name"]) < 17:
        team1_name = match_json["teamHome"]["name"]
    else:
        team1_name = match_json["teamHome"]["teamCode"]
    # If the AWAY team name is too long, display their teamCode.
    if len(match_json["teamAway"]["name"]) < 17:
        team2_name = match_json["teamAway"]["name"]
    else:
        team2_name = match_json["teamAway"]["teamCode"]
    return team1_name, team2_name