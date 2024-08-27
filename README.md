Here is my package to stream upcomming AIF tournaments!

If it's your first time:
1) Make sure you extracted `Streamer kit.rar` in `C:\Streamer kit`, otherwise you will need to set everything in OBS manually.
2) Install Fonts from `install\fonts`
3) Install Snaz from `install\SnazSetup` at `C:\Snaz`. (Should be the default anyway) and after intalling change Snaz like in `install\snaz.png`

How to setup overlay for the match:
1) `python main.py` in `C:\Streamer kit`
2) Enter tournament id (at the moment is 83).
3) Select your match and exit the console after you have selected your game.
4) Open OBS Studio and Click on Scene Collection (top menu), then click import
5) Import `[team1]-[team2].json` file (it was generated from python file) from `C:\Streamer kit`
6) Click on Scene Collection again and click the match you want to stream.
and that's all you need to do.
