def make_lineups():
    with open("playersHome.txt", "r") as home:
        for line in home:
            position, player_name = line.strip().split(":")
            with open(f"text-files/home{position}.txt", "a+") as pos_file:
                pos_file.write(player_name + "\n")

    with open("playersAway.txt", "r") as away:
        for line in away:
            position, player_name = line.strip().split(":")
            with open(f"text-files/away{position}.txt", "a+") as pos_file:
                pos_file.write(player_name + "\n")