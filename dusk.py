#! /usr/bin/env python3
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import errors

import random

os.chdir('./Dusk')
load_dotenv('./.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents(members = True, messages = True, guilds = True)

client = commands.Bot(intents = intents, command_prefix = ".", status=discord.Status.online, activity=discord.Game(".help"), help_command = None)

eight_list = [
    "http://www.redkid.net/generator/8ball/newsign.php?line1=Ask+&line2=Turtle&line3=&Shake+Me=Shake+Me",
    "http://www.redkid.net/generator/8ball/newsign.php?line1=um+sure&line2=I+guess&line3=&Shake+Me=Shake+Me",
    "http://www.redkid.net/generator/8ball/newsign.php?line1=too+dizzy&line2=ask+me&line3=later&Shake+Me=Shake+Me",
    "http://www.redkid.net/generator/8ball/newsign.php?line1=bruh+idk&line2=Google&line3=it&Shake+Me=Shake+Me",
    "http://www.redkid.net/generator/8ball/newsign.php?line1=Ask+yo&line2=Mamma&line3=&Shake+Me=Shake+Me",
    "http://www.redkid.net/generator/8ball/newsign.php?line1=oh%2C+for&line2=sure.&line3=&Shake+Me=Shake+Me",
    "http://www.redkid.net/generator/8ball/newsign.php?line1=lol+cute&line2=but+no&line3=&Shake+Me=Shake+Me",
]

h_or_t = [
    "https://media.tenor.com/images/a3f762237882e2b8dfa32199bbe9a90d/tenor.gif", # heads
    "https://media.tenor.com/images/3f1aa6550335c20338817bd19a3b5806/tenor.gif" # tails
]

@client.event
async def on_ready():
    print("Dusk bot is running.")


@client.command()
async def status(ctx):
    print("I am alive!")
    await ctx.send("I am alive!")

@client.command()
async def help(ctx):
    embed = discord.Embed(title = "Help menu", color = discord.Colour.purple())
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
    embed.add_field(name = 'Dusk Help', value = "Type `.d help` to bring up this menu, but you already knew that.", inline = False)
    embed.add_field(name = 'Magic 8-Ball', value = "Type `.d eight <question>` to summon the all powerful 8-ball!", inline = False)
    embed.add_field(name = "Coin Flip", value = "Flip a coin with `.d flip`")
    await ctx.send(embed = embed)

@client.command()
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name, color = discord.Colour.purple() )
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
    await ctx.send(embed = embed)

@client.command(aliases = ['8ball', '8', '8 ball', 'eight ball', '8-ball', 'eight-ball'])
async def eight(ctx, *, arg):
    embed = discord.Embed(
        title = "The all powerfull 8ball has spoken!",
        color = discord.Colour.purple(),
        description = f"{arg}"
    )
    embed.set_thumbnail(url = "https://media4.giphy.com/media/efahzan109oWdMRKnH/giphy.gif")
    embed.set_image(url = random.choice(eight_list))
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
    await ctx.send(embed = embed)
@eight.error
async def on_command_error(ctx, err):
    if isinstance(err, errors.MissingRequiredArgument):
        await ctx.send("You do not have the right syntax. try `.eight <question>`")


@client.command(aliases = ['coinflip', 'ht', 'hort'])
async def flip(ctx):
    state = random.randint(1,2)
    embed = discord.Embed(
        title = "Flipping coin..",
        color = discord.Colour.purple(),
        description = "Coin flipped heads" if state ==1 else "Coin flipped tails" #embeds don't allow for if statements, so I was taught a trick with tenary operators.
    )
    embed.set_image(url = h_or_t[0] if state == 1 else h_or_t[1])
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
    await ctx.send(embed = embed)

@client.command(aliases = ['dice', 'd'])
async def roll(ctx, *,  sides):
    num = random.randint(1, int(sides))
    embed = discord.Embed(
        title = f"Rolling a {sides} sided die",
        color = discord.Colour.purple(),
    )
    embed.add_field(name = "The Die has landed on", value = f"`{num}`")
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
    await ctx.send(embed = embed)
@roll.error
async def roll_errorr(ctx, err):    
    if isinstance(err, errors.CommandInvokeError): 
        embed = discord.Embed(
            title = "Invalid syntax. \n try  `.roll <number of sides>`"
        )
        await ctx.send(embed = embed)
    if isinstance(err, errors.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Missing arguments. Did you forget a number? \n try  `.roll <number of sides>`"
        )
        await ctx.send(embed = embed)

client.run(DISCORD_TOKEN)
