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
    embed = discord.Embed(
        title = "Help menu",
        color = discord.Colour.purple()
    )
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
    embed.add_field(name = 'Dusk Help', value = "Type `.help` to bring up this menu, but you already knew that.", inline = False)
    embed.add_field(name = 'Magic 8-Ball', value = "Type `.eight <question>` to summon the all powerful 8-ball!", inline = False)
    embed.add_field(name = "Coin Flip", value = "Flip a coin with `.flip`", inline = False)
    embed.add_field(name = 'Dice', value = "roll a virtually infinite sided dice. `.dice <number of sides>`")
    embed.add_field(name = 'WhoIs', value = "Learn the details of a member with `.whois @user`", inline = False)
    embed.add_field(name = 'Github', value = "Check out the bot's code and more. `.github`", inline = False)
    embed.add_field(name = 'Support the Dev for more free bots :grin:', value = "https://www.paypal.com/paypalme/TheTurtleKing", inline = False)
    await ctx.send(embed = embed)

@client.command(aliases = ['git', 'code'])
async def github(ctx):
    embed = discord.Embed(
        title = "Check out the developer's code!",
        color = discord.Colour.purple(),
    )
    embed.set_thumbnail(url = "https://www.sferalabs.cc/wp-content/uploads/github-logo-white.png")
    embed.add_field(name = "Dusk Bot code", value = "https://github.com/tscheer100/Dusk-Bot", inline = False)
    embed.add_field(name = "Developers Github", value = "https://github.com/tscheer100")
    embed.add_field(name = "Support more free bots by paying for the developer's coffee :woozy_face::coffee:", value = "https://www.paypal.com/paypalme/TheTurtleKing", inline = False)
    await ctx.send(embed = embed)

@client.command(aliases = ['who', 'whodat'])
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(
        title = member.name, 
        color = discord.Colour.purple() 
    )
    embed.add_field(name = 'Nickname', value = member.nick, inline = False)
    embed.add_field(name = 'ID', value = member.id)
    embed.add_field(name = 'Joined at', value = member.joined_at)
    embed.add_field(name = 'Needs to verify', value = member.pending)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author.name}")
    await ctx.send(embed = embed)
@whois.error
async def whois_error(ctx, err):
    if isinstance(err, errors.MissingRequiredArgument):
        embed = discord.Embed(
            color = discord.Colour.dark_purple(),
            title = "Missing argument. Did you forget to mention a user? \n Try `.whois @user`"
        )
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
async def eight_error(ctx, err):
    if isinstance(err, errors.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Missing arguments, did you forget your question? \n Try `.eight <question>`",
            color = discord.Colour.dark_purple()
        )
        await ctx.send(embed = embed)


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
            title = "Invalid syntax. \n Try  `.roll <number of sides>`",
            color = discord.Colour.dark_purple()
        )
        await ctx.send(embed = embed)
    if isinstance(err, errors.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Missing arguments. Did you forget a number? \n Try  `.roll <number of sides>`",
            color = discord.Colour.dark_purple()
        )
        await ctx.send(embed = embed)

client.run(DISCORD_TOKEN)
