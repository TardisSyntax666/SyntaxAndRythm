import random

import discord
from discord.ext import commands
import random

messages = ["I can't even remember why i married you **Dad Bot**!", "I'm leaving and taking the kids, I'll be staying "
                                                                    "at my mothers place **Dad Bot**.",
            "It's so constant with you **Dad Bot**! You don't take anything seriously.", "Why do you live in this "
                                                                                         "make believe world where "
                                                                                         "everything has to be a joke "
                                                                                         "**Dad Bot**?",
            "When was the last time you went to one of jimmy's sport games **Dad Bot**?", "I'm getting a divorce "
                                                                                          "**Dad Bot**!",
            "I found your phone **Dad Bot**. Who the fuck is Jessica?"]


class MumBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def do_the_hook(self, channel, string):
        with open("mumstock.png", 'rb') as f:
            bot_pfp = f.read()
        hook = await channel.create_webhook(name="Mum Bot", avatar=bot_pfp)
        await hook.send(string)
        await hook.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author) == "Dad Bot#2189":
            msg = messages[random.randint(0, len(messages)-1)]
            await self.do_the_hook(message.channel, msg)
        pass


def setup(bot):
    bot.add_cog(MumBot(bot))