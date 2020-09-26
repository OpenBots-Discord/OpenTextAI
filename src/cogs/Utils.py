import json
import mc
import re
from os.path import abspath, dirname
from random import randint

from discord.ext import commands
import discord

filepath = dirname(abspath(__file__))

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


class Utils(commands.Cog, name='Utils'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Utils'

    def done_embed(msg):
        return discord.Embed(color=0x00FF47, description="✅⼁" + msg)

    def error_embed(msg):
        return discord.Embed(color=0xED4242, description="🚫⼁" + msg)

    def get_lang(bot, message):
        with open(dirname(abspath(__file__)) + '/../data/langs.json', 'r') as f:
            langs = json.load(f)

        try:
            return langs[str(message.guild.id)]

        except KeyError:
            langs[str(message.guild.id)] = config['default_locale']

            with open(dirname(abspath(__file__)) + '/../data/langs.json', 'w') as f:
                json.dump(langs, f, indent=4)

            return langs[str(message.guild.id)]

    def get_chat(message):
        with open(filepath + '/../data/chats.json', 'r') as f:
            ch = json.load(f)
        try:
            return ch[str(message.guild.id)]
        except:
            pass


def setup(bot):
    bot.add_cog(Utils(bot))
