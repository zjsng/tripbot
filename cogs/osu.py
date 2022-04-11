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
    async def osutop(self, ctx, offset):
        # Users would start with 1 instead of a 0
        offset = int(offset) - 1

        # Call on the API for the required information
        # response will be multiple dictionaries depending on the limit provided in params
        url = f'{osuAPI.get_api_url()}/users/8497340/scores/best'
        params = osuAPI.get_params(0, 'osu', 5, int(offset) * 5)
        response = await osuAPI.get_response(url, params=params)

        # Formatting the embed's message with the response from osu! API
        value_list = []
        count = (int(offset) * 5) + 1
        for dict in response.json():
            value_list.append("**{}. [{} [{}] ]({})** [{}★]\n{}pp".format(
                count, dict['beatmapset']['title'], dict['beatmap']['version'], dict['beatmap']['url'],
                dict['beatmap']['difficulty_rating'], dict['pp']
            ))
            count += 1
        embed_msg = discord.Embed(
            description='\n'.join(value_list),
            colour=ctx.author.roles[-1].colour
        )
        embed_msg.set_author(
            name=f"{ctx.author.name}'s top plays",
            url="https://osu.ppy.sh/users/8497340",
            icon_url=ctx.author.avatar_url
        )
        embed_msg.set_footer(text=ctx.author)

        await ctx.channel.send(embed=embed_msg)

# Function for loading as an extension
def setup(bot):
    bot.add_cog(osu(bot))