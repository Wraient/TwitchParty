import subprocess
import random
import time
import os
import datetime
import pytz
from twitchio.ext import commands
import json

twitch_streamkey = "" # Your Twitch streamkey
twitch_token = "" # Your Twitch token
channel_name = "" # Your Twitch username

class Stream():
    def __init__(self):
        self.streamkey = twitch_streamkey
        self.path = os.getcwd()
        self.file_path = os.getcwd()+"/anime/"
        self.playing = "" # the file that is playing
        self.started = "" # the time at which the stream was started
        self.pre_seek = "0" # amount of time video was seeked before playing
        self.subtitles = False
        self.subtitle_delay = "0"
        self.paused = True
    
    def parameter_update(self, parameter_list:list): #(playing, pre_seek, subtitle_delay)
        if len(parameter_list)==3:
            self.subtitles=True
            if parameter_list[-1]!=True:
                self.subtitle_delay=parameter_list[-1]
            
        if len(parameter_list)>=2:
            self.pre_seek=parameter_list[1]
        self.playing=parameter_list[0]
        self.started=time.time()
            
    
    def time_to_seconds(self, timer): #returns seconds in INT
        time2 = timer.split(":")
        if len(time2)==3:
            x = time.strptime(timer,'%H:%M:%S')
            seconds = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            return seconds
        elif len(time2) ==2:
            x = time.strptime(timer, "%M:%S")
            seconds = datetime.timedelta(minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
            return seconds
        else:
            return int(timer)

    def kill(self):
        print("KILLLINGGGGGGGGGGGGGGG")
        os.system("killall --user $USER  --ignore-case  --signal INT  ffmpeg")
        os.system("pkill ffmpeg")
    
    def start_base(self, input_file):
        self.parameter_update([input_file])
        subprocess.Popen([f"ffmpeg -re -i {input_file} -c:v libx264 -preset ultrafast -b:v 3000k -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -f flv rtmp://live.twitch.tv/app/{self.streamkey}"], shell=True)
        return

    def ass_to_srt(self, input_file):
        subprocess.Popen([f"ffmpeg -i {self.path}/subtitles/{input_file}.ass -map 0 -c:s srt {self.path}/subtitles/{input_file}.srt -y"], shell=True)
    
    def start(self, input_file):
        self.parameter_update([input_file])
        self.start_base(str(self.file_path)+input_file+".*")
    
    def start_flv(self, input_file):
        self.parameter_update([input_file])
        subprocess.Popen([f"ffmpeg -re -i {str(self.file_path)+input_file} -c copy -f flv rtmp://live.twitch.tv/app/{self.streamkey}"], shell=True)

    def start_from(self, input_file:str, seek_to:str):
        self.parameter_update([input_file, seek_to])
        # self.started = time.time() - self.time_to_seconds(self.pre_seek)

        subprocess.Popen([f"ffmpeg -re -ss {seek_to} -i {str(self.file_path)+input_file}.* -c:v libx264 -preset ultrafast -b:v 3000k -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -f flv rtmp://live.twitch.tv/app/{self.streamkey}"], shell=True)

    def encode(self, input_file):
        subprocess.Popen([f"ffmpeg -i {str(self.file_path)+input_file} -c:v libx264 -preset medium -b:v 3000k -maxrate 3000k -bufsize 6000k -vf \"scale=1280:-1,format=yuv420p\" -g 50 -c:a aac -b:a 128k -ac 2 -ar 44100 {str(self.file_path)+input_file}.flv"], shell=True)

    def start_from_youtube(self, yt_link):
        yt_source = subprocess.check_output(f"yt-dlp --get-url {yt_link}", shell=True, text=True).split("\n")
        subprocess.Popen([f"ffmpeg -re -i \"{yt_source[0]}\" -i \"{yt_source[1]}\" -c:v libx264 -preset ultrafast -b:v 3000k -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -f flv rtmp://live.twitch.tv/app/{self.streamkey}"], shell=True)
        print(yt_source)


    def youtube_start_from(self, yt_link, time_to_start):
        yt_source = subprocess.check_output(f"yt-dlp --get-url {yt_link}", shell=True, text=True).split("\n")
        subprocess.Popen([f"ffmpeg -re -ss {time_to_start} -i \"{yt_source[0]}\" -ss {time_to_start} -i \"{yt_source[1]}\"  -c:v libx264 -preset ultrafast -b:v 3000k -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -f flv rtmp://live.twitch.tv/app/{self.streamkey}"], shell=True)
        print(yt_source)


    def start_sub(self, input_file):
        self.parameter_update([input_file, "0", True])
        self.ass_to_srt(input_file)
        subprocess.Popen([f"ffmpeg -re -i {str(self.file_path)+input_file}.mkv -c:v libx264 -preset ultrafast -b:v 3000k -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -vf subtitles={self.path}/subtitles/{input_file}.srt -f flv rtmp://bom01.contribute.live-video.net/app/{self.streamkey}"], shell=True)
    
    def start_sub_delay(self, input_file, seek_sub):
        self.parameter_update([input_file, "0", seek_sub])

        self.ass_to_srt(input_file)

        subprocess.Popen([f"ffmpeg -itsoffset {seek_sub} -i {self.path}/subtitles/{input_file}.srt -c copy {self.path}/subtitles/subtitles_delayed.srt -y"], shell=True)
        subprocess.Popen([f"ffmpeg -re -i {str(self.file_path)+input_file}.mkv -c:v libx264 -preset ultrafast -b:v 3000k -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -vf subtitles={self.path}/subtitles/subtitles_delayed.srt -f flv rtmp://bom01.contribute.live-video.net/app/{self.streamkey}"], shell=True)

    def delay_sub(self, input_file, seek_sub):
        self.parameter_update([input_file, "0", seek_sub])
        self.ass_to_srt(input_file)
        subprocess.Popen([f"ffmpeg -i {self.path}/subtitles/{input_file}.srt -itsoffset {seek_sub} -c copy output.srt"], shell=True)

    def start_from_with_sub(self, input_file, seek_to, sub_delay):
        self.parameter_update([input_file, seek_to, sub_delay])
        
        self.started = time.time() - self.time_to_seconds(self.pre_seek)

        self.ass_to_srt(input_file)

        subprocess.Popen([f"ffmpeg -itsoffset {sub_delay} -i {self.path}/subtitles/{input_file}.srt -c copy {self.path}/subtitles/subtitles_delayed.srt -y"], shell=True)

        subprocess.Popen([f"iconv -f utf-8 -t utf-8 -c {self.path}/subtitles/subtitles_delayed.srt > {self.path}/subtitles/subtitles_delayed.srt"], shell=True) # clean subtitles from non utf-8 characters

        subprocess.Popen([f"srt fixed-timeshift --seconds -{self.time_to_seconds(seek_to)} < {self.path}/subtitles/subtitles_delayed.srt > {self.path}/subtitles/subtitles_fixed.srt -y"], shell=True) # only works when root

        subprocess.Popen([f"ffmpeg -re -ss {seek_to} -i {str(self.file_path)+input_file}.* -c:v libx264 -preset ultrafast -b:v 3000k -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -vf subtitles={self.path}/subtitles/subtitles_fixed.srt -f flv rtmp://bom01.contribute.live-video.net/app/{self.streamkey}"], shell=True)

    def update_json(self):
        today = datetime.date.today()
        formatted_date = today.strftime("%d/%m/%Y")
        time_rn = str(datetime.datetime.now().time())
        seeker = str(round(time.time()-int(self.started)-10))
        if int(seeker) < 0:
            seeker = "0"
        playing =  str(self.playing)
        project_data = {
            "playing":playing,
            "seeker": seeker,
            "subtitles" : self.subtitles,
            "subtitle_delay": self.subtitle_delay,
            "date":formatted_date,
            "time":time_rn
        }

        with open("data.json", "w") as file:
            json.dump(project_data, file)


    def play_from_json(self):
        with open("data.json", "r") as file:
            data = json.load(file)

        self.playing = data["playing"] # the file that is playing
        self.started = str(round(time.time()-int(data["seeker"]))) # the time at which the stream was started
        self.pre_seek = data["seeker"] # amount of time video was seeked before playing
        self.subtitles = data["subtitles"]
        self.subtitle_delay = data["subtitle_delay"]

        if data["subtitles"]:pass
        self.start_from(self.playing, self.pre_seek)


stream = Stream()

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=twitch_token, prefix='?', initial_channels=[channel_name])

    async def event_ready(self):
        await bot.connected_channels[0].send('Bot Landed')
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        whitelist = [channel_name]
        msg = message.content.split()
        # print(msg)
        if message.echo or (message.author.name not in whitelist):
            return

        if "!start" in msg or "!s" in msg: #start file
            await bot.connected_channels[0].send('BOT: Opening File!')
            stream.kill()
            stream.paused = False
            stream.start(msg[1])
            
        elif "!startfrom" in msg or "!sf" in msg: # start from
            await bot.connected_channels[0].send('BOT: Doing just that!')
            stream.paused=False
            stream.kill()
            stream.start_from(msg[1], msg[2])

        if "!sstart" in msg or "!ss" in msg: #sub start with delay
            await bot.connected_channels[0].send('BOT: Opening File with subs!')
            stream.kill()
            stream.paused = False
            if len(msg)==3:
                stream.start_sub_delay(msg[1], msg[2])
            else:
                stream.start_sub(msg[1])
            
        if "!ssf" in msg: #start wtih sub from {time}
            await bot.connected_channels[0].send('BOT: Opening File with subs!')
            stream.kill()
            stream.paused = False
            if len(msg)==3:
                stream.start_from_with_sub(msg[1], msg[2], 0)
            if len(msg)==4:
                stream.start_from_with_sub(msg[1], msg[2], msg[3])
            
        elif "!yt" in msg: # start youtube
            await bot.connected_channels[0].send('BOT: Opening Youtube!')
            stream.kill()
            stream.paused = True
            if len(msg)==2:
                stream.start_from_youtube(msg[1])
            if len(msg)==3:
                stream.youtube_start_from(msg[1], msg[2])

        elif "!pause" in msg or "!p" in msg: #pause
            await bot.connected_channels[0].send('BOT: Pausing!')
            random_youtube = ["GvqTJnKA0Bc", "_dmtLLAQawI", "v_oZ9Pe0yRg", "23_mESawEEc", "7YkzC0a1GXo", "3QzT1sq6kCY", "aewbOlGXv6s", "F4tHL8reNCs", "yg6JN7eH4XE", "flgtJUthKkk", "k85mRPqvMbE", "FtE6SV_1wu4", "flgtJUthKkk"]
            stream.kill()
            stream.paused = True
            stream.start_from_youtube("https://www.youtube.com/watch\?v\="+random_youtube[random.randint(0,len(random_youtube)-1)])

        elif "!play" in msg: # end stream
            await bot.connected_channels[0].send('BOT: Playing!')
            stream.play_from_json()
            stream.paused = False
            stream.kill()

        elif "!end" in msg: # end stream
            await bot.connected_channels[0].send('BOT: Ending!')
            print("ending")
            stream.kill()

        elif "!help" in msg: # help
            await bot.connected_channels[0].send('BOT: (!start or !s) {file name}')
            await bot.connected_channels[0].send('BOT: (!sf or !startfrom) {file name} {time to start from}')
            await bot.connected_channels[0].send('BOT: !ss {file name} {subtitle delay (optional)}')
            await bot.connected_channels[0].send('BOT: !ssf {file name} {time to start from} {subtitle delay (optional)}')
            await bot.connected_channels[0].send('BOT: !yt {youtube link}')
            await bot.connected_channels[0].send('BOT: !pause or !p')
            await bot.connected_channels[0].send('BOT: !end')

        elif "!ping" in msg: # ping
            await bot.connected_channels[0].send("Pong!")

        elif "!ls" in msg: # list files in ./anime
            data_list = os.listdir(stream.file_path)
            for i in data_list:
                await bot.connected_channels[0].send("BOT: "+i)
        
        elif "!quit" in msg: #quit program
            await bot.connected_channels[0].send("BOT: quiting :((")
            stream.kill()
            exit()
        

        message_content = message.content
        print(message.author.name, end=": ")
        print(message_content)
        if message_content[:3]!="BOT":
            tz_NY = pytz.timezone('Asia/Kolkata')
            datetime_NY = datetime.datetime.now(tz_NY)
            current_time = str(datetime_NY.strftime("%H:%M:%S"))
            date_today = str(datetime.date.today())
            with open("logs.txt", "a") as logs:
                logs.write("["+date_today+" "+current_time+"] "+message.author.name+": "+message_content+"\n")
        else:print("bot message")
        
        if not stream.paused:
            stream.update_json()
        await self.handle_commands(message)


    @commands.command()
    async def hello(self, ctx: commands.Context):
        print("hey")
        await ctx.send(f'BOT: Hello {ctx.author.name}!')

bot = Bot()
if __name__ == "__main__":
    bot.run()
