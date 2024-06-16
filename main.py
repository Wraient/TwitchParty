import subprocess
import random
import time
import os
import datetime
import pytz
from twitchio.ext import commands
import json
import re
import sqlite3
import sys
import traceback
from database_handler import AnimeDatabase

username = "" # Your Twitch Username add more usernames in the whitelist list
streamkey = "" # https://dashboard.twitch.tv/u/YOUR_USERNAME/settings/stream 
oAuthToken = "" # https://twitchtokengenerator.com/
script_path=False
user_timezone = "Asia/Kolkata"
preset="superfast"
whitelist = [username, ]

# script_path = "/home/wraient/Documents/Projects/watchParty"

anime_dict={}

def search(msg):
    global anime_dict
    anime_dict2={}
    anime = ""
    for i in range(len(msg)-1):
        anime+=msg[i+1]+" "

    print("searching for",anime)
    
    with open("./scripts/tmp/query", "w") as query:
        query.write(anime)
        print("query wrote")

    os.system("./scripts/anime_list.sh")

    with open('./scripts/tmp/anime_list', 'r') as file:
        input_data = file.read()

    # Parse the input into a dictionary
    spliter="NEWLINEFROMHERE "
    try:
        for line in input_data.split(spliter):
            parts = line.split(' ', 1)
            if line==input_data.split(spliter)[-1]:
                parts[1]= parts[1][:-len(spliter)]
            if len(parts) >= 2:
                anime_id, anime_name = parts[0], parts[1]
                anime_dict2[len(anime_dict2) + 1] = (anime_id, anime_name)
        anime_dict = anime_dict2
        print("anime_dict:",anime_dict)
    except:
        print("No anime with that name")
        return "noanime"

def episode_list(msg):
    index_selected=int(msg[0][1:])

    anime_dict
    if index_selected in anime_dict:
        anime_id, anime_name = anime_dict[index_selected]
        print(f"The ID of {anime_name} is {anime_id}")
        with open("./scripts/tmp/anime", "w") as anime_file:
            anime_file.write(anime_name)
            print("anime name wrote")
    else:
        return False

    with open("./scripts/tmp/id", "w") as id_file:
        id_file.write(anime_id)

    os.system("./scripts/episode_list.sh")

    return True

def get_link(msg):
    episode_no=msg[0][1:]

    with open("./scripts/tmp/ep_no", "w") as ep_no_file:
        ep_no_file.write(episode_no)

    os.system("./scripts/episode_url.sh")

    with open('./scripts/tmp/links', 'r') as file:
        # Read the contents of the file
        input_data = file.read()

    # Split the input into lines
    lines = input_data.split('\n')

    # Extract the first link
    first_link = None
    for line in lines:
        parts = line.split('>')
        if len(parts) >= 2:
            link_and_text = parts[1].strip()
            link_parts = link_and_text.split()
            first_link = link_parts[0]
            break

    print("first link:", first_link)
    return first_link

def extractor(anime_id=False, episode_no=False, anime_name=False):
    if anime_id:
        with open("./scripts/tmp/id", "r") as _id:
            return _id.read()
    if episode_no:
        with open("./scripts/tmp/ep_no", "r") as ep_no:
            return ep_no.read()
    if anime_name:
        with open("./scripts/tmp/anime", "r") as a_name:
            return a_name.read()

def file_inserter(anime_id=False, episode_no=False, anime_name=False):
    if anime_id:
        with open("./scripts/tmp/id", "w") as _id:
            return _id.write(anime_id)
    if episode_no:
        with open("./scripts/tmp/ep_no", "w") as ep_no:
            return ep_no.write(episode_no)
    if anime_name:
        with open("./scripts/tmp/anime", "w") as a_name:
            return a_name.write(anime_name)

def anime_time():
    with open("--nostat", "r") as result:
        stderr_content = result.read()

    # Find the last occurrence of out_time_ms
    out_time_matches = re.findall(r"out_time_ms=(\d+)", stderr_content)
    if out_time_matches:
        last_out_time = out_time_matches[-1]
        out_time_ms = int(last_out_time)
        out_time_seconds = out_time_ms / 1000000
        return out_time_seconds     
    else:
        return False

def save_anime_timing(initial_time):
    temp69420 = anime_time() + initial_time
    if temp69420>30:
        temp69420-=30
    if temp69420:
        db = AnimeDatabase('anime_database.db')
        db.insert_anime(extractor(anime_id=True), extractor(anime_name=True), int(extractor(episode_no=True)), temp69420+initial_time, nickname=db.get_nickname_by_id(extractor(anime_id=True)))
        db.conn.close()
        return temp69420


def ensure_path_exists(path):
    if os.path.isdir(path):
        # If it's a directory, create it if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Directory created: {path}")
        else:
            print(f"Directory already exists: {path}")
    else:
        # If it's a file path, get the directory part
        directory = os.path.dirname(path)
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory created: {directory}")
        else:
            print(f"Directory already exists: {directory}")

    
class Stream():
    def __init__(self):
        self.streamkey = streamkey # nowraient1
        self.input_file=""
        if script_path:
            self.path = script_path+"refactor.py"
            self.file_path = script_path+"/anime/"
        else:
            self.path = os.getcwd()
            self.file_path = os.getcwd()+"/anime/"
    
    def kill(self):
        print("Killing Stream.")
        os.system("killall --user $USER  --ignore-case  --signal INT  ffmpeg")
        os.system("pkill ffmpeg")
        os.system("kill $(pgrep -f ffmpeg)")
    
    def start_base(self, input_file):
        ffmpeg_cmd = [
            'ffmpeg', '-re', '-hide_banner', '-i', input_file, '-c:v', 'libx264', '-preset', preset,
            '-b:v', '3000k', '-maxrate', '3000k', '-progress', '--nostat', '-bufsize', '6000k', '-pix_fmt', 'yuv420p',
            '-g', '50', '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-ar', '44100',
            '-f', 'flv', f'rtmp://live.twitch.tv/app/{streamkey}'
        ]
        subprocess.Popen(ffmpeg_cmd)
    
    def link_seek_time(self, input_file, seek_to):
        ffmpeg_cmd = [
            'ffmpeg', '-re', '-hide_banner', '-ss', seek_to, '-i', input_file, '-c:v', 'libx264', '-preset', preset,
            '-b:v', '3000k', '-maxrate', '3000k', '-progress', '--nostat', '-bufsize', '6000k', '-pix_fmt', 'yuv420p',
            '-g', '50', '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-ar', '44100',
            '-f', 'flv', f'rtmp://live.twitch.tv/app/{streamkey}'
        ]
        subprocess.Popen(ffmpeg_cmd)

    def yt_dlp_start(self, yt_link):
        yt_source = subprocess.check_output(f"yt-dlp --no-warnings --get-url {yt_link}", shell=True, text=True).split("\n")
        
        ffmpeg_cmd = [
            'ffmpeg', '-re', '-hide_banner', '-i', yt_source[0], '-i', yt_source[1], '-c:v', 'libx264', '-preset', preset,
            '-b:v', '3000k', '-maxrate', '3000k', '-progress', '--nostat', '-bufsize', '6000k', '-pix_fmt', 'yuv420p',
            '-g', '50', '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-ar', '44100',
            '-f', 'flv', f'rtmp://live.twitch.tv/app/{streamkey}'
        ]
        
        subprocess.Popen(ffmpeg_cmd)

        print(yt_source)


stream = Stream()

class Bot(commands.Bot):

    ensure_path_exists("./scripts/tmp/query")

    global anime_dict
    def __init__(self):
        super().__init__(token=oAuthToken, prefix='?', initial_channels=[username])
        # stream.anime_dict={}
        # self.initial_time = 0

    async def event_ready(self):
        await bot.connected_channels[0].send('Bot Landed')
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
    
        try:

            global whitelist
            msg = message.content.split() # ['this', 'is', 'the', 'message']
            print(msg)
            if message.echo or (message.author.name not in whitelist):
                return

            if "!yt" in msg:
                stream.kill()
                stream.yt_dlp_start(msg[1])

            if "!search" in msg:
                if search(msg) == "noanime":
                    await bot.connected_channels[0].send(f"No anime with that name was found!")
                    return
                await bot.connected_channels[0].send(f"select a anime (#): ")
                print(anime_dict)
                for index, (_, anime_name) in anime_dict.items():
                    print(index, anime_name)
                    await bot.connected_channels[0].send(f"{index}. {anime_name}")
            
            if "#" in msg[0]:
                # episode_list(msg)
                if episode_list(msg):
                    await bot.connected_channels[0].send('Which episode do you want to watch: ')
                else:
                    await bot.connected_channels[0].send('Thats not an option.')

            if "@" in msg[0]:
                self.initial_time = 0
                first_link = get_link(msg)
                if first_link:
                    stream.kill()
                    try:
                        if msg[1]: # if there is a time stamp 
                            await bot.connected_channels[0].send(f'Starting {extractor(anime_name=True)} ep {extractor(episode_no=True)} at time {msg[1]}')
                            stream.link_seek_time(first_link, msg[1])
                    except:
                        stream.start_base(first_link)
                        await bot.connected_channels[0].send(f'Starting {extractor(anime_name=True)} ep {extractor(episode_no=True)} from begining.')

                else:
                    await bot.connected_channels[0].send('No links found in the file.')
            
            if "!cp" in msg:
                self.initial_time = 0
                db = AnimeDatabase('anime_database.db')
                db.insert_anime(extractor(anime_id=True), extractor(anime_name=True), int(extractor(episode_no=True))+1, "00:00")
                db.conn.close()
                await bot.connected_channels[0].send(f'Marked {extractor(anime_name=True)} episode {extractor(episode_no=True)} completed.')
                print("@" + str(int(extractor(episode_no=True))+1))
                first_link = get_link([f"@{int(extractor(episode_no=True))+1}"])
                print(first_link)
                if first_link:
                    stream.kill()
                    stream.start_base(first_link)
                else:
                    await bot.connected_channels[0].send('No links found in the file.')

                
                first_link = get_link(["@"+str(results[0][2])])
                print("first_link:", first_link)
                if first_link:
                    stream.kill()
                    stream.link_seek_time(first_link, results[0][3])
                else:
                    await bot.connected_channels[0].send('No links found in the file.')

            if '!end' in msg:

                temp69420 = save_anime_timing(self.initial_time)
                await bot.connected_channels[0].send(f'Saved {extractor(anime_name=True)} ep {extractor(episode_no=True)} time at {temp69420} seconds.')

                self.initial_time = 0

                stream.kill()
                await bot.connected_channels[0].send('Killing the stream.')

            if '!quit' in msg:
                stream.kill()
                await bot.connected_channels[0].send('Goodbye.')
                sys.exit()
            
            if "!help" in msg: # help
                await bot.connected_channels[0].send('BOT: its simple, dummy!')
                await bot.connected_channels[0].send('BOT: !ping - ping the bot')
                await bot.connected_channels[0].send('BOT: !search {anime name} - Initiate search')
                await bot.connected_channels[0].send('BOT: #{index of anime} - Select anime')
                await bot.connected_channels[0].send('BOT: @{episode number} - Play episode number')
                await bot.connected_channels[0].send('BOT: !continue {anime name / nickname} - continue anime from where left off last time')
                await bot.connected_channels[0].send('BOT: !nickname - nickname the current playing anime')
                await bot.connected_channels[0].send('BOT: !db - show all the animes in the database')
                await bot.connected_channels[0].send('BOT: !cp - set anime episode to compeleted, start new episode')
                await bot.connected_channels[0].send('BOT: !yt {youtube link} - start youtube video')
                await bot.connected_channels[0].send('BOT: !end - end Stream (save the anime name and timing in database)')
                await bot.connected_channels[0].send('BOT: !quit - end Stream (Without saving in database and bot exit!)')
                await bot.connected_channels[0].send('BOT: !help - show these messages')

            if '!ping' in msg:
                await bot.connected_channels[0].send("Pong!")

            if "!continue" in msg:
                
                # db.search_anime_by_name()
                db = AnimeDatabase('anime_database.db')
                # partial_name = '1p'  # Partial name search
                results = db.search_anime_by_name(msg[1])
                db.__del__()
                print("results:",results)
                
                file_inserter(anime_id=results[0][0], episode_no=results[0][2], anime_name=results[0][1])
                print("anime_id:", extractor(anime_id=True))
                print("anime_name:", extractor(anime_name=True))
                print("episode_no:", extractor(episode_no=True))
                anime_time_in_file = results[0][3]
                if anime_time_in_file=="00:00":
                    self.initial_time = 0
                else:
                    self.initial_time = int(round(float(anime_time_in_file)))
                await bot.connected_channels[0].send(f'Starting {results[0][1]} episode {results[0][2]} at time ({anime_time_in_file} seconds)') # starting {anime_name} episode {episode_no}

                first_link = get_link(["@"+str(results[0][2])])
                print("first_link:", first_link)
                if first_link:
                    stream.kill()
                    stream.link_seek_time(first_link, results[0][3])
                else:
                    await bot.connected_channels[0].send('No links found in the file.')

            if "!db" in msg:
                await bot.connected_channels[0].send('Animes in the db are')
                db = AnimeDatabase('anime_database.db')
                db_data = db.fetch_all_anime()
                index_db = 0
                for anime in db_data:
                    index_db+=1
                    await bot.connected_channels[0].send(f'{index_db}. {anime[1]} (ep {anime[2]}) time: {anime[3]} Nickname: {anime[4]}')

                db.__del__()
                    
            if "!nickname" in msg:
                # print(msg)
                db = AnimeDatabase('anime_database.db')
                db.add_nickname_by_id(extractor(anime_id=True), msg[1])
                print("database\n",db.fetch_all_anime())
                db.__del__()
                # file_inserter(ep_no=)

        except Exception as error:
            print("Some error occured:", error)
            traceback.print_exc()

        message_content = message.content
        print(message.author.name, end=": ")
        print(message_content)
        if message_content[:3]!="BOT":
            tz_NY = pytz.timezone(user_timezone)
            datetime_NY = datetime.datetime.now(tz_NY)
            current_time = str(datetime_NY.strftime("%H:%M:%S"))
            date_today = str(datetime.date.today())
            with open("logs.txt", "a") as logs:
                logs.write("["+date_today+" "+current_time+"] "+message.author.name+": "+message_content+"\n")
        else:print("bot message")
        
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        print("hey")
        await ctx.send(f'BOT: Hello {ctx.author.name}!')

bot = Bot()
if __name__ == "__main__":
    bot.run()