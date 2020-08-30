import asyncio
import re
import config
import json
import logger as log
from os.path import abspath, dirname
from random import randint

import discord
import mc
from discord.ext import commands
from discord.ext.commands import Bot

bot = Bot(command_prefix=config.DEFAULT_PREFIX, help_command=None)

filepath = dirname(abspath(__file__))


if config.LANGUAGE == "ru_RU":
    from translations.ru_RU import *
elif config.LANGUAGE == "en_EN":
    from translations.en_EN import *
else:
    log.warn(
        "Unable to load translations. Make sure you have entered the correct language.")
    exit()


def done_embed(msg):
    return discord.Embed(color=0x00FF47, description="✅⼁" + msg)


def error_embed(msg):
    return discord.Embed(color=0xED4242, description="🚫⼁" + msg)


def get_chat(message):
    with open(filepath + '/data/chats.json', 'r') as f:
        ch = json.load(f)
    try:
        return ch[str(message.guild.id)]
    except:
        pass


def get_generated_line(msg, minword=2, maxword=15, minsym=5, maxsym=150):
    samples_txt = mc.util.load_txt_samples(
        filepath + '/samples/{0}.txt'.format(get_chat(msg)), separator="\n")
    generator = mc.StringGenerator(samples=samples_txt)

    result = generator.generate_string(
        attempts=20,
        validator=mc.util.combine_validators(
            mc.validators.words_count(minword, maxword),
            mc.validators.symbols_count(minsym, maxsym),
        ),
    )

    clean_result = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', "[Link Deleted]", result)

    return clean_result


@commands.cooldown(1, 60, commands.BucketType.channel)
@commands.has_permissions(administrator=True)
@bot.command(aliases=['set'])
async def s(ctx):
    with open(filepath + '/data/chats.json', 'r') as f:
        logs = json.load(f)

    if str(ctx.guild.id) in logs:
        logs.pop(str(ctx.guild.id))

        with open(filepath + '/data/chats.json', 'w') as f:
            json.dump(logs, f, indent=4)
        await ctx.send(embed=done_embed(reset_chat_msg()))
    else:
        logs[str(ctx.guild.id)] = ctx.message.channel.id

        with open(filepath + '/data/chats.json', 'w') as f:
            json.dump(logs, f, indent=4)
        await ctx.send(embed=done_embed(set_chat_msg()))

        f = open(
            filepath + '/samples/{0}.txt'.format(get_chat(ctx.message)), 'w')
        messages = await ctx.message.channel.history(limit=15000).flatten()
        for i in messages:
            if i.author.bot:
                pass
            else:
                clean_msg = re.sub(r'\<[^)]*\>', '', i.content)
                if '\n' in clean_msg:
                    pass
                elif clean_msg == '':
                    pass
                else:
                    f.write(clean_msg.lower().strip() + '\n')
        await ctx.send(done_embed(successful_index()))


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        color=0x6cdbe0, title=help_title(), description=help_text())
    await ctx.send(embed=embed)


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(aliases=['burgut'])
async def b(ctx):
    try:
        lines = randint(2, 10)
        face = randint(1, 23)
        result = ''

        for _ in range(lines - 1):
            result += get_generated_line(ctx.message, 1, 10).upper() + "\n@\n"
        result += get_generated_line(ctx.message, 1, 10).upper()

        file = discord.File(
            filepath + '/data/burgut_faces/{0}.jpg'.format(face), filename='{0}.jpg'.format(face))
        embed = discord.Embed(
            color=0xff546b, title=burgut_title(), description=result)
        embed.set_image(url='attachment://{0}.jpg'.format(face))
        await ctx.send(file=file, embed=embed)
    except:
        await ctx.send(embed=error_embed(too_late_gen()))


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(aliases=['dialog', 'dialogue'])
async def d(ctx):
    try:
        lines = randint(2, 20)

        result = '```'
        for _ in range(lines):
            result += '> ' + \
                get_generated_line(ctx.message, 1, 10).capitalize() + "\n"
        result += '```'

        embed = discord.Embed(
            color=0xfcf36a, title=dialogue_title(), description=result)
        await ctx.send(embed=embed)

    except:
        await ctx.send(embed=error_embed(too_late_gen()))


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(aliases=['generate', 'gen'])
async def g(ctx, mode=''):
    try:
        if mode == "1":
            result = get_generated_line(ctx.message, 1, 4)
        elif mode == "2":
            result = get_generated_line(ctx.message, 4, 8)
        elif mode == "3":
            result = get_generated_line(ctx.message, 8, 15)
        else:
            result = get_generated_line(ctx.message)

        chance = randint(1, 20)
        if chance >= 1 and chance <= 10:
            result = result.capitalize()
        elif chance >= 11 and chance <= 15:
            result = result.lower()
        elif chance >= 16 and chance <= 20:
            result = result.upper()

        embed = discord.Embed(
            color=0x6cdbe0, title=gen_title(), description=result)
        await ctx.send(embed=embed)
    except:
        await ctx.send(embed=error_embed(too_late_gen()))


@bot.event
async def on_ready():
    print('Ready!')


@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(color=0x6cdbe0, title='**OpenTextAI**',
                          description=on_join_message())
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/avatars/748543469001244813/45d8aa6c9e33329de6a78519cbef4b4a.png?size=256')

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=embed)
            break


@bot.event
async def on_message(msg):
    try:
        if msg.channel.id == get_chat(msg):
            msg_chance = randint(1, 30)
            if msg_chance == 30:
                result = get_generated_line(msg)
                chance = randint(1, 20)
                if chance >= 1 and chance <= 10:
                    result = result.capitalize()
                elif chance >= 11 and chance <= 15:
                    result = result.lower()
                elif chance >= 16 and chance <= 20:
                    result = result.upper()

                await msg.channel.send(result)

            if msg.author.bot:
                pass
            else:
                f = open(
                    filepath + '/samples/{0}.txt'.format(get_chat(msg)), 'a')
                clean_msg = re.sub(r'\<[^)]*\>', '', msg.content)
                if '\n' in clean_msg:
                    pass
                elif clean_msg == '':
                    pass
                else:
                    f.write(clean_msg.lower().strip() + '\n')
    except:
        pass

    await bot.process_commands(msg)


@s.error
async def errors(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = error_embed(missing_perms())
        await ctx.send(embed=embed)
    if isinstance(error, commands.BotMissingPermissions):
        embed = error_embed(missing_bot_perms())
        await ctx.send(embed=embed)


bot.run(config.TOKEN)
