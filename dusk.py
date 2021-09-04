#! /usr/bin/env python3
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure
# from discord.ext.commands import errors

# uncomment if running in VSCode and change to the appropriate directory.
# os.chdir('./Dusk')
load_dotenv('./.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')

intents = discord.Intents(members = True, messages = True, guilds = True)

client = commands.Bot(
    intents = intents, 
    command_prefix = ".", 
    status=discord.Status.online, 
    activity=discord.Game(".help"), 
    help_command = None,
    owner_id = int(OWNER_ID)
    )

client.load_extension('cogs.economy') # This has to be loaded in first because other cogs rely on this one.

for filename in reversed(os.listdir('./cogs')):
   
    if filename.endswith('.py') and not filename == 'economy.py':
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print("Dusk bot is running.")

@client.command()
async def status(ctx):
    print("I am alive!")
    await ctx.send("I am alive!")

@client.command() 
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Bot shutting down")
    await ctx.bot.logout()
@shutdown.error
async def shutdown_error(ctx, err):
    if isinstance(err, CheckFailure):
        await ctx.send("You are not an owner")
        print(ctx.author.name + " tried to shut down the bot")
    else:
        raise

client.run(DISCORD_TOKEN)
