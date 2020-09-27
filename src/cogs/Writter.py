import discord
import json
from os.path import abspath, dirname
from cogs.Utils import Utils

import discord
from discord.ext import commands

filepath = dirname(abspath(__file__))

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


class Writter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.cooldown(1, 60, commands.BucketType.channel)
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
                messages = await channel.history(limit=7500).flatten()
                for message in messages:
                    if message.author.bot:
                        pass
                    else:
                        f.write(message.content.lower().strip() + '\\')

                        for file in message.attachments:
                            if file.url[-3::] == 'png' or file.url[-3::] == 'jpg' or file.url[-3::] == 'jpeg':
                                ff.write(file.url + '\n')
            except:
                pass

        await ctx.send(embed=Utils.done_embed(locales[lang]['gen']['successful_index']))

    @ commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.startswith('ai.') or msg.content.startswith('aic.'):
            pass
        else:
            # try:
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
                    f.write(msg.content.lower().strip() + '\\')

                ff = open(
                    filepath + '/../samples/{0}_img.txt'.format(msg.guild.id), 'a')

                for file in msg.attachments:
                    if file.url[-3::] == 'png' or file.url[-3::] == 'jpg' or file.url[-3::] == 'jpeg':
                        ff.write(file.url + '\n')

            await self.bot.process_commands(msg)
        # except:
        #     pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        f = open(
            filepath + '/../samples/{0}.txt'.format(guild.id), 'w')
        ff = open(
            filepath + '/../samples/{0}_img.txt'.format(guild.id), 'w')

        for channel in guild.text_channels:
            try:
                messages = await channel.history(limit=7500).flatten()
                for message in messages:
                    if message.author.bot:
                        pass
                    else:
                        if '\\' in message.content:
                            pass
                        elif message.content == '':
                            pass
                        else:
                            f.write(message.content.lower().strip() + '\\')

                    for file in message.attachments:
                        if file.url[-3::] == 'png' or file.url[-3::] == 'jpg' or file.url[-3::] == 'jpeg':
                            ff.write(file.url + '\n')
            except:
                pass


def setup(bot):
    bot.add_cog(Writter(bot))
