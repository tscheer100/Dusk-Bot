import discord
from discord import user
from discord.ext import commands
from discord.ext.commands import errors
import json
import random
import asyncio

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    # load data 
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

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy Cog loaded.")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = message.channel

        if message.author.id == 302050872383242240 and message.embeds:          
            if '<@' in message.embeds[0].description and "done" in message.embeds[0].description:
                desc = message.embeds[0].description
                start = desc.find('<@')
                end = desc.find('>')
                bumper_id = desc[start+2:end]
                bumper = self.client.get_user(int(bumper_id))
                await self.update_bank(bumper, 500, "wallet")
                await ctx.send(f"Thanks, {bumper.mention} for bumping the server! \nYou've earned `500` coins!")

    # Commands
    @commands.command(aliases = ["bal", "wallet", "money"])
    async def balance(self, ctx, member: discord.Member = None):
        if not member:
            await self.open_account(ctx.author)
            self.user = ctx.author
        else:
            await self.open_account(member)
            self.user = member

        users = await self.get_bank_data()
        wallet_amt = users[str(self.user.id)]["wallet"]
        bank_amt = users[str(self.user.id)]["bank"]

        embed = discord.Embed(
            title = f"{self.user.display_name}'s balance",
            color = discord.Color.purple()
        )
        embed.add_field(name = "Wallet balance", value = wallet_amt)
        embed.add_field(name = "Bank balance", value = bank_amt)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author.name}")
        await ctx.send(embed = embed)
    @balance.error
    async def balance_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument):
            return

    @commands.command()
    async def withdraw(self, ctx, amount = None):
        await self.open_account(ctx.author)
        self.user = ctx.author
        users = await self.get_bank_data()

        if amount == None:
            await ctx.send("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)
        bank_amt = users[str(self.user.id)]["bank"]
 
        if amount == "all":
            amount = bank_amt
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
        self.user = ctx.author
        users = await self.get_bank_data()

        wallet_amt = users[str(self.user.id)]["wallet"]
        if amount == None:
            await ctx.send("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)
        if amount == "all":
            amount = wallet_amt
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

    @commands.command(aliases = ["send","give"])
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

        await ctx.send(f"You sent {amount} coins to {member.display_name}!")
    @gift.error
    async def gift_error(self, ctx, err):
        if isinstance(err, errors.MemberNotFound):
            await ctx.send("Member not found. Try `.gift @member <amount>`")

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

        # dusk emojis

        # among_rand = "<a:among_rand:855159685538512937>"
        # choices = ["<:among_yellow:855213922180005969>",
        # "<:among_white:855213922062958593>",
        # "<:among_red:855160363090706464>",
        # "<:among_purple:855160523939381278>",
        # "<:among_cyan:855213921899773984>",
        # "<:among_blue:855160063495897130>"]
 
        # test server emojis
        among_rand = "<a:among_rand:848648377922224229>"
        choices = ["<:among_blue:848646255252471868>",
        "<:among_purple:848646255264399370>",
        "<:among_red:848646255248146523>",
        # "<:among_yellow:855192733555621938>",
        # "<:among_cyan:855194895333720115>", removed to make chances more fair
        # "<:among_white:855196037647171595>"
        ]
        
        first = ""
        done = ""
        duplicate_check = set()
        
        # setting up final and results
        for i in range(3):
            final.append(random.choice(choices))

        for k in range(len(final)):
            done += final[k]
            done += " "
        
        for elem in final: 
            if elem in duplicate_check:
                return True
            else:
                duplicate_check.add(elem)

        initial_embed = discord.Embed(
            title = "The slots begin to whirl furiously...",
            color = discord.Color.dark_purple()
        )
        initial = among_rand + " " + among_rand + " " + among_rand
        initial_embed.add_field(name = initial, value = "you wait anxiously...")
        msg = await ctx.send(embed = initial_embed)
        
        await asyncio.sleep(1)

        first_embed = discord.Embed(
            title = "The slots begin to whirl furiously...",
            color = discord.Color.dark_purple()
        )
        first += final[0] + " " + among_rand + " " + among_rand
        first_embed.add_field(name = first, value = "you wait anxiously...")
        await msg.edit(embed = first_embed)

        await asyncio.sleep(1)

        second_embed = discord.Embed(
            title = "The slots begin to whirl furiously...",
            color = discord.Color.dark_purple()
        )
        second = final[0] + " " + final[1] + " " + among_rand
        second_embed.add_field(name = second, value = "you wait anxiously...")
        await msg.edit(embed = second_embed)

        await asyncio.sleep(1)

        results_embed = discord.Embed(
            title = "The slots finally stop spinning...",
            color = discord.Color.dark_purple()
        )

        len_diff = len(final) - len(duplicate_check)

        # results, send after slot finishes
        if len_diff == 2:
            await self.update_bank(ctx.author, 4*amount)
            results_embed.add_field(name = done, value = f"OH BABY A TRIPLE! You've won {4*amount} coins! :Fire16:")
        elif len_diff == 1:
            await self.update_bank(ctx.author, amount)
            results_embed.add_field(name = done, value = f"Congratulations! You've won {2*amount} coins! :Fire16:")
        else:
            await self.update_bank(ctx.author, -1*amount)
            results_embed.add_field(name= done, value = f" Oh no! You've lost {amount} coins.")
        await msg.edit(embed = results_embed)



    @commands.command(aliases = ["steal", "mug"])
    async def rob(self, ctx, member: discord.Member):
        await self.open_account(ctx.author)
        await self.open_account(member)

        bal = await self.update_bank(member)
        thief_bal = await self.update_bank(ctx.author)
        earnings = random.randrange(1, int(bal[0]/4))
        success = random.randrange(0,2)

        if thief_bal[0] >= (bal[0]/4):
            if bal[0] < 100:
                await ctx.send(f"It's not worth it, {member.display_name} only has {bal[0]} coins")
                return
            else:
                if success == 1: 
                    await ctx.send(f"You stole {earnings} from {member.display_name}'s' wallet!")
                    await self.update_bank(ctx.author, earnings)
                    await self.update_bank(member, -1*earnings)
                else:
                    await ctx.send(f"Oops! you got caught! You had to pay {member.display_name} {earnings} coins.")
                    await self.update_bank(ctx.author, -1*earnings)
                    await self.update_bank(member, earnings)
        else:
            await ctx.send("""If you get caught, you might not have enough to pay the fee.\nDon't rob from people unless you have at least a fourth of their wallet balance.""")
    @rob.error
    async def rob_error(self, ctx, err):
        if isinstance(err, errors.MemberNotFound):
            await ctx.send("invalid syntax. type `.rob @user`")  
            
def setup(client):
    client.add_cog(Economy(client))