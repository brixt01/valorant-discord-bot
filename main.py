'''
Title: Valorant Discord Bot
Author: Ben Brixton
'''

import discord
from secret import token

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Successfully logged in as \"{client.user}\"")

@client.event
async def on_message(msg):
    if msg.author == client.user: return
    if not msg.content.startswith("val "): return

    args = msg.content.split(" ")[1:]
    cmd = args[0].lower() if args else ""

    if cmd == "help":
        await help_command(msg)
    else:
        await unknown_command(msg)

async def help_command(msg):
    await msg.channel.send("Commands:\n1. Command\n2. Command\n3. Command")

async def unknown_command(msg):
    await msg.channel.send("Unknown command. Use \"val help\" for a list of commands") 

client.run(token)