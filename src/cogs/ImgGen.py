from PIL import Image, ImageDraw, ImageFont

import discord
import json
import mc
import re
from os.path import abspath, dirname
from random import randint
import random
import requests
from io import BytesIO
import os

from cogs.Utils import Utils

from discord.ext import commands


filepath = dirname(abspath(__file__))

with open(dirname(abspath(__file__)) + '/../data/locales.json') as f:
    locales = json.load(f)

with open(dirname(abspath(__file__)) + '/../data/config.json') as f:
    config = json.load(f)


def get_generated_line(msg, minword=2, maxword=15, minsym=5, maxsym=150):
    samples_txt = mc.util.load_txt_samples(
        filepath + '/../samples/{0}.txt'.format(msg.guild.id), separator="\\")
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


class ImgGen(commands.Cog, name='ImgGen'):
    def __init__(self, bot):
        self.bot = bot
        self.name = 'ImgGen'

    @commands.command(aliases=['fresko'])
    async def f(self, ctx):
        result = get_generated_line(msg=ctx.message, maxsym=30)

        chance = randint(1, 20)
        if chance >= 1 and chance <= 13:
            result = result.capitalize()
        elif chance >= 14 and chance <= 17:
            result = result.lower()
        elif chance >= 18 and chance <= 20:
            result = result.upper()

        base = Image.open(filepath + "/../data/fressko.png").convert("RGBA")

        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        h, w = base.size

        fnt = ImageFont.truetype(filepath + "/../data/font.ttf", 50)
        d = ImageDraw.Draw(txt)

        tw, th = d.textsize(result, fnt)

        d.text(((w-tw) / 2 + 95, 300), result, font=fnt, fill=(0, 0, 0, 255))

        out = Image.alpha_composite(base, txt)

        id = randint(0, 100000000)
        out.save(filepath + f"/../data/f_temp_{id}.png")

        file = discord.File(filepath + f"/../data/f_temp_{id}.png",
                            filename="fresko.png")

        await ctx.send(file=file)
        os.remove(filepath + f"/../data/f_temp_{id}.png")

    @commands.command()
    async def dem(self, ctx, member: discord.Member = None):
        msg = get_generated_line(ctx.message, maxsym=20)
        msg2 = get_generated_line(ctx.message, maxsym=30)

        base = Image.open(filepath + "/../data/dem.png").convert("RGBA")

        if (ctx.message.attachments != []) and (ctx.message.attachments[0].url[-3::] == 'png' or ctx.message.attachments[0].url[-3::] == 'jpg' or ctx.message.attachments[0].url[-3::] == 'jpeg'):
            url = ctx.message.attachments[0].url
        elif member == None:
            with open(filepath + "/../samples/{0}_img.txt".format(ctx.message.guild.id), 'r') as imgs:
                url = random.choice(imgs.read().split('\n'))
        else:
            url = 'https://cdn.discordapp.com/avatars/{0}/{1}.png?size=256'.format(
                member.id, member.avatar)

        response = requests.get(url)

        image = Image.open(BytesIO(response.content)).convert("RGBA")
        image = image.resize((670, 670), Image.ANTIALIAS)
        image.copy()

        h, w = base.size
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

        fnt = ImageFont.truetype(filepath + "/../data/font.ttf", 60)
        fnt_small = ImageFont.truetype(filepath + "/../data/font.ttf", 36)

        d = ImageDraw.Draw(txt)

        th, tw = d.textsize(msg, fnt)
        ths, tws = d.textsize(msg2, fnt_small)

        txt.paste(image, (80, 50))

        d.text(((h-th) / 2, w - 136),
               msg, font=fnt, fill=(255, 255, 255, 255))

        d.text(((h-ths) / 2, w - 66),
               msg2, font=fnt_small, fill=(255, 255, 255, 255))

        out = Image.alpha_composite(base, txt)

        id = randint(0, 100000000)
        out.save(filepath + f"/../data/dem_temp_{id}.png")

        file = discord.File(filepath + f"/../data/dem_temp_{id}.png",
                            filename="demotivator.png")

        await ctx.send(file=file)
        os.remove(filepath + f"/../data/dem_temp_{id}.png")

    @dem.error
    async def dem_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('дурачок...')


def setup(bot):
    bot.add_cog(ImgGen(bot))
