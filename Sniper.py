import discord

from discord.ext import commands
import de_messages as de


class Sniper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) == "❓":
            info = de.fetch_e_message(payload.message.id)
            if info is not None:
                

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        message = payload.cached_message

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        message = payload.cached_message

    @commands.command(aliases=["-_-"])
    async def dsnipe(self, ctx):
        """Simple ping command to show latency.
        Replies with latency in milliseconds
        ------------
        No Parameters
        """
        info = de.fetch_e_message(str(ctx.guild.id), str(ctx.channel.id))
        edit_embed = discord.Embed(title="Deleted Message")
        edit_embed.add_field(name="Time", value=info["time"])
        edit_embed.add_field(name="Content", value=info["content"])
        await ctx.channel.send(f"Pong! {round(self.bot.latency * 1000)}ms")


def setup(bot):
    bot.add_cog(Sniper(bot))
