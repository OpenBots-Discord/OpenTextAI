import asyncio
import glob
import json
import datetime
from os.path import dirname
from os.path import abspath

import discord
from discord.ext import commands


class Workers(commands.Cog, name='Workers'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Workers'
        bot.loop.create_task(Workers.status_updater(self, bot))

    async def status_updater(self, bot):
        while True:
            try:
                members = 0
                for guilds in self.bot.guilds:
                    members += len(guilds.members)
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                         name='ai.help  ⼁  🖥   :  {0}  ⼁  👤  :  {1}'.format(len(self.bot.guilds), members)))
                await asyncio.sleep(10)
            except:
                pass


def setup(bot):
    bot.add_cog(Workers(bot))
