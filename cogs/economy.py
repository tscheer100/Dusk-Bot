from logging import error
import os
import random
import asyncio
import discord
import pymongo
from dotenv import load_dotenv
from discord import member, user
from discord.ext.commands.core import command
from discord.ext import commands
from discord.ext.commands import context, errors
from motor import motor_asyncio
from typing import Union

load_dotenv('./.env')
MONGO_URL = os.getenv('MONGO_URL')

cluster = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = cluster['dusk-bank']
collection = db['bank']

class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("bank ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.open_bank(member)
        
    async def open_bank(self, ctx: Union[commands.Context, discord.Member]):
        if isinstance(ctx, commands.Context):
            self.ID = ctx.author.id
            self.name = ctx.author.name
        elif isinstance(ctx, discord.Member):
            self.ID = ctx.id
            self.name = ctx.name
        result = await collection.find_one({'_id': self.ID})
        if result == None:
            print(result)
            wallet = 0
            bank = 0
            new = {'_id': self.ID, 'name': self.name, 'wallet': wallet, 'bank': bank,
           'has_work': False,}
            await collection.insert_one(new)
            print(new)
        else:
            print("member already has a bank")

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = message.channel

        if message.author.id == 302050872383242240 and message.embeds:
            if '<@' in message.embeds[0].description and "done" in message.embeds[0].description:
                desc = message.embeds[0].description
                start = desc.find('<@')
                end = desc.find('>')
                bumper_id = desc[start+2:end]
                bumper_id = int(bumper_id)
                bumper = self.client.get_user(int(bumper_id))
                self.user = await collection.find_one({'_id': bumper_id})
                self.user_wallet = self.user['wallet']
                await collection.update_one({'_id': bumper_id}, {'$set': {'wallet': self.user_wallet + 500} })
                await ctx.send(f"Thanks, {bumper.mention} for bumping the server! \nYou've earned `500` coins!")

    # Commands
    @commands.command(aliases = ["bal", "wallet", "money"])
    async def balance(self, ctx, member: discord.Member = None):
        req = ctx.author
        if not member:
            await self.open_bank(ctx.author)
            self.user = ctx.author
            self.ID = ctx.author.id
            
        else:
            await self.open_bank(member)
            self.user = member
            self.ID = member.id

        result = await collection.find_one({'_id': self.ID})
        wallet_amt = result['wallet']
        bank_amt = result['bank']

        embed = discord.Embed(
            title = f"{self.user.display_name}'s balance",
            color = discord.Color.purple()
        )
        embed.add_field(name = "Wallet balance", value = wallet_amt)
        embed.add_field(name = "Bank balance", value = bank_amt)
        embed.add_field(name = "Net Worth", value = wallet_amt + bank_amt, inline = False)
        embed.set_footer(icon_url = req.avatar_url, text = f"requested by {req.display_name}")
        await ctx.send(embed = embed)
    @balance.error
    async def balance_error(self, err):
        if isinstance(err, errors.MissingRequiredArgument):
            return
        else:
            raise error

    @commands.command(aliases = ["dep"])
    async def deposit(self, ctx, amount = None):
        await self.open_bank(ctx.author)
        ID = ctx.author.id
        user = await collection.find_one({'_id': ID})

        wallet_amt = user['wallet']
        bank_amt = user['bank']

        if amount == None:
            await ctx.send("Invalid syntax, try `.deposit <amount>`")
            return
        
        if amount == 'all':
            collection.update_one({'_id': self.ID}, {'$set': {'wallet': 0} })
            collection.update_one({'_id': self.ID}, {'$set': {'bank': bank_amt + wallet_amt}})
            await ctx.send("You have deposited all of your entire wallet into your bank.")
            return

        new_wallet = wallet_amt - int(amount)
        new_bank = bank_amt + int(amount)
        if new_wallet >= 0:
            collection.update_one({'_id': self.ID}, {'$set': {'wallet': new_wallet} })
            collection.update_one({'_id': self.ID}, {'$set': {'bank': new_bank} })
            await ctx.send(f"You have deposited **{amount}** coins!")
        else:
            await ctx.send("You don't have enough in your wallet to deposit that much!")

    @commands.command()
    async def withdraw(self, ctx, amount = None):
        await self.open_bank(ctx.author)
        ID = ctx.author.id
        user = await collection.find_one({'_id': ID})

        wallet_amt = user['wallet']
        bank_amt = user['bank']

        if amount == None:
            await ctx.send("Invalid syntax, try `.withdraw <amount>`")
            return
        
        if amount == 'all':
            collection.update_one({'_id': self.ID}, {'$set': {'bank': 0} })
            collection.update_one({'_id': self.ID}, {'$set': {'wallet': bank_amt + wallet_amt}})
            await ctx.send("You have withdrawn your entire bank.")
            return

        new_wallet = wallet_amt + int(amount)
        new_bank = bank_amt - int(amount)

        if new_bank >= 0:
            collection.update_one({'_id': self.ID}, {'$set': {'wallet': new_wallet} })
            collection.update_one({'_id': self.ID}, {'$set': {'bank': new_bank} })
            await ctx.send(f"You have withdrawn **{amount}** coins!")
        else:
            await ctx.send("You don't have enough in your bank to withdraw that much!")

    @commands.command(aliases = ['send','give', 'pay'])
    async def gift(self, ctx, Member: discord.Member, amount = None):
        await self.open_bank(ctx.author)
        await self.open_bank(member)
        ID = ctx.author.id
        MEM_ID = Member.id
        
        if ctx.author.id == Member.id:
            await ctx.send("You can't gift yourself something.")
            return

        user = await collection.find_one({'_id': ID})
        mem = await collection.find_one({'_id': MEM_ID})
        wallet_amt = user['wallet']
        mem_amt = mem['wallet']
        if amount == None:
            await ctx.send("Please enter the amount")
            print("amount is None_type")
            return

        amount = int(amount)

        if amount > user['wallet']: # <-- problem starts here?
            await ctx.send("Insufficient amount in your wallet")
            return
        if amount == 0:
            await ctx.send(f"Sent {Member.display_name} a paperclip and chewed gum. \nYou good?")
            return
        if amount < 0:
            await ctx.send("Amount must be positive!")
            return
        
        await collection.update_one({'_id': ID}, {'$set': {'wallet': wallet_amt + (-1*amount)}})
        await collection.update_one({'_id': MEM_ID}, {'$set': {'wallet': mem_amt + amount}})

        await ctx.send(f"You sent {amount} coins to {Member.display_name}")
    @gift.error
    async def gift_error(self, ctx, err):
        if isinstance(err, errors.MemberNotFound):
            await ctx.send("Member not found. Try `.gift @member <amount>`")
        else:
            raise error

    # This method is wonky.
    @commands.command(aliases = ["slot"])
    async def slots(self, ctx, amount = None):
        await self.open_bank(ctx.author)
        user = await collection.find_one({'_id': ctx.author.id})
        wallet = user['wallet']

        if amount == None:
            await ctx.send("Please enter the amount.")
            return
        else:
            amount = int(amount)
        if amount > wallet:
            await ctx.send("Insufficient funds in your wallet.")
            return
        if amount < 0:
            await ctx.send("Amount can't be negative.")
        final = []

        # dusk emojis

        among_rand = "<a:among_rand:855159685538512937>"
        choices = ["<:among_yellow:855213922180005969>",
        "<:among_white:855213922062958593>",
        "<:among_red:855160363090706464>",
        "<:among_purple:855160523939381278>",
        "<:among_cyan:855213921899773984>",
        "<:among_blue:855160063495897130>"]
 
        # test server emojis
        # among_rand = "<a:among_rand:848648377922224229>"
        # choices = ["<:among_blue:848646255252471868>",
        # "<:among_purple:848646255264399370>",
        # "<:among_red:848646255248146523>",
        # "<:among_yellow:855192733555621938>",
        # "<:among_cyan:855194895333720115>", 
        # "<:among_white:855196037647171595>"]
        
        
        first = ""
        done = ""
        duplicate_check = set()

        # setting up final and results
        for i in range(3):
            final.append(random.choice(choices))
        
        for k in range(len(final)):
            done += final[k]
            done += " "
            duplicate_check.add(final[k])

        initial_embed = discord.Embed(
            title = "The slots begin to whirl furiously...",
            color = discord.Color.dark_purple()
        )
        initial = among_rand + " " + among_rand + " " + among_rand
        initial_embed.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author.display_name}")
        initial_embed.add_field(name = initial, value = "you wait anxiously...")
        msg = await ctx.send(embed = initial_embed)
        await asyncio.sleep(1)

        first_embed = discord.Embed(
            title = "The slots begin to whirl furiously...",
            color = discord.Color.dark_purple()
        )
        first += final[0] + " " + among_rand + " " + among_rand
        first_embed.add_field(name = first, value = "you wait anxiously...")
        first_embed.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author.display_name}")
        await msg.edit(embed = first_embed)

        await asyncio.sleep(1)

        second_embed = discord.Embed(
            title = "The slots begin to whirl furiously...",
            color = discord.Color.dark_purple()
        )
        second = final[0] + " " + final[1] + " " + among_rand
        second_embed.add_field(name = second, value = "you wait anxiously...")
        second_embed.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author.display_name}")
        await msg.edit(embed = second_embed)

        await asyncio.sleep(1)
        results_embed = discord.Embed(
            title = "The slots finally stop spinning...",
            color = discord.Color.dark_purple()
        )
        results_embed.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author.display_name}")
        print(duplicate_check)
        len_diff = len(final) - len(duplicate_check)
        # results, send after slot finishes
        if len_diff == 2:
            await collection.update_one({'_id': ctx.author.id}, {'$set': {'wallet': wallet + (4*amount)} })
            results_embed.add_field(name = done, value = f"OH BABY A TRIPLE! You've won {4*amount} coins! ")
        elif len_diff == 1:
            await collection.update_one({'_id': ctx.author.id}, {'$set': {'wallet': wallet + amount} })
            results_embed.add_field(name = done, value = f"Congratulations! You've won {2*amount} coins! ")
        else:
            await collection.update_one({'_id': ctx.author.id}, {'$set': {'wallet': wallet - amount} })
            results_embed.add_field(name= done, value = f" Oh no! You've lost {amount} coins.")
        await msg.edit(embed = results_embed)
    
    @commands.command(aliases = ["steal", "mug"])
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member):
        await self.open_bank(ctx.author)
        await self.open_bank(member)
        await asyncio.sleep(0.5)
        VICTIM_ID = await collection.find_one({'_id': member.id})
        VICTIM_ID = VICTIM_ID['_id']
        THEIF_ID = await collection.find_one({'_id': ctx.author.id})
        THEIF_ID = THEIF_ID['_id']
        victim_wallet = await collection.find_one({'_id': VICTIM_ID})
        victim_wallet = victim_wallet['wallet']
        thief_wallet = await collection.find_one({'_id': THEIF_ID})
        thief_wallet = thief_wallet['wallet']

        earnings = random.randrange(1, int(victim_wallet/4))
        success = bool(random.getrandbits(1))

        if thief_wallet >= (victim_wallet/4):
            if victim_wallet < 100:
                await ctx.send(f"It's not worth it, {member.display_name} only has {victim_wallet}")
                return
            else:
                if success:
                    await ctx.send(f"You stole **{earnings}** from **{member.display_name}'s** wallet!")
                    await collection.update_one({'_id': THEIF_ID},{'$set': {'wallet': (thief_wallet + earnings)} })
                    await collection.update_one({'_id': VICTIM_ID}, {'$set': {'wallet': (victim_wallet - earnings)} }) 
                else:
                    await ctx.send(f"Oops! you got caught! You had to pay **{member.display_name}** **{earnings}** coins.")
                    await collection.update_one({'_id': THEIF_ID},{'$set': {'wallet': (thief_wallet - earnings)} })
                    await collection.update_one({'_id': VICTIM_ID}, {'$set': {'wallet': (victim_wallet + earnings)} }) 
        else:
            await ctx.send("""If you get caught, you might not have enough to pay the fee.\nDon't rob from people unless you have at least a fourth of their wallet balance.""")
    @rob.error 
    async def rob_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = "**You are on a cooldown!** please wait **{:.2f}s**".format(err.retry_after)   
            await ctx.send(msg)
        elif isinstance(err, errors.MissingRequiredArgument):
            await ctx.send("Who are you trying to rob? Try `.rob @user`")
            self.rob.reset_cooldown(ctx)
        else:
            raise
    
    @commands.command(aliases = ['nick', 'name'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def forcenick(self, ctx, member: discord.Member, nick = None):
        if nick == None:
            await ctx.send("You didn't set a nickname. Try `.forcenick @user <nickname>`")

        await self.open_bank(ctx.author)
        price = 5000
        forcer = await collection.find_one({'_id': ctx.author.id})
        forcer_wallet = forcer['wallet']
        if forcer_wallet < price:
            await ctx.send(f"You don't have enough money to force a nickname! The price is {price}.")
        else:
            await collection.update_one({'_id': ctx.author.id}, {'$set': {'wallet': forcer_wallet - price} })
            await member.edit(nick=nick)
            await ctx.send(f"nickname was changed for {member.mention}")
    @forcenick.error
    async def forcenick_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = "**You are on a cooldown!** please wait **{:.2f}s**".format(err.retry_after) 
            await ctx.send(msg)
        else:
            raise

    @commands.command()
    async def addnet(self, ctx):
        cursor = collection.find().sort('_id')
        docs = await cursor.to_list(None)
        ids = []
        for _ids in ctx.guild.members:
            ids.append(_ids.id)

        for doc in docs:
            if doc['_id'] in  ids:
                mem = await collection.find_one({'_id': doc['_id']})
                print(mem)
                await asyncio.sleep(.1)
                mem = await collection.find_one({'_id': doc['_id']})
                net = int(mem['wallet']) + int(mem['bank'])
                await collection.update_one({'_id': doc['_id']}, {'$set': {'net': net} }, upsert = True)
                print(str(mem))
            else:
                mem = await collection.find_one({'_id': doc['_id']})
                net = int(mem['bank']) + int(mem['wallet'])
                await collection.update_one({'_id': mem['_id']}, {'$set': {'net': net} })
                print(str(mem) + " not in the server" )

    
    @commands.command()
    async def baltop(self, ctx):
        cursor = collection.find().sort('net', pymongo.DESCENDING)
        docs = await cursor.to_list(length = 100)
        ids = []
        checks = []

        for _ids in ctx.guild.members:
            ids.append(_ids.id)
        print(ids)

        for check in docs:
            if check['_id'] in ids:
                checks.append(check['_id'])

        print(checks)

        embed = discord.Embed(
            title = "Members with the highest networth",
            color = discord.Color.purple()
        )

        if len(checks) < 10:
            for doc in range(len(checks)):
                mem = ctx.guild.get_member(checks[doc])
                net = await collection.find_one({'_id': mem.id})

                print(mem.id)
                try:
                    if not mem.id == 845372731872903198:
                        embed.add_field(name = mem, value=net['net'], inline = False)
                except KeyError:
                    print(f"KeyError with {mem} with id {mem.id}")

        else:
            for doc in range(10):
                mem = ctx.guild.get_member(checks[doc])
                net = await collection.find_one({'_id': mem.id})

                print(mem.id)
                try:
                    if not mem.id == 845372731872903198:
                        embed.add_field(name = mem, value=net['net'], inline = False)
                except KeyError:
                    print(f"KeyError with {mem} with id {mem.id}")

        await ctx.send(embed = embed)
    @baltop.error
    async def baltop_error(self, ctx, err):
        if isinstance(err, KeyError):
            print("KeyError")
        else:
            raise

def setup(client):
    client.add_cog(Bank(client))