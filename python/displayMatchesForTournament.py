def show_matches_for_tournament(match_json):
    number_of_matches = 0
    for i in range(len(match_json["items"])):
        match = match_json["items"][i]
        if match['teamAway'] and match['teamHome'] and match['kickOff']:
            number_of_matches += 1
            team_home = match["teamHome"]["name"]
            team_away = match["teamAway"]["name"]
            day = match['kickOff'][8:10]  # Day of the match
            month = match['kickOff'][5:7]  # Month of the match
            hour = str(int(match['kickOff'][11:13]) + 1)  # Change the hour to GMT +1
            minutes = match['kickOff'][14:-4]  # to see if it starts at :00 or :30.
            print(
                '{} | {} - {} | Date: {}.{} | Time: {}:{} (GMT+1)'
                .format(i, team_home, team_away, day, month, hour, minutes)
            )
    return number_of_matches