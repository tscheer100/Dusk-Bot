#! /usr/bin/env python3
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import errors
import random

# uncomment if running in VSCode and change to the appropriate directory.
# os.chdir('./Dusk')
load_dotenv('./.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents(members = True, messages = True, guilds = True)

client = commands.Bot(intents = intents, command_prefix = ".", status=discord.Status.online, activity=discord.Game(".help"), help_command = None)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print("Dusk bot is running.")

client.run(DISCORD_TOKEN)
