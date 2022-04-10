import asyncio
import json
import pprint
import discord

from cogs.osuAPI import osuAPI
from discord.ext import commands

# Cog for handling all osu!-related commands
class osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def osu(self, ctx, offset):
        # Users would start with 1 instead of a 0
        offset = int(offset) - 1

        params = {
            'mode': 'osu',
            'limit': 5,
            'offset': int(offset) * 5
        }

        response = await osuAPI.get_response(f'{osuAPI.get_api_url()}/users/8497340/scores/best', params=params)

        pp_data = []
        for dictionary in response.json():
            if 'pp' in dictionary:
                pp_data.append(dictionary['pp'])

        count = (int(offset) * 5) + 1
        embedMsg = discord.Embed(
            title="Top Plays",
            description=f"Showing page {int(offset) + 1} of the user's top plays",
            colour=ctx.author.roles[-1].colour)
        for key in pp_data:
            embedMsg.add_field(name=f"#{count}", value=f"{key}pp", inline=False)
            count += 1

        await ctx.channel.send(embed=embedMsg)

# Function for loading as an extension
def setup(bot):
    bot.add_cog(osu(bot))