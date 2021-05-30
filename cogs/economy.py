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


    @commands.command(aliases = ["send"])
    async def gift(self, ctx, member: discord.Member, amount = None):
        await self.open_account(ctx.author)
        await self.open_account(member)

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
        
        await self.update_bank(ctx.author, -1*amount, "wallet")
        await self.update_bank(member, amount, "wallet")

        await ctx.send(f"You sent {amount} coins to {member}!")
    @gift.error
    async def gift_error(self, ctx, err):
        if isinstance(err, errors.MemberNotFound):
            await ctx.send("Member not found. Try `.gift @member <amount>`")

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

    @commands.command(aliases = ["slot"])
    async def slots(self, ctx, amount = None):
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
        
        final = []
        choices = ["<:among_blue:848646255252471868>", "<:among_purple:848646255264399370>", "<:among_red:848646255248146523>"]
        done = ""
        for i in range(len(choices)):
            # a = random.choice(["<:among_blue:848646255252471868>", "<:among_purple:848646255264399370>", "<among_red:848646255248146523>"])
            final.append(random.choice(choices))

        for k in range(len(final)):
            done += final[k]
            done += " "
        
        slot_embed = discord.Embed(
            title = "You pull the lever...",
            description = "You wait anxiously as the slots spin furiously...",
            color = discord.Color.purple()
        )
        slot_embed.set_image(url = "https://i.gifer.com/8nNk.gif")
        await ctx.send(embed = slot_embed)

        results_embed = discord.Embed(
            title = "The slots finally stop spinning...",
            color = discord.Color.dark_purple()
        )
        if final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
            await self.update_bank(ctx.author, 2*amount)
            results_embed.add_field(name = done, value = f"Congratulations! You've won {2*amount} coins! :Fire16:")
        else:
            await self.update_bank(ctx.author, -1*amount)
            results_embed.add_field(name= done, value = f" Oh no!You've lost {amount} coins.")
        await ctx.send(embed = results_embed)

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
        wallet_amt = users[str(self.user.id)]["wallet"]
        bank_amt = users[str(self.user.id)]["bank"]
        earnings = random.randrange(100)

        if wallet_amt + bank_amt < 200:
            await ctx.send(f"Someone gave you **{earnings}** coins!")
            users[str(self.user.id)]["wallet"] += earnings
        else:
            await ctx.send("You can only beg if your net worth is below __**200 coins**__")

        with open("bank.json", "w") as f:
            json.dump(users, f)

        return self.user


def setup(client):
    client.add_cog(Economy(client))