import discord
from discord.ext import commands
from discord.ext.commands import errors

class Valheim(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Valheim Cog loaded.")

    #commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def valheim(self, ctx, *, message = None):
        await ctx.send("Check your DMs {} :)".format(ctx.author.mention))

        embed = discord.Embed(
            title = "Vanilla Valheim info",
            description = "This is the information to log into our vanilla Valheim server"
        )
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
        embed.add_field(name = "Server name", value = "Muspelheim")
        embed.add_field(name = "Password", value = "valhalla")
        embed.add_field(name = "IP address", value = "52.149.14.67:4456")
        embed.add_field(name = "Looking for the modded seerver?", value = "Type `.modvalheim` for modded server info")

        await ctx.author.send(embed = embed)
    
    @commands.command()
    async def modvalheim(self, ctx):
        await ctx.send("Check your DMs {} :)".format(ctx.author.mention))
        embed = discord.Embed(
            title = "Valheim Modded Info",
            description = "This server is only accessable if you have the latest patch for the server"
        )

        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
        embed.add_field(name = "Latest patch (v. 1.3 sv2)", value = "file can be found [here](https://niflheim.blob.core.windows.net/installer/NiflheimLauncher.zip)", inline = False)
        embed.add_field(name = "Installation instructions", value = "installation and join instructions can be found [here](https://github.com/Firoso/Valheim-Dusk-Niflheim)", inline = False)
        
        await ctx.author.send(embed = embed)

def setup(client):
    client.add_cog(Valheim(client))