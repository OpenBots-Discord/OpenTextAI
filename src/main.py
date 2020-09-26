import asyncio
import json
from os.path import abspath, dirname

import discord
import mc
import os
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.Utils import Utils


with open(dirname(abspath(__file__)) + '/data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/data/config.json') as f:
    config = json.load(f)


bot = Bot(command_prefix=config['default_prefix'], help_command=None)

filepath = dirname(abspath(__file__))

a = discord.utils.get()


@bot.event
async def on_ready():
    for filename in os.listdir(filepath + '/cogs/'):
        if filename.endswith('.py'):
            bot.load_extension('cogs.{0}'.format(filename[:-3]))
    print('Ready!')


@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(color=0x6cdbe0, title='**OpenTextAI**',
                          description=locales['ru_RU']['etc']['on_join_message'])
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/avatars/748543469001244813/45d8aa6c9e33329de6a78519cbef4b4a.png?size=256')

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=embed)
            break


bot.run(config['token'])
