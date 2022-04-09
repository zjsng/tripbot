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
        params = {
            'mode': 'osu',
            'limit': 5,
            'offset': int(offset) * 5
        }

        #response = requests.get(f'{osuAPI.get_api_url()}/users/8497340/scores/best', params=params, headers=headers)
        response = await osuAPI.get_response(f'{osuAPI.get_api_url()}/users/8497340/scores/best', params=params)

        #beatmapset_data = response.json()[0].get('beatmapset')
        pp_data = []
        for dictionary in response.json():
            if 'pp' in dictionary:
                pp_data.append(dictionary['pp'])

        await ctx.channel.send(pp_data)