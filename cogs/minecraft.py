import discord
from discord.ext import commands
from discord.ext.commands import errors

class Minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Minecraft Cog loaded.")

    #commands
    @commands.command()
    async def minecraft(self, ctx):
        embed = discord.Embed(
            title = "Minecraft Info",
            description = "Our minecraft server runs on the latest version :)"
        )
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
        embed.add_field(name = "Server Name", value = "A crumb of creepers", inline = False)
        embed.add_field(name = "IP address", value = "`mc.demonwolfdev.com`", inline = False)
        
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Minecraft(client))