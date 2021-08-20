import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from motor import motor_asyncio

load_dotenv('./.env')
MONGO_URL = os.getenv('MONGO_URL')

cluster = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = cluster['dusk-bank']
collection = db['bank']

class Work(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.Bank = client.get_cog('Bank')
        self.open_bank = self.Bank.open_bank

    # 1 min
    @commands.command()
    @commands.cooldown(1,60, commands.BucketType.user)
    async def beg(self, ctx):
        await self.open_bank(ctx)
        self.user = ctx.author
        self.ID = ctx.author.id
        
        result = await collection.find_one({'_id': self.ID})
        wallet_amt = result['wallet']
        bank_amt = result['bank']
        earnings = random.randrange(100)
        if wallet_amt + bank_amt < 200:
            await ctx.send(f"Someone gave you **{earnings}** coins!")
            new_wallet = wallet_amt + earnings
            await collection.update_one({'_id': self.ID}, {'$set': {'wallet': new_wallet} })
        else:
            await ctx.send("You can only beg if your net worth is below __**200 coins**__")
    @beg.error 
    async def beg_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = "**You are on a cooldown!** please wait **{:.2f}s**".format(err.retry_after)   
            await ctx.send(msg)
        else:
            raise

    # 2 min
    @commands.has_role("work") 
    @commands.command()
    @commands.cooldown(1,120, commands.BucketType.user)
    async def work(self, ctx):
        await self.open_bank(ctx)
        earned = random.randrange(20)
        ID = ctx.author.id
        result = await collection.find_one({'_id': ID})
        wallet_amt = result['wallet']

        await ctx.send(f"You worked for **{earned}** coins")
        new_wallet = wallet_amt + earned
        await collection.update_one({'_id': ID}, {'$set': {'wallet': new_wallet} })
    @work.error
    async def work_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = "**You are on a cooldown!** please wait **{:.2f}s**".format(err.retry_after)   
            await ctx.send(msg)
        elif isinstance(err, commands.errors.MissingRole):
            await ctx.send("You don't have the work command. Buy it by using `.shop`")
        else:
            raise
    
    # 5 min
    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def pray(self, ctx):
        await self.open_bank(ctx)
        earned = random.randrange(40)
        ID = ctx.author.id
        result = await collection.find_one({'_id': ID})
        wallet_amt = result['wallet']

        await ctx.send(f"You prayed  to the Flying Spaghetti Monster. \nHis noodly appendages hand you **{earned}** coins! R'amen!")
        new_wallet = wallet_amt + earned
        await collection.update_one({'_id': ID}, {'$set': {'wallet': new_wallet} })
    @pray.error
    async def pray_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = "**You are on a cooldown!** please wait **{:.2f}s**".format(err.retry_after)   
            await ctx.send(msg)
        else:
            raise

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def salvage(self, ctx):
        await self.open_bank(ctx)
        earned = random.randrange(40)
        ID = ctx.author.id
        result = await collection.find_one({'_id': ID})
        wallet_amt = result['wallet']

        await ctx.send(f"You have salvaged **{earned}** coins digging through dumpsters")
        new_wallet = wallet_amt + earned
        await collection.update_one({'_id': ID}, {'$set': {'wallet': new_wallet} })
    @salvage.error
    async def salvage_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = "**You are on a cooldown!** please wait **{:.2f}s**".format(err.retry_after)   
            await ctx.send(msg)
        else:
            raise

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def dance(self, ctx):
        await self.open_bank(ctx)
        earned = random.randrange(40)
        ID = ctx.author.id
        result = await collection.find_one({'_id': ID})
        wallet_amt = result['wallet']

        await ctx.send(f"You danced on the street as bystanders tip you **{earned}** coins")
        new_wallet = wallet_amt + earned
        await collection.update_one({'_id': ID}, {'$set': {'wallet': new_wallet} })
    @dance.error
    async def dance_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = "**You are on a cooldown!** please wait **{:.2f}s**".format(err.retry_after)   
            await ctx.send(msg)
        else:
            raise


    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def workout(self, ctx):
        await self.open_bank(ctx)
        earned = random.randrange(40)
        ID = ctx.author.id
        result = await collection.find_one({'_id': ID})
        wallet_amt = result['wallet']

        await ctx.send(f"You workout and a pansexual cowboy appreciates your abs and gives you **{earned}** coins")
        new_wallet = wallet_amt + earned
        await collection.update_one({'_id': ID}, {'$set': {'wallet': new_wallet} })
    @workout.error
    async def workout_error(self, ctx, err):
        if isinstance(err, commands.CommandOnCooldown):
            msg = "**You are on a cooldown!** please wait **{:.2f}s**".format(err.retry_after)   
            await ctx.send(msg)
        else:
            raise

def setup(client):
    client.add_cog(Work(client))