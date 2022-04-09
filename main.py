import datetime
import logging
import pprint
import discord
import requests
from cogs.osu import osu

from cogs.osuAPI import osuAPI
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discordbot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Global Variables
bot = commands.Bot(command_prefix='.')

# Bot initialisation
# API token is requested on init of the bot
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    try:
        token = await osuAPI.get_token()
        print('Token: ' + token)
        print('OAuth retrieval success!')
    except Exception as e:
        print('Exception: ' + str(e))
    #token_expire = datetime.datetime.now().timestamp() + int(response['expires_in'])
    #print('Token: {}'.format(token))
    #print('Token expires at: {}'.format(token_expire))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        
    # Required to process any @bot.command() decorated commands due to on_message overriding
    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    await ctx.send("Sample command.")

# Attach cogs to the bot before starting to run it
bot.add_cog(osu(bot))

# Run the bot with the token provided
# TODO: Load bot token from file so that it is not leaked on GitHub
bot.run()