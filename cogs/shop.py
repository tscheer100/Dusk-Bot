import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from motor import motor_asyncio

load_dotenv('./.env')
MONGO_URL = os.getenv('MONGO_URL')

cluster = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = cluster['dusk-bank']
collection = db['bank']

class Shop(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.Bank = client.get_cog('Bank')
        self.open_bank = self.Bank.open_bank

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("shop ready")
    
    #commands
    @commands.command()
    async def shop(self, ctx, role = None): 
        await self.open_bank(ctx)
        ID = ctx.author.id
        user = await collection.find_one({'_id': ID})
        wallet_amt = user['wallet']
        member = ctx.author

        work = 200
        work_role = discord.utils.get(ctx.guild.roles, name='work')
        pray = 1000
        pray_role = discord.utils.get(ctx.guild.roles, name='pray')
        salvage = 1000
        salvage_role = discord.utils.get(ctx.guild.roles, name='salvage')
        dance = 1000
        dance_role = discord.utils.get(ctx.guild.roles, name='dance')
        workout = 1000
        workout_role = discord.utils.get(ctx.guild.roles, name='workout')

        
        if not role:
            embed_shop = discord.Embed(
                title = f"Dusk Shop",
                description = "Use `.shop <itme>` to purchase. \n **Example:** `.shop work`",
                color = discord.Color.purple()
            )
            
            embed_shop.add_field(name = "Can be used every 2 minutes. Cost: 200 coins", value = "`.work` pays 0-20 coins")
            embed_shop.add_field(name = "Can be used every 2 minutes Cost: 1000 coins", value = "`.pray` `.salvage` `.dance` `.workout` pays 0-40 coins", inline = False)
            embed_shop.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author.display_name}")
            embed_shop.set_thumbnail(url = "https://cdn.discordapp.com/attachments/767175117901266974/767250128045473802/duskiconmixedreborn.gif")
            await ctx.send(embed = embed_shop)

        if role == 'work':
            if user['wallet'] >= work:
                if not work_role in member.roles:
                    await collection.update_one({'_id': ID}, {'$set': {'wallet': wallet_amt - work} })
                    await member.add_roles(work_role)
                    await ctx.send("You have purchased the **work** role for **200 coins**")
                else:
                    await ctx.send("You already have that role.")
            else:
                await ctx.send("You don't have enough coinage to buy this.")
        
        if role == 'pray':
            if user['wallet'] >= pray:
                if not pray_role in member.roles:
                    await collection.update_one({'_id': ID}, {'$set': {'wallet': wallet_amt - pray} })
                    await member.add_roles(pray_role)
                    await ctx.send("You have purchased the **pray** role for **1000 coins**")
                else:
                    await ctx.send("You already have that role.")
            else:
                await ctx.send("You don't have enough coinage to buy this.")

        if role == 'salvage':
            if user['wallet'] >= salvage:
                if not salvage_role in member.roles:
                    await collection.update_one({'_id': ID}, {'$set': {'wallet': wallet_amt - salvage} })
                    await member.add_roles(salvage_role)
                    await ctx.send("You have purchased the **salvage** role for **1000 coins**")
                else:
                    await ctx.send("You already have that role.")
            else:
                await ctx.send("You don't have enough coinage to buy this.")
        
        if role == 'dance':
            if user['wallet'] >= dance:
                if not dance_role in member.roles:
                    await collection.update_one({'_id': ID}, {'$set': {'wallet': wallet_amt - dance} })
                    await member.add_roles(dance_role)
                    await ctx.send("You have purchased the **dance** role for **1000 coins**")
                else:
                    await ctx.send("You already have that role.")
            else:
                await ctx.send("You don't have enough coinage to buy this.")

        if role == 'workout':
            if user['wallet'] >= workout:
                if not workout_role in member.roles:
                    await collection.update_one({'_id': ID}, {'$set': {'wallet': wallet_amt - workout} })
                    await member.add_roles(workout_role)
                    await ctx.send("You have purchased the **workout** role for **1000 coins**")
                else:
                    await ctx.send("You already have that role.")
            else:
                await ctx.send("You don't have enough coinage to buy this.")
        
        
                
def setup(client):
    client.add_cog(Shop(client))
