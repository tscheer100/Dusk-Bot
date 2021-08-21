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
        
        if not role:
            embed_shop = discord.Embed(
                title = f"Dusk Shop",
                description = "Use `.shop <itme>` to purchase. \n **Example:** `.shop work`",
                color = discord.Color.purple()
            )
            embed_shop.add_field(name = "Can be used every 2 minutes", value = "`.work` pays 0-20 coins")
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
                
def setup(client):
    client.add_cog(Shop(client))
