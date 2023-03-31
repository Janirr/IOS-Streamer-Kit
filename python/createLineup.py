def make_lineups():
    with open("C:\\Streamer kit\\playersHome.txt", "r") as home:
        for line in home:
            position, player_name = line.strip().split(":")
            with open(f"text-files/homeTeam/{position}.txt", "w") as pos_file:
                pos_file.write(player_name + "\n")

    with open("C:\\Streamer kit\\playersAway.txt", "r") as away:
        for line in away:
            position, player_name = line.strip().split(":")
            with open(f"text-files/awayTeam/{position}.txt", "w") as pos_file:
                pos_file.write(player_name + "\n")

