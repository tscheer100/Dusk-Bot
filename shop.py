import os
import discord
from discord.ext import commands
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

    @commands.command()
    async def shop(self, ctx, role = None):  
        await self.open_bank(ctx)
        ID = ctx.author.id
        user = await collection.find_one({'_id': ID})
        
        if role == None:
            embed_shop = discord.Embed(
                title = f"Dusk Shop",
                # description = "Buy ranks to gain perks, obtain jobs "
                color = discord.Color.purple()
            )
            embed_shop.add_field(name = ".work", value = "pays 0-20 coins")
            await ctx.send(embed = embed_shop)

        # if role == 'work':
        #     if 

def setup(client):
    client.add_cog(Shop(client))
