# TwitchParty

Youtube Video : https://www.youtube.com/watch?v=aO0ZvWdiuq4 (older version)

This script uses FFMPEG which is a open source tool to stream videos to your Twitch Channel.

This script supports searching for any anime, and playing any anime episode you would want. In future, searching for shows feature would be added.

The searching and retriving of anime urls is done using code sections of [ani-cli](https://github.com/pystardust/ani-cli) program

# Installation

### Linux
```
git clone https://github.com/wraient/twitchparty
cd ./twitchparty
python3 main.py
```

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

 1. Enter your **Twitch username** on [line 15](https://github.com/Wraient/TwitchParty/blob/main/main.py#L15)


 2. **Stream Key**

     stream key can be obtained [here](https://dashboard.twitch.tv/u/YOUR_USERNAME/settings/stream)
    
     Enter your Twitch Stream Key on [line 16](https://github.com/Wraient/TwitchParty/blob/main/main.py#L16)

 3. **OAuthToken**

    OAuthToken can be obtained [here](https://twitchtokengenerator.com/)

    Enter your Twitch application token on [line 17](https://github.com/Wraient/TwitchParty/blob/main/main.py#L17)


 4. (Optional) If you want to add more channels in the **whitelist** list add it on [line 21](https://github.com/Wraient/TwitchParty/blob/main/main.py#L21)
