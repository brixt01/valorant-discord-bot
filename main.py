'''
Title: Valorant Discord Bot
Author: Ben Brixton
'''

import discord
import requests
from secret import token

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

'''
Events
'''

# Bot successfully started
@client.event
async def on_ready():
    print(f"Successfully logged in as \"{client.user}\"")

# Message recieved
@client.event
async def on_message(msg):

    if msg.author == client.user: return        # Do not response to self (infinite loop)
    if not msg.content.startswith("val "): return       # Check message is a "val" command

    # Run function depending on command
    if msg.content.startswith("val help"):
        await help_command(msg)
    elif msg.content.startswith("val stats"):
        await stats_command(msg)
    else:
        await unknown_command(msg)

'''
Commands
'''

# Stats command
async def stats_command(msg):

    # Check they have entered argument
    if len(msg.content.split()) < 3:
        await msg.channel.send("Incorrect use of command")
        return

    user = msg.content.split()[2]       # Get user argument

    # Check user argument is in format <username>#<tagline>
    if len(user.split("#")) < 2:
        await msg.channel.send("Ensure you have entered both a username and tagline in the format <username>#<tagline>")
        return
    
    # Get username and tagline
    username = user.split('#')[0]
    tagline = user.split('#')[1]

    request = requests.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/eu/{username}/{tagline}")        # API call
    
    # Check API call successful
    if request.status_code != 200:
        response = (
            f"Unable to fetch stats for {user}\n"
            "Ensure that the username and tagline are correct."
        )
        await msg.channel.send(response)
        return

    # Collect relevant stats
    stats = request.json()["data"]
    rank = stats["currenttierpatched"]
    rank_image_url = stats["images"]["small"]
    ranking_in_tier = stats["ranking_in_tier"]
    elo = stats["elo"]

    # Format response
    response = (
        f"**Stats for {user}**\n\n"

        f"Rank: {rank}\n"
        f"Progress: {ranking_in_tier}/100\n"
        f"Elo: {elo}\n"
    )

    # Add rank image embed
    embed = discord.Embed()
    embed.set_image(url=rank_image_url)

    # Send response
    await msg.channel.send(response, embed=embed)

# Help command
async def help_command(msg):

    # val help stats
    if msg.content.startswith("val help stats"):
        reponse = "val stats: Displays a user's stats"

    # val help link
    elif msg.content.startswith("val help link"):
        reponse = "val link: Link a valorant account to your discord account"
    
    # val help credits
    elif msg.content.startswith("val help credits"):
        reponse = "val credits: Credits for what made this bot possible"
    
    # val help
    else:
        reponse = (
            "**Help**\n\n"

            "`val help`: This right here!\n"
            "`val stats`: Displays a user's stats\n"
            "`val link`: Link a valorant account to your discord account\n"
            "`val credits`: Credits for what made this bot possible\n\n"

            "For more help with individual commands, use `val help <command>`"
        )
    
    await msg.channel.send(reponse)

# Unknown command
async def unknown_command(msg):
    await msg.channel.send("Unknown command. Use \"val help\" for a list of commands") 

'''
Run bot
'''

client.run(token)