import json
import os
from os.path import abspath, dirname

import discord
from cogs.Utils import Utils

from discord.ext import commands

filepath = dirname(abspath(__file__))

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


class Writter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 60, commands.BucketType.channel)
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def train(self, ctx):
        lang = Utils.get_lang(None, ctx.message)
        await ctx.send(embed=Utils.done_embed(locales[lang]['etc']['on_train']))
        f = open(
            filepath + '/../samples/{0}.txt'.format(ctx.message.guild.id), 'w')
        ff = open(
            filepath + '/../samples/{0}_img.txt'.format(ctx.message.guild.id), 'w')

        for channel in ctx.guild.text_channels:
            try:
                messages = await channel.history(limit=500).flatten()
                for message in messages:
                    if message.author.bot:
                        pass
                    else:
                        is_bad_word = False
                        for badword in config['bad_start_words']:
                            if message.content.startswith(badword):
                                is_bad_word = True
                                break
                        if is_bad_word == False:
                            f.write(discord.utils.escape_markdown(
                                message.clean_content.lower().strip()) + '\\')

                        for file in message.attachments:
                            if file.url[-3::] == 'png' or file.url[-3::] == 'jpg' or file.url[-3::] == 'jpeg':
                                ff.write(file.url + '\n')
            except:
                pass

        await ctx.send(embed=Utils.done_embed(locales[lang]['gen']['successful_index']))

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def wipe(self, ctx):
        lang = Utils.get_lang(None, ctx.message)

        os.remove(filepath + f"/../samples/{ctx.guild.id}.txt")
        os.remove(filepath + f"/../samples/{ctx.guild.id}_img.txt")
        await ctx.send(embed=Utils.done_embed(locales[lang]['etc']['on_wipe']))

    @ commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.startswith('ai.') or msg.content.startswith('aic.'):
            pass
        else:
            if msg.author.bot:
                pass
            else:
                if '\\' in msg.content:
                    pass
                elif msg.content == '':
                    pass
                else:
                    f = open(
                        filepath + '/../samples/{0}.txt'.format(msg.guild.id), 'a')
                    f.write(discord.utils.escape_markdown(
                        msg.clean_content.lower().strip()) + '\\')

                ff = open(
                    filepath + '/../samples/{0}_img.txt'.format(msg.guild.id), 'a')

                for file in msg.attachments:
                    if file.url[-3::] == 'png' or file.url[-3::] == 'jpg' or file.url[-3::] == 'jpeg':
                        ff.write(file.url + '\n')

            await self.bot.process_commands(msg)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        f = open(
            filepath + '/../samples/{0}.txt'.format(guild.id), 'w')
        ff = open(
            filepath + '/../samples/{0}_img.txt'.format(guild.id), 'w')

        for channel in guild.text_channels:
            try:
                messages = await channel.history(limit=500).flatten()
                for message in messages:
                    if message.author.bot:
                        pass
                    else:
                        if '\\' in message.content:
                            pass
                        elif message.content == '':
                            pass
                        else:
                            was_bad = False
                            for badword in config['bad_start_words']:
                                if message.content.startswith(badword):
                                    was_bad = True

                            f.write(discord.utils.escape_markdown(
                                message.clean_content.lower().strip()) + '\\')

                    for file in message.attachments:
                        if file.url[-3::] == 'png' or file.url[-3::] == 'jpg' or file.url[-3::] == 'jpeg':
                            ff.write(file.url + '\n')
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        os.remove(filepath + f"/../data/{guild.id}.png")
        os.remove(filepath + f"/../data/{guild.id}_img.png")


def setup(bot):
    bot.add_cog(Writter(bot))
