import discord
from discord.ext import commands
import minestat
import time
import requests

tokenfile = open("./secret/token")
token = tokenfile.read()
print(token)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "m?", intents=intents)

@bot.event
async def on_ready():
    print("Started !")

@bot.command()
async def mctracker_help(ctx):
    embedVar = discord.Embed(title="Help", description="This is the help page for <@1209199691779022898>.", color=0x00ff00)
    embedVar.add_field(name="m?quickview", value="You can write `m?quickview <SERVER IP> <PORT>` to inspect any given server (java or bedrock).\nIf you don't know what a port is, use `25565` for Java and `19132` for Bedrock.", inline=False)
    embedVar.add_field(name="Example :", value="Here is an example down below.")
    await ctx.send(embed=embedVar)
    await ctx.send("m?quickview hypixel.net 0")
    server = "hypixel.net"
    port = "0"
    await ctx.send(f"Connecting to server `{server}` with port `{port}`...")
    startTime = time.time()
    ms = minestat.MineStat(server, int(port))
    await ctx.send(f"Connected to `{ms.address}` in `{time.time()-startTime} sec` !")
    if ms.online:
        embedVar = discord.Embed(title=f"Status of `{ms.address}`", description=f"Status of `{ms.address}` on port `{ms.port}`:",color=0x2B2D31)
        embedVar.add_field(name="Software:", value=f"`{ms.version}`", inline=False)
        embedVar.add_field(name="Players:", value=f"`{ms.current_players}`/`{ms.max_players}`", inline=False)
        embedVar.add_field(name="MOTD:",value=f"```{ms.stripped_motd}```",inline=False)
    else:       
        embedVar = discord.Embed(title=f"Couldn't connect to `{server}`.", description="Server offline (or not a Minecarft server)")
    await ctx.send(embed=embedVar)

@bot.command()
async def ping(ctx):
    print("pong")
    await ctx.send("pong")

@bot.command()
async def server_info(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    numberOfMembers = server.member_count
    await ctx.send("`There is in this server:\n"+str(numberOfTextChannels)+" text channel(s)\n"+str(numberOfVoiceChannels)+" voice channels(s)\nfor "+str(numberOfMembers)+" members.`")

@bot.command()
async def say(ctx, *text):
    await ctx.send(" ".join(text))

@bot.command()
async def quickview(ctx, server, port):
    await ctx.send(f"Connecting to server `{server}` with port `{port}`...")
    startTime = time.time()
    ms = minestat.MineStat(server, int(port))
    await ctx.send(f"Connected to `{ms.address}` in `{time.time()-startTime} sec` !")
    if ms.online:
        embedVar = discord.Embed(title=f"Status of `{ms.address}`", description=f"Status of `{ms.address}` on port `{ms.port}`:",color=0x2B2D31)
        embedVar.add_field(name="Software:", value=f"`{ms.version}`", inline=False)
        embedVar.add_field(name="Players:", value=f"`{ms.current_players}`/`{ms.max_players}`", inline=False)
        embedVar.add_field(name="MOTD:",value=f"`{ms.stripped_motd}`",inline=False)
    else:       
        embedVar = discord.Embed(title=f"Couldn't connect to `{server}`.", description="Server offline (or not a Minecarft server)")
    await ctx.send(embed=embedVar)

@bot.command()
async def scanfiles(ctx):
    message = ctx.message
    files = message.attachments
    url = files[0].url
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        debounce = True
        i = 0
        for line in text.splitlines():
            i += 1
            if len(text.splitlines()) > 5 and debounce:
                await ctx.send("You must buy the premium version to queue more than 5 servers !")
                debounce = False
            if i > 5:
                await ctx.send("```ansi\n[2;31mQueue stopped, buy [2;34mpremium[0m[2;31m[0m [2;31mfor unlimited queuing.[0m\n``` (pas vraiment en fait jsp pk jai mis ca)")
                break
            server = line.split()[0]
            port = line.split()[1]
            await ctx.send(f"Connecting to server `{server}` with port `{port}`...")
            startTime = time.time()
            ms = minestat.MineStat(server, int(port))
            await ctx.send(f"Connected to `{ms.address}` in `{time.time()-startTime} sec` !")
            if ms.online:
                embedVar = discord.Embed(title=f"Status of `{ms.address}`", description=f"Status of `{ms.address}` on port `{ms.port}`:",color=0x2B2D31)
                embedVar.add_field(name="Software:", value=f"`{ms.version}`", inline=False)
                embedVar.add_field(name="Players:", value=f"`{ms.current_players}`/`{ms.max_players}`", inline=False)
                embedVar.add_field(name="MOTD:",value=f"`{ms.stripped_motd}`",inline=False)
            else:       
                embedVar = discord.Embed(title=f"Couldn't connect to `{server}`.", description="Server offline (or not a Minecarft server)")
            await ctx.send(embed=embedVar)
    else:
        await ctx.send(f"The request to {url} failed, error code : {response.status_code}")

bot.run(token)