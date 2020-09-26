import discord
import json
from os.path import abspath, dirname

from cogs.Utils import Utils

from discord.ext import commands
from discord.ext.commands import Bot

filepath = dirname(abspath(__file__))

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


class General(commands.Cog, name='General'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'General'

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        lang = Utils.get_lang(None, ctx.message)
        embed = discord.Embed(
            color=0x6cdbe0, title=locales[lang]['help']['help_title'], description=locales[lang]['help']['help_text'])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
