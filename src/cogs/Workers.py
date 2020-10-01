import asyncio
import requests
import json
from os.path import dirname
from os.path import abspath

import discord
from discord.ext import commands


class Workers(commands.Cog, name='Workers'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Workers'
        bot.loop.create_task(Workers.status_updater(self, bot))
        # bot.loop.create_task(Workers.sdc_updater(self, bot))

    async def status_updater(self, bot):
        while True:
            try:
                members = 0
                for guilds in self.bot.guilds:
                    members += len(guilds.members)
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                         name='ai.help  ⼁  🖥   :  {0}  ⼁  👤  :  {1}'.format(len(self.bot.guilds), members)))
                await asyncio.sleep(60)
            except:
                pass

    async def sdc_updater(self, bot):
        with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
            config = json.load(f)
        while True:
            response = requests.post('https://api.server-discord.com/v2/bots/748543469001244813/stats',
                                     headers={
                                         "Authorization": config['sdc_token']},
                                     data={"servers": len(bot.guilds), "shards": 0})
            await asyncio.sleep(60)


def setup(bot):
    bot.add_cog(Workers(bot))
