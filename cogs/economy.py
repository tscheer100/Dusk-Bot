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
    @commands.command(aliases = ["bal"])
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

    @commands.command()
    async def withdraw(self, ctx, amount = None):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)        
        if amount > bal[1]:
            await ctx.send("Insufficient amount")
            return
        if amount<0:
            await ctx.send("amount must be positive!")
            return
        
        await self.update_bank(ctx.author, amount)
        await self.update_bank(ctx.author, -1*amount, "bank")

        await ctx.send(f"You withdrew {amount} coins!")

    @commands.command(aliases = ["dep"])
    async def deposit(self, ctx, amount = None):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)        
        if amount > bal[0]:
            await ctx.send("Insufficient amount")
            return
        if amount<0:
            await ctx.send("amount must be positive!")
            return
        
        await self.update_bank(ctx.author, -1*amount)
        await self.update_bank(ctx.author, amount, "bank")

        await ctx.send(f"You deposited {amount} coins!")

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

    async def update_bank(self, user,change = 0, mode = "wallet"):
        users = await self.get_bank_data()
        users[str(user.id)][mode] += change

        with open("bank.json", "w") as f:
            json.dump(users, f)
        bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
        return bal

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

        return self.user

def setup(client):
    client.add_cog(Economy(client))