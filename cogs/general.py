import discord
from discord.ext import commands
from discord.ext.commands import errors
import random

# Data
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

class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("General Cog loaded.")

    # Commands

    @commands.command(aliases = ['git', 'code'])
    async def github(self, ctx):
        embed = discord.Embed(
            title = "Check out the developer's code!",
            color = discord.Colour.purple(),
        )
        embed.set_thumbnail(url = "https://www.sferalabs.cc/wp-content/uploads/github-logo-white.png")
        embed.add_field(name = "Dusk Bot code", value = "https://github.com/tscheer100/Dusk-Bot", inline = False)
        embed.add_field(name = "Developers Github", value = "https://github.com/tscheer100")
        embed.add_field(name = "Support more free bots by paying for the developer's coffee :woozy_face::coffee:", value = "https://www.paypal.com/paypalme/TheTurtleKing", inline = False)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['who', 'whodat'])
    async def whois(self, ctx, member : discord.Member):
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
    async def whois_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument):
            embed = discord.Embed(
                color = discord.Colour.dark_purple(),
                title = "Missing argument. Did you forget to mention a user? \n Try `.whois @user`"
            )
            await ctx.send(embed = embed)

    @commands.command(aliases = ['8ball', '8', '8 ball', 'eight ball', '8-ball', 'eight-ball'])
    async def eight(self,ctx, *, arg):
        embed = discord.Embed(
            title = "The all powerfull 8ball has spoken!",
            color = discord.Colour.purple(),
            description = f"{arg}"
        )
        embed.set_thumbnail(self, url = "https://media4.giphy.com/media/efahzan109oWdMRKnH/giphy.gif")
        embed.set_image(url = random.choice(eight_list))
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
        await ctx.send(embed = embed)
    @eight.error
    async def eight_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument):
            embed = discord.Embed(
                title = "Missing arguments, did you forget your question? \n Try `.eight <question>`",
                color = discord.Colour.dark_purple()
            )
            await ctx.send(embed = embed)


    @commands.command(aliases = ['coinflip', 'ht', 'hort', 'coin'])
    async def flip(self, ctx):
        state = random.randint(1,2)
        embed = discord.Embed(
            title = "Flipping coin..",
            color = discord.Colour.purple(),
            description = "Coin flipped heads" if state ==1 else "Coin flipped tails" #embeds don't allow for if statements, so I was taught a trick with tenary operators.
        )
        embed.set_image(url = h_or_t[0] if state == 1 else h_or_t[1])
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['dice', 'd'])
    async def roll(self, ctx, sides = None):
        if sides == None:
            await ctx.send("number of sides not specified, default will be 6.")
            sides = 6
        if sides <= 1:
            await ctx.send("numbwe of sides needs to at least be 2 and no less.")
            return

        num = random.randint(1, int(sides))
        embed = discord.Embed(
            title = f"Rolling a {sides} sided die",
            color = discord.Colour.purple(),
        )
        embed.add_field(name = "The Die has landed on", value = f"`{num}`")
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
        await ctx.send(embed = embed)
    @roll.error
    async def roll_errorr(self, ctx, err):    
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
        else:
            raise

    

def setup(client):
    client.add_cog(General(client))