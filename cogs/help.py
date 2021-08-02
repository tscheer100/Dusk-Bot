import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("help ready")

    # Command
    @commands.command()
    async def help(self, ctx, htype = None):

        # hdict = {
        #     'general': self.gen_embed,
        #     'economy': econ_embed,
        #     'valheim': valheim_embed
        # }

        if htype == None:
            await ctx.send(embed = self.htype_embed(ctx))
        elif htype == 'general':
            await ctx.send(embed = self.gen_embed(ctx))
        elif htype == 'economy':
            await ctx.send(embed = self.econ_embed(ctx))
        elif htype == 'valheim':
            await ctx.send(embed = self.valheim_embed(ctx))
        else:
            await ctx.send("Unknown help command. Type `.help`")

    def htype_embed(self, ctx):
        embed = discord.Embed(
            title = "Help Commands",
            color = discord.Color.purple()
        )
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
        embed.add_field(name = '.help', value = "Brings this up.", inline = False)
        embed.add_field(name = '.help general', value = "Get general commands.", inline = False)
        embed.add_field(name = '.help economy', value = "Get economy commands/", inline = False)
        embed.add_field(name = '.help valheim', value = "Get valheim commands.", inline = False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
        return embed

    def gen_embed(self, ctx):
        embed = discord.Embed(
            title = "General Commands",
            color = discord.Color.purple()            
        )
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
        embed.add_field(name = '.eight <question>', value = "Summon the all powerful 8-ball!", inline = False)
        embed.add_field(name = '.coin', value = "Flip a coin.", inline = False)
        embed.add_field(name = '.dice <sides>', value = "Roll a virtually infinite sided dice.", inline = False)
        embed.add_field(name = '.whois @member', value = "Learn the details of a member.`", inline = False)
        embed.add_field(name = 'Support the Dev for more free bots :grin:', value = "https://www.paypal.com/paypalme/TheTurtleKing", inline = False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
        return embed
    
    def econ_embed(self, ctx):
        embed = discord.Embed(
            title = "Economy Commands",
            color = discord.Color.purple()
        )
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
        embed.add_field(name = '.balance', value = "Check how rich you are.", inline = False)
        embed.add_field(name = '.deposit', value = "Deposit money from your wallet to your bank.", inline = False)
        embed.add_field(name = '.withdraw', value = "withdraw money from your bank to your wallet.", inline = False)
        embed.add_field(name = '.beg', value = "Go to the streets and hope people are kind.", inline = False)
        embed.add_field(name = '.gift @user <amount>', value = "Give coins to another member", inline = False)
        embed.add_field(name = '.slots <amount>', value = "Try your luck with slots.", inline = False)
        embed.add_field(name = '.rob', value = "rob another player. \n(must have at least 1/4 of their wallet in your wallet)", inline = False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
        return embed

    def valheim_embed(self, ctx):
        embed = discord.Embed(
            title = "Valheim Commands",
            color = discord.Color.purple()
        )
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
        embed.add_field(name = '.valheim', value = "Get info to join our Valheim server", inline = False)
        embed.add_field(name = '.modvalheim', value = "Get the download and IP address to joinr our Modded Valheim server", inline = False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"reqquested by {ctx.author.name}")
        return embed

def setup(client):
    client.add_cog(Help(client))

