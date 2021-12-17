import discord
from discord.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.print_all = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.print_all and not message.author.bot:
            print(message.content)
        if str(message.content) == "&tpam" and message.author.id == 331681967437512705:
            if self.print_all:
                self.print_all = False
            else:
                self.print_all = True
            await message.channel.send(f"Print all message as been set to {str(self.print_all)}.")


def setup(bot):
    bot.add_cog(Logs(bot))