import discord
from discord.ext import commands
from discord.ext.commands import errors
import json
import random

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy Cog loaded.")

    # Commands
    @commands.command()
    async def balance(self, ctx):
        await self.open_account(ctx.author)
        self.user = ctx.author
        users = await self.get_bank_data()
        wallet_amt = users[str(self.user.id)]["wallet"]
        bank_amt = users[str(self.user.id)]["bank"]

        embed = discord.Embed(
            title = f"{ctx.author.name}'s balance",
            color = discord.Color.purple()
        )
        embed.add_field(name = "Wallet balance", value = wallet_amt)
        embed.add_field(name = "Bank balance", value = bank_amt)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author.name}")
        await ctx.send(embed = embed)

    async def open_account(self, user):
        users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0

        with open("bank.json", "w") as f:
            json.dump(users, f)
        return True

    # load data 
    async def get_bank_data(self):
        with open("bank.json", "r") as f:
            users = json.load(f)
        return users

    @commands.command()
    async def beg(self, ctx):
        await self.open_account(ctx.author)
        self.user = ctx.author
        users = await self.get_bank_data()
        earnings = random.randrange(100)

        await ctx.send(f"Someone gave you {earnings} coins!")

        users[str(self.user.id)]["wallet"] += earnings

        with open("bank.json", "w") as f:
            json.dump(users, f)

def setup(client):
    client.add_cog(Economy(client))