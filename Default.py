import discord
from discord.ext import commands


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def do_the_hook(self, channel, string):
        with open("Evil.png", 'rb') as f:
            bot_pfp = f.read()
        hook = await channel.create_webhook(name="S&R", avatar=bot_pfp)
        await hook.send(string)
        await hook.delete()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if str(error) in ["You do not own this bot."]:
            await self.do_the_hook(ctx.channel, f":rage:  I can not let you do that **{ctx.author.mention}**")
        elif "required argument" in str(error):
            await self.do_the_hook(ctx.channel, f":rage:  You failed to supply the argument **{str(error).split(' ')[0]}** **{ctx.author.mention}**")
        elif str(error) == "The check functions for command frog failed.":
            await self.do_the_hook(ctx.channel, f":rage:  Remember that:     **{ctx.author.mention}**\n-   Max message length is 30 characters\n-   Make sure to separate sections with a comma.")
        else:
            print(error)

    @commands.command()
    async def ping(self, ctx):
        """Simple ping command to show latency.
        Replies with latency in milliseconds
        ------------
        No Parameters
        """
        await ctx.channel.send(f"Pong! {round(self.bot.latency * 1000)}ms")


def setup(bot):
    bot.add_cog(Default(bot))
