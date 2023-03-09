import discord
import youtube_dl
import asyncio
import os

#Get Discord Token from the enviroment
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=discord.Intents.all())

#Global variable to keep track of the current voice client
vc = None

@client.event
async def on_ready():
    activity = discord.Activity(name='youtube | !help', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    global vc
    if message.content.startswith('!ping'):
        await message.channel.send('Pong!')
  
  
    if message.content.startswith("!help"):
        help_text = "!play - play music by inserting youtube URL after command \n" \
                    "!stop - disconnect from voice channel \n"\
                    "!pause - pause/stop \n"\
                    "!resume - resume playing after pause \n"\
                    "!help - list of all commands \n"
                          
        embed = discord.Embed(title="list of commands:", description=help_text, color=0x00ff00)
        await message.channel.send(embed=embed)
    

    elif message.content.startswith('!play'):
        # Get the video or audio link
        link = message.content.split(' ')[1]
        # Check if user is in a voice channel
        if message.author.voice is None:
            await message.channel.send("You are not in a voice channel.")
            return
        # If the bot is not already connected to a voice channel, join the voice channel
        if vc is None:
            voice_channel = message.author.voice.channel
            vc = await voice_channel.connect()
        # Play the audio
        if 'youtube' in link or 'youtu.be' in link:
            ydl_opts = {'format': 'bestaudio/best', 'noplaylist': True,'nocheckcertificate': True, 'ignoreerrors': True, 'quiet': True, 'outtmpl': '-'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                url = info['url']
                vc.play(discord.FFmpegPCMAudio(url), after=lambda e: print('done', e))
                while vc.is_playing():
                    await asyncio.sleep(1)
        elif 'soundcloud' in link:
            vc.play(discord.FFmpegOpusAudio(link), after=lambda e: print('done', e))
            while vc.is_playing():
                    await asyncio.sleep(1)
    elif message.content.startswith('!stop'):
        if vc is not None:
            vc.stop()
            await vc.disconnect()
            vc = None
    elif message.content.startswith('!pause'):
        if vc is not None:
            vc.pause()
    elif message.content.startswith('!resume'):
        if vc is not None:
            vc.resume()

client.run(DISCORD_TOKEN)
