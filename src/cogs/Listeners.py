import asyncio
import requests
import json
from os.path import dirname
from os.path import abspath
import datetime

from termcolor import cprint

from cogs.Utils import Utils

import discord
from discord.ext import commands


with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


class Listeners(commands.Cog, name='Listeners'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Listeners'

    @commands.Cog.listener()
    async def on_command(self, ctx):
        now = datetime.datetime.now()
        time = now.strftime('%H:%M:%S')
        cprint(locales[config['default_locale']]['bot_log']
               ['log_cmd'].format(time, ctx.message.author, ctx.command.name, ctx.message.guild), 'green', attrs=['dark'])

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        lang = Utils.get_lang(None, ctx.message)

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.MissingPermissions):
            embed = Utils.error_embed(
                locales[lang]['errors']['missing_perms'])
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()

        elif isinstance(error, commands.BotMissingPermissions):
            embed = Utils.error_embed(
                locales[lang]['errors']['missing_bot_perms'])
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()

        elif isinstance(error, commands.CommandOnCooldown):
            embed = Utils.error_embed(
                locales[lang]['errors']['cooldown'].format(
                    error.retry_after))
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()

        else:
            now = datetime.datetime.now()
            time = now.strftime('%H:%M:%S')
            cprint(locales[config['default_locale']]['bot_log']
                   ['warn'].format(time, str(error)), 'red')
            embed = discord.Embed(title=locales[lang]['errors']['on_error_title'],
                                  description=locales[lang]['errors']['on_error_text'].format(str(error)), color=0xdd0000)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()


def setup(bot):
    bot.add_cog(Listeners(bot))
