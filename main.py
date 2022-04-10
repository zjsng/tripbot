import os
import dotenv
from dotenv import load_dotenv

import datetime
import logging
import pprint
import discord
import requests
from cogs.osu import osu

from cogs.osuAPI import osuAPI
from discord.ext import commands

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='tripbot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Loading .env
load_dotenv()

# Global Variables
bot_token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='.')
cogs = ["cogs.osu"]

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

# Test command to check if the bot is alive
@bot.command()
async def test(ctx):
    print("Test command triggered.")
    await ctx.send("Sample command")

# Command to reload ALL cogs
@bot.command()
async def reload(ctx):
    print("Reloading all cogs...")
    for cog in cogs:
        bot.reload_extension(cog)
    await ctx.send("Cogs reloaded")

# Attach cogs as extensions to the bot before starting to run it
# Attaching as extension allows for hot reload of cogs
if __name__ == "__main__":
    for cog in cogs:
        bot.load_extension(cog)

# Run the bot with the token provided
bot.run(bot_token)