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

        params = {
            'include_fails': 0,
            'mode': 'osu',
            'limit': 5,
            'offset': int(offset) * 5
        }

        response = await osuAPI.get_response(f'{osuAPI.get_api_url()}/users/8497340/scores/best', params=params)

        # Removed to streamline the code
        # pp_data = []
        # for dictionary in response.json():
        #     if 'pp' in dictionary:
        #         pp_data.append(dictionary['pp'])

        count = (int(offset) * 5) + 1
        embed_msg = discord.Embed(
            title="Top Plays",
            description=f"Showing page {int(offset) + 1} of the user's top plays",
            colour=ctx.author.roles[-1].colour)
        embed_msg.set_footer(text=ctx.author)
        value_str = ''
        for dict in response.json():
            value_str += "**{}. [{} [{}] ]({})** [{}]\n{}pp\n".format(
                count, dict['beatmapset']['title'], dict['beatmap']['version'], dict['beatmap']['url'],
                dict['beatmap']['difficulty_rating'], dict['pp']
            )
            count += 1
        embed_msg.add_field(name=f"Top {int(count)-1} osu! Standard Plays", value=value_str, inline=False)

        await ctx.channel.send(embed=embed_msg)

# Function for loading as an extension
def setup(bot):
    bot.add_cog(osu(bot))