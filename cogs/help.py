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
        #     'general': gen_embed,
        #     'economy': econ_embed,
        #     'bank': bank_embed,
        #     'valheim': valheim_embed
        # }

        if htype == None:
            await ctx.send("htype embed goes here")
        elif htype == 'general':
            await ctx.send("general embed goes here")
        elif htype == 'economy':
            await ctx.send("econ embed goes here")
        elif htype == 'bank':
            await ctx.send("bank embed goes here")
        elif htype == 'valheim':
            await ctx.send("valheim embed goes here")
        else:
            await ctx.send("Unknown help command. Type `.help`")

def setup(client):
    client.add_cog(Help(client))

