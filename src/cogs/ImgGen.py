from PIL import Image, ImageDraw, ImageFont

import discord
import json
import mc
import re
from os.path import abspath, dirname
from random import randint
import os

from cogs.Utils import Utils

from discord.ext import commands
from discord.ext.commands import Bot


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
    async def f(self, ctx, *, msg: str):
        result = get_generated_line(msg=ctx.message, maxsym=30)

        if msg != '':
            if len(msg) > 32:
                await ctx.send('хули так много блять')
                return
            else:
                result = msg

        else:
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
        out.save(filepath + f"/../data/temp_{id}.png")

        file = discord.File(filepath + f"/../data/temp_{id}.png",
                            filename="fresko.png")

        await ctx.send(file=file)
        os.remove(filepath + f"/../data/temp_{id}.png")


def setup(bot):
    bot.add_cog(ImgGen(bot))
