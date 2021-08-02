import discord
from discord.ext import commands
import os
from PIL import Image, ImageDraw

dir_path = os.path.dirname(os.path.realpath("main.py"))


def frog_check(ctx):
    message = ctx.message.content.split(' ')[1]
    if ',' in message:
        msg1 = message.split(',')[0]
        msg2 = message.split(',')[1]

        if len(msg1) <= 30 or len(msg2) <= 30:
            return True
        else:
            return False
    else:
        return False


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(frog_check)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def frog(self, ctx, *, message):
        if ',' in message:
            msg1 = message.split(',')[0]
            msg2 = message.split(',')[1]

            if len(msg1) <= 30 or len(msg2) <= 30:

                import cv2
                import numpy as np
                import glob

                img_array = []
                for filename in glob.glob(f"{dir_path}/Frog/before/*.jpg"):
                    img = cv2.imread(filename)
                    height, width, layers = img.shape
                    size = (width, height)
                    img_array.append(img)

                out = cv2.VideoWriter(f"{dir_path}/Frog/Frog.avi", cv2.VideoWriter_fourcc(*'DIVX'), 10, size)

                for i in range(len(img_array)):
                    out.write(img_array[i])
                out.release()

                await ctx.channel.send(file=discord.File(f"{dir_path}/Frog/frog.avi"))

            else:
                await ctx.channel.send("Max message length is 30 characters")
        else:
            await ctx.channel.send("Make sure to separate sections with a comma.")


def setup(bot):
    bot.add_cog(Logs(bot))
