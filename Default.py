import discord
import requests
from discord.ext import commands


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_pin = True
        self.auto_delete = False
        self.time_default_locations = ["America/New_York", "Australia/Melbourne"]

    async def do_the_hook(self, channel, string):
        with open("Evil.png", 'rb') as f:
            bot_pfp = f.read()
        hook = await channel.create_webhook(name="S&R", avatar=bot_pfp)
        await hook.send(string)
        await hook.delete()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.auto_pin:
            if str(reaction.emoji) == "<:upvote:724823464325939250>":
                msg = reaction.message
                for r in msg.reactions:
                    if str(r.emoji) == "<:upvote:724823464325939250>" and r.count == 7:
                        await msg.pin()
                        break
        if self.auto_delete:
            if str(reaction.emoji) == "🪓":
                msg = reaction.message
                for r in msg.reactions:
                    if str(r.emoji) == "🪓" and r.count == 5:
                        await msg.delete()
                        break

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if str(error) in ["You do not own this bot."]:
            await self.do_the_hook(ctx.channel, f":rage:  I can not let you do that **{ctx.author.mention}**")
        elif "required argument" in str(error):
            await self.do_the_hook(ctx.channel,
                                   f":rage:  You failed to supply the argument **{str(error).split(' ')[0]}** **{ctx.author.mention}**")
        elif str(error) == "The check functions for command frog failed.":
            await self.do_the_hook(ctx.channel,
                                   f":rage:  Remember that:     **{ctx.author.mention}**\n-   Max message length is 30 characters\n-   Make sure to separate sections with a comma.")
        elif "You are on cooldown" in str(error):
            await self.do_the_hook(ctx.channel, f":rage:  {str(error)}  **{ctx.author.mention}**")
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

    @commands.command()
    async def time(self, ctx, location=None):
        """Shows time in the given location.
        If location is not given, displays default locations.
        ------------
        location: string
            Area, e.g America/Argentina/Salta or Australia/Melbourne

        """
        times = ""
        if location is None:
            for i in self.time_default_locations:
                data = requests.get(f"https://worldtimeapi.org/api/timezone/{i}").json()
                date = data["datetime"].split('T')[0]
                time = data["datetime"].split('T')[1][0:5]
                times += f"**{i}** {date} ***{time}***\n"
        else:
            data = requests.get(f"https://worldtimeapi.org/api/timezone/{location}").json()
            date = data["datetime"].split('T')[0]
            time = data["datetime"].split('T')[1][0:5]
            times += f"**{location}** {date} ***{time}***\n"
        await ctx.channel.send(times)

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx, msg):
        print(msg)

    @commands.command(aliases=['ls'])
    @commands.is_owner()
    async def list_servers(self, ctx, invite: bool = False):
        if not invite:
            send_str = "Servers:\n"
            for i in self.bot.guilds:
                send_str += f"{i.name}\n"
            await ctx.channel.send(send_str)
        else:
            send_str = "Servers:\n"
            for i in self.bot.guilds:
                try:
                    invite = await i.invites()
                    send_str += f"{invite[0]}\n"
                except Exception:
                    pass
            await ctx.channel.send(send_str)

    @commands.command(aliases=["tap"])
    @commands.is_owner()
    async def toggleautopin(self, ctx):
        if self.auto_pin:
            self.auto_pin = False
            await ctx.channel.send("**Auto pin has been turned off.**")
        else:
            self.auto_pin = True
            await ctx.channel.send("**Auto pin has been turned on.**")

    @commands.command(aliases=["tad"])
    @commands.is_owner()
    async def toggleautodelete(self, ctx):
        if self.auto_delete:
            self.auto_delete = False
            await ctx.channel.send("**Auto delete has been turned off.**")
        else:
            self.auto_delete = True
            await ctx.channel.send("**Auto delete has been turned on.**")


def setup(bot):
    bot.add_cog(Default(bot))
