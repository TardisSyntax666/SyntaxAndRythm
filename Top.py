import discord
from discord.ext import commands
import Currency_External as ce


class Top(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def top(self, ctx):
        """An introduction message for ToP.
            Replies with an intro embed
            ------------
            No Parameters
            """
        member = ctx.author

        top_embed = discord.Embed(title=f"Thieves O' Plenty",
                                  colour=discord.Colour.purple())
        top_embed.set_author(name=f"ToP", icon_url="https://media.discordapp.net/attachments"
                                                   "/871319488002416730/871320277949247508/theif_icon"
                                                   ".png?width=523&height=517")
        top_embed.add_field(name="Intorduction", value="Welcome to Thieves O' Plenty (a.k.a ToP). Your one and only "
                                                       "quest is to steal and make money. You can steal to find gold. "
                                                       "Then sell said gold to get money. Be carefull tho. Just as you can steal from others."
                                                       " Others can steal from you.", inline=False)
        top_embed.add_field(name="Info",
                            value="For more information regarding ToP please see &howtoplaytop or &htptop.",
                            inline=False)
        top_embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/871319488002416730/871320277949247508/theif_icon.png?width"
                "=523&height=517")
        top_embed.set_image(
            url="https://media.discordapp.net/attachments/871319488002416730/871320332638773248"
                "/cooltext389937869728439.png?width=1200&height=158")
        top_embed.set_footer(text="This command has no steal risk.")

        await ctx.channel.send(embed=top_embed)

    @commands.command(aliases=["bal", "wal", "wallet"])
    @commands.is_owner()
    async def balance(self, ctx, member: discord.Member = None):
        """Shows current balance/wallet for ToP.
            Replies with an balance embed
            ------------
            member: user mention [defaults to author]
                The member who's balance you want displayed.
            """
        if member is None:
            member = ctx.author
        account = ce.fetch_account(ctx.guild.id, member.id)

        account_embed = discord.Embed(title=f"Your Balance",
                                      colour=member.colour)
        account_embed.set_author(name=f"{str(member)}", icon_url="https://media.discordapp.net/attachments"
                                                                 "/871319488002416730/871320277949247508/theif_icon.png?width=523&height=517")
        account_embed.add_field(name="**Money**",
                                value=f"${str(account.m_balance)}",
                                inline=True)
        account_embed.add_field(name="**Gold**",
                                value=f"{str(account.g_balance)}",
                                inline=True)
        account_embed.add_field(name="Knife",
                                value=f"{str(account.knife)}",
                                inline=False)
        account_embed.add_field(name="Steal risk",
                                value=f"{str(account.steal_risk)}",
                                inline=True)
        account_embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/871319488002416730/871319521380679740/money_bag.png?width"
                "=654&height=517")
        account_embed.set_image(
            url="https://media.discordapp.net/attachments/871319488002416730/871320332638773248/cooltext389937869728439.png?width=1200&height=158")
        account_embed.set_footer(text="This command has no steal risk.")

        await ctx.channel.send(embed=account_embed)


def setup(bot):
    bot.add_cog(Top(bot))
