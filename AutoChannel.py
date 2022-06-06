import random

import discord
import requests
from discord.ext import commands
import channel_order_db as cod


class AutoChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (str(message.guild.id) == "715341363746439250") and (not message.author.bot) and (not str(message.content) in ["&populate", "&channel_points"]):
            channel = message.channel
            category = channel.category
            current = int(cod.get_channel_points(category.id, channel.id))
            cod.set_channel_points(category.id, channel.id, str(current + 1))


def setup(bot):
    bot.add_cog(AutoChannel(bot))
