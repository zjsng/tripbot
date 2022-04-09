import asyncio
import json
import datetime
import aiohttp
import discord
import requests

from os import getenv

# Constant Global Variables
API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'https://osu.ppy.sh/oauth/token'

# Global Variables
token = ''
token_expire = ''

class osuAPI(object):
    # Get Functions
    def get_api_url():
        return API_URL

    # Set Functions

    # Async Request Functions (Used when doing API calls)
    
    # Always call get_token() before sending a request with the API to ensure token validity
    async def get_token():
        current_time_sec = datetime.datetime.now().timestamp()

        global token
        if not token or current_time_sec > token_expire:
            print('Trying to retrieve a new token...')
            token = await osuAPI.retrieve_oauth_token()
        else:
            print('Token still currently valid')

        return token
    
    # Generally to be only called by the get_token() function
    async def retrieve_oauth_token():
        body = {
            "client_id": 11507,
            "client_secret": 'tIwYM4hhyxcZvc4bLtIGTCCTvspOlLvjrdMMpFFo',
            "grant_type": "client_credentials",
            "scope": "public"
        }

        response = requests.post(TOKEN_URL, data=body)

        global token_expire
        token_expire = datetime.datetime.now().timestamp() + int(response.json().get('expires_in'))

        return response.json().get('access_token')

    # Should be called by commands in the osu! cog for requesting information using the API
    async def get_response(URL, params):
        token = await osuAPI.get_token()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        return requests.get(URL, params, headers=headers)