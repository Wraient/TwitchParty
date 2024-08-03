# TwitchParty

Youtube Video : https://www.youtube.com/watch?v=aO0ZvWdiuq4 (older version)

This script uses FFMPEG which is a open source tool to stream videos to your Twitch Channel.

This script supports searching for any anime, and playing any anime episode you would want. In future, searching for shows feature would be added.

The searching and retriving of anime urls is done using code sections of [ani-cli](https://github.com/pystardust/ani-cli) program

# Installation

### Linux

<details><summary>Debian</summary>
  
```
git clone https://github.com/wraient/twitchparty --depth=1
cd ./twitchparty
sudo apt update && sudo apt upgrade
pip3 install pytz
pip3 install twitchio
pip3 install yt-dlp
sudo apt-get install ffmpeg
```

</details>

<details><summary>Arch Linux</summary>
  
```
git clone https://github.com/wraient/twitchparty --depth=1
cd ./twitchparty
python -m venv venv
source ./venv/bin/activate
pip3 install pytz
pip3 install twitchio
sudo pacman -Sy yt-dlp
sudo pacman -Sy ffmpeg
```
</details>

After installing you need to edit the script according to your needs, refer to [Edits required in the script](https://github.com/Wraient/TwitchParty/#edits-required-in-the-script)

After editing, you can run the script with 

```
python3 main.py
```

### The script currently only works in linux environment.

# Pre-Requisits

- FFMPEG
  
  Install FFMPEG : https://ffmpeg.org/download.html
- pytz

  ```
  pip3 install pytz
  ```

- twitchio

  ```
  pip3 install twitchio
  ```
  
- yt-dlp

  Install yt-dlp : https://github.com/yt-dlp/yt-dlp/releases

# Usage

Once the bot is connected to you twitch channel a "Bot Landed!" Message would be sent by the bot in the chat.
From there you can 

Watch an anime: 
  1. Search for an anime with `!search [anime name]`
  2. Select the anime from the results with `#[index number]`
  3. Start Any episode you want with `@[episode number]`
  - Stop episode to play later with `!end`
  - Mark episode as completed with `!cp`
  - Quit the bot without any saving in database `!quit`
  - Add nickname to currently playing anime `!nickname [nickname]`

Watch youtube Video:
  - Just send `!yt [youtube link]`

Resume an anime
  - `!continue [anime name / saved nickname ]`

Miscellaneous:
  - Ping the bot `!ping`
  - Show watched db `!db`
  - Ask for help `!help`

# Edits required in the script

 1. Enter your **Twitch username** on [line 15](https://github.com/Wraient/TwitchParty/blob/main/main.py#L15)


 2. **Stream Key**

     [Stream Key can be obtained here](https://dashboard.twitch.tv/u/YOUR_USERNAME/settings/stream)
    
     Enter your Twitch Stream Key on [line 16](https://github.com/Wraient/TwitchParty/blob/main/main.py#L16)

 3. **OAuthToken**

    [OAuthToken can be obtained here](https://twitchtokengenerator.com/)

    Enter your Twitch application token on [line 17](https://github.com/Wraient/TwitchParty/blob/main/main.py#L17)


 4. (Optional) If you want to add more channels in the **whitelist** list add it on [line 21](https://github.com/Wraient/TwitchParty/blob/main/main.py#L21)
