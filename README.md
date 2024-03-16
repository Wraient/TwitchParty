# TwitchParty

Youtube Video : https://www.youtube.com/watch?v=aO0ZvWdiuq4

This scipt uses FFMPEG which is a open source tool to stream videos to your Twitch Channel.

### The script currently only works in linux environment.

# Pre-Requisits

- FFMPEG
  
  Install FFMPEG : https://ffmpeg.org/download.html
- pytz

  `pip3 install pytz`

- twitchio

  `pip3 install twitchio`
- yt-dlp

  Install yt-dlp : https://github.com/yt-dlp/yt-dlp/releases

# Edits required in the script

 1. Enter your Twitch Stream on [line 10](https://github.com/Wraient/TwitchParty/blob/main/main.py#L10)
  
 2. Enter your Twitch application token on [line 11](https://github.com/Wraient/TwitchParty/blob/main/main.py#L11)

 3. Enter your Twitch username on [line 12](https://github.com/Wraient/TwitchParty/blob/main/main.py#L12)

 4. If you want to add more channels in the whitelist append channels to list on [line 174 ](https://github.com/Wraient/TwitchParty/blob/main/main.py#L174)
  
