import asyncio
import os
import random
import discord
from discord.ext import commands, tasks
import Currency_External as Ce
from datetime import datetime, timedelta, date
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from PIL import Image


class Top(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.once_per_day.start()

        self.gtime = datetime.now().strftime('0:%M:%S, AEST')
        gstonks_txt = open("Niches/GoldStonks.txt", 'r')
        for line in gstonks_txt:
            val = int(line.strip().split(":")[1])
            break
        self.gvalue = val

    async def do_the_hook(self, channel, string):
        with open("Evil.png", 'rb') as f:
            bot_pfp = f.read()
        hook = await channel.create_webhook(name="S&R", avatar=bot_pfp)
        await hook.send(string)
        await hook.delete()

    @commands.command(aliases=["rob", "borrowIndefinitely"])
    @commands.is_owner()
    @commands.cooldown(1, 60)
    async def steal(self, ctx):
        """Steals a random amount from an npc. Has a 1 minute cooldown.
            Replies an embed stating outcome
            ------------
            No Parameters
            """
        account = Ce.fetch_account(ctx.guild.id, ctx.author.id)

        steal_messages_txt = open(f"Niches/steal_messages.txt", 'r+')
        steal_messages = [[], [], [], []]
        e = 0
        for line in steal_messages_txt:
            if line.strip() != "":
                steal_messages[e].append(line.strip())
            else:
                e += 1
        # steal_messages_txt.close()
        # for i in steal_messages:
        #     print(i)

        num = random.randint(0, 99)
        if num in [0, 1]:
            steal_embed = discord.Embed(title=":white_check_mark: Stealing")
            steal_embed.add_field(name="Status", value="Successful")
            steal_embed.add_field(name="You Found:", value="A page from the developers note book! You have been dm'ed "
                                                           "a helpful insight into the workings of the steal command.")
            await ctx.channel.send(embed=steal_embed)
            await ctx.author.send(steal_messages[3][random.randint(0, len(steal_messages[3]) - 1)])
        else:

            steal_embed = discord.Embed(title=":yellow_circle: Stealing")
            steal_embed.add_field(name="Status", value="Pending...")

            if account.knife == "Rusty Knife":
                chance = 40
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867116638474300/Rusty_Knfie.png"
            elif account.knife == "Flint Knife":
                chance = 45
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867108400889916/Flint_Knfie.png"
            elif account.knife == "Stone Knife":
                chance = 50
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867121126383646/Stone_Knife.png"
            elif account.knife == "Iron Knife":
                chance = 55
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867112519692318/Iron_Knife.png"
            elif account.knife == "Steal Knife":
                chance = 60
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867121822650388/Steal_Knfie.png"
            elif account.knife == "Carbon Fiber Knife":
                chance = 65
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867104110100540/Carbon_Fiber_knife.png"
            elif account.knife == "Diamond Knife":
                chance = 70
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867363217416212/Diamond_Knife.png"
            elif account.knife == "Netherite Knife":
                chance = 75
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867112951681074/Netherite_Knife.png"
            elif account.knife == "Obsidian Knife":
                chance = 80
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867114432266261/Obsidian_Knife.png"
            elif account.knife == "Cardboard Knife":
                chance = 85
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867104458215464/Cardboard_Knife.png"
            else:
                chance = 1
                knife_img_url = None

            list_yes = []
            for i in range(chance):
                list_yes.append(i)

            num = random.randint(0, 99)

            pointer = Image.open("pointer.png").convert('RGBA')
            imgs = []
            for i in range(25):
                final_img = Image.new('RGBA', (900, 100), (255, 255, 255))
                green_img = Image.new('RGBA', (9 * chance, 100), (0, 167, 14))
                final_img.paste(green_img, (0, 0))
                final_img.paste(pointer, ((i + 1) * 36 - 28, 40), pointer)
                imgs.append(final_img)

            start = imgs[0]
            imgs.remove(start)
            start.save(f"output_{ctx.author.display_name}.gif", save_all=True, append_images=imgs, optimize=True, duration=0.0001, loop=0)

            final_img = Image.new('RGBA', (900, 100), (255, 255, 255))
            green_img = Image.new('RGBA', (9 * chance, 100), (0, 167, 14))
            final_img.paste(green_img, (0, 0))
            final_img.paste(pointer, ((int(num) + 1) * 9 - 28, 40), pointer)
            final_img.save(f"output_{ctx.author.display_name}.png")

            steal_embed.set_thumbnail(url=knife_img_url)

            file = discord.File(f"output_{ctx.author.display_name}.gif")
            steal_embed.set_image(url=f"attachment://output_{ctx.author.display_name}.gif")
            a = await ctx.reply(embed=steal_embed, file=file, mention_author=False)

            if num in list_yes:

                price_chance = 20
                current_hour = int(date.today().strftime("%H"))
                if current_hour < 7 and not current_hour == 0:
                    price_chance += 10  # Early bird
                elif current_hour == 12:
                    price_chance += 10  # Lunch time dash
                elif current_hour == 0:
                    price_chance += 20  # Midnight bonus
                elif current_hour == 20:
                    price_chance += 10  # Dinner time dash
                num = random.randint(0, 99)

                large_price = []
                for i in range(price_chance):
                    large_price.append(i)

                if num in large_price:
                    price = random.randint(10, 20)
                    msg = steal_messages[2][random.randint(0, len(steal_messages[2]) - 1)]
                else:
                    price = random.randint(1, 10)
                    msg = steal_messages[1][random.randint(0, len(steal_messages[1]) - 1)]

                await asyncio.sleep(3)
                account.add_g_balance(price)
                steal_embed = discord.Embed(title=":white_check_mark: Stealing")
                steal_embed.add_field(name="Status", value="Successful")
                steal_embed.set_thumbnail(url=knife_img_url)
                steal_embed.add_field(name="You found:", value=f"**{price}** Gold. {msg}")
                file = discord.File(f"output_{ctx.author.display_name}.png")
                steal_embed.set_image(url=f"attachment://output_{ctx.author.display_name}.png")
                await a.delete()
                await ctx.reply(embed=steal_embed, file=file)
            else:
                await asyncio.sleep(3)
                steal_embed = discord.Embed(title=":x: Stealing")
                steal_embed.add_field(name="Status", value="Failed")
                steal_embed.set_thumbnail(url=knife_img_url)
                steal_embed.add_field(name="You found:",
                                      value=f"Absolutely nothing. {steal_messages[0][random.randint(0, len(steal_messages[0]) - 1)]}")
                file = discord.File(f"output_{ctx.author.display_name}.png")
                steal_embed.set_image(url=f"attachment://output_{ctx.author.display_name}.png")
                await a.delete()
                await ctx.reply(embed=steal_embed, file=file)
        os.remove(f"output_{ctx.author.display_name}.gif")
        os.remove(f"output_{ctx.author.display_name}.png")

    @commands.command(aliases=["psteal", "prob", "playerrob"])
    @commands.is_owner()
    @commands.cooldown(1, 3600)
    async def playersteal(self, ctx, member : discord.Member):
        """Steals a random amount up to 10 from the mentioned user. Has a 1 hour cooldown.
            Replies an embed stating outcome
            ------------
            mention: discord.Member
                The mention of the user you wish to steal from.
            """

        account = Ce.fetch_account(ctx.guild.id, ctx.author.id)
        account_f = Ce.fetch_account(ctx.guild.id, member.id)
        if account_f.g_balance > 0:
            steal_embed = discord.Embed(title=":yellow_circle: Stealing")
            steal_embed.add_field(name="Status", value="Pending...")

            if account.knife == "Rusty Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867116638474300/Rusty_Knfie.png"
            elif account.knife == "Flint Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867108400889916/Flint_Knfie.png"
            elif account.knife == "Stone Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867121126383646/Stone_Knife.png"
            elif account.knife == "Iron Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867112519692318/Iron_Knife.png"
            elif account.knife == "Steal Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867121822650388/Steal_Knfie.png"
            elif account.knife == "Carbon Fiber Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867104110100540/Carbon_Fiber_knife.png"
            elif account.knife == "Diamond Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867363217416212/Diamond_Knife.png"
            elif account.knife == "Netherite Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867112951681074/Netherite_Knife.png"
            elif account.knife == "Obsidian Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867114432266261/Obsidian_Knife.png"
            elif account.knife == "Cardboard Knife":
                knife_img_url = "https://media.discordapp.net/attachments/871319488002416730/878867104458215464/Cardboard_Knife.png"
            else:
                knife_img_url = None

            chance = 20

            list_yes = []
            for i in range(chance):
                list_yes.append(i)

            num = random.randint(0, 99)

            pointer = Image.open("pointer.png").convert('RGBA')
            imgs = []
            for i in range(25):
                final_img = Image.new('RGBA', (900, 100), (255, 255, 255))
                green_img = Image.new('RGBA', (9 * chance, 100), (0, 167, 14))
                final_img.paste(green_img, (0, 0))
                final_img.paste(pointer, ((i + 1) * 36 - 28, 40), pointer)
                imgs.append(final_img)

            start = imgs[0]
            imgs.remove(start)
            start.save(f"output_{ctx.author.display_name}2.gif", save_all=True, append_images=imgs, optimize=True, duration=0.0001, loop=0)

            final_img = Image.new('RGBA', (900, 100), (255, 255, 255))
            green_img = Image.new('RGBA', (9 * chance, 100), (0, 167, 14))
            final_img.paste(green_img, (0, 0))
            final_img.paste(pointer, ((int(num) + 1) * 9 - 28, 40), pointer)
            final_img.save(f"output_{ctx.author.display_name}2.png")

            steal_embed.set_thumbnail(url=knife_img_url)

            file = discord.File(f"output_{ctx.author.display_name}2.gif")
            steal_embed.set_image(url=f"attachment://output_{ctx.author.display_name}2.gif")
            a = await ctx.reply(embed=steal_embed, file=file, mention_author=False)

            if num in list_yes:
                if account_f.g_balance <= 10:
                    take = account_f.g_balance
                else:
                    take = 10
                price = random.randint(1, take)

                await asyncio.sleep(3)
                account.add_g_balance(price)
                account_f.add_g_balance(int(price*-1))
                steal_embed = discord.Embed(title=":white_check_mark: Stealing")
                steal_embed.add_field(name="Status", value="Successful")
                steal_embed.set_thumbnail(url=knife_img_url)
                steal_embed.add_field(name="You found:", value=f"**{price}** Gold. I gusse that paid off. Don't tell **{member}**.")
                file = discord.File(f"output_{ctx.author.display_name}2.png")
                steal_embed.set_image(url=f"attachment://output_{ctx.author.display_name}2.png")
                await a.delete()
                await ctx.reply(embed=steal_embed, file=file)
            else:
                await asyncio.sleep(3)
                steal_embed = discord.Embed(title=":x: Stealing")
                steal_embed.add_field(name="Status", value="Failed")
                steal_embed.set_thumbnail(url=knife_img_url)
                steal_embed.add_field(name="You found:",
                                      value=f"Absolutely nothing. Maybe that'll teach you to steal from other players.")
                file = discord.File(f"output_{ctx.author.display_name}2.png")
                steal_embed.set_image(url=f"attachment://output_{ctx.author.display_name}2.png")
                await a.delete()
                await ctx.reply(embed=steal_embed, file=file)
            os.remove(f"output_{ctx.author.display_name}2.gif")
            os.remove(f"output_{ctx.author.display_name}2.png")
        else:
            await self.do_the_hook(ctx.channel,
                                   f":rage:  You can't steal from someone with no money **{ctx.author.mention}**")

    @commands.command(aliases=["gv", "goldv", "gvalue"])
    @commands.is_owner()
    async def goldvalue(self, ctx):
        """Current price/value for selling gold.
            Replies with a graph embed
            ------------
            No Parameters
            """

        stonks_embed = discord.Embed(title=f"Gold Value",
                                     colour=discord.Colour.purple(),
                                     description=f"The gold value's next update is at:\n **{(datetime.now() + timedelta(days=1)).strftime('%d %b %Y')} {self.gtime}**")
        stonks_embed.set_author(name=f"ToP", icon_url="https://media.discordapp.net/attachments"
                                                      "/871319488002416730/871320277949247508/theif_icon"
                                                      ".png?width=523&height=517")
        stonks_embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/871319488002416730/871320277949247508/theif_icon.png?width"
                "=523&height=517")
        file = discord.File("GoldStonks.png", filename="goldstonks.png")

        stonks_embed.set_image(
            url="attachment://goldstonks.png")
        stonks_embed.set_footer(text="This command has no steal risk.")

        await ctx.channel.send(file=file, embed=stonks_embed)

    @commands.command()
    @commands.is_owner()
    async def top(self, ctx):
        """An introduction message for ToP.
            Replies with an intro embed
            ------------
            No Parameters
            """

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
                            value="For more information regarding ToP please see `&howtoplaytop` or `&htptop`.",
                            inline=False)
        top_embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/871319488002416730/871320277949247508/theif_icon.png?width"
                "=523&height=517")
        top_embed.set_image(
            url="https://media.discordapp.net/attachments/871319488002416730/871320332638773248"
                "/cooltext389937869728439.png?width=1200&height=158")
        top_embed.set_footer(text="This command has no steal risk.")

        await ctx.channel.send(embed=top_embed)

    @commands.command(aliases=['htptop'])
    @commands.is_owner()
    async def howtoplaytop(self, ctx):
        """Information about how ToP works.
            Replies with an info embed
            ------------
            No Parameters
            """

        top_info_embed = discord.Embed(title=f"Thieves O' Plenty",
                                       colour=discord.Colour.purple())
        top_info_embed.set_author(name=f"ToP", icon_url="https://media.discordapp.net/attachments"
                                                        "/871319488002416730/871320277949247508/theif_icon"
                                                        ".png?width=523&height=517")
        top_info_embed.add_field(name="How to Play",
                                 value="You find gold by stealing it from others. You can use `&steal` "
                                       "to have a certain chance at stealing from an npc. Using "
                                       "`&psteal @mention` will give you a certain chance of stealing "
                                       "from another player. To make money you then have to sell your "
                                       "gold using `&sellgold`. The value of gold isn't always the "
                                       "same though so you better check how much gold is worth using "
                                       "`&goldvalue` first. Be careful though, as the days increase so "
                                       "to does your *steal_risk* which is how likely an npc will "
                                       "steal from you. The longer you wait to sell your gold the more "
                                       "likely you are to loose it. Your *steal_risk* resets at the "
                                       "end of the week.", inline=False)
        top_info_embed.add_field(name="Items",
                                 value="The knife is the only item in the game right now and you upgrade it with money to "
                                       "increase your chance of having a successful steal. For more info about items use "
                                       "`&shop` to browse items and their abilities.",
                                 inline=False)
        top_info_embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/871319488002416730/871320277949247508/theif_icon.png?width"
                "=523&height=517")
        top_info_embed.set_image(
            url="https://media.discordapp.net/attachments/871319488002416730/871320332638773248"
                "/cooltext389937869728439.png?width=1200&height=158")
        top_info_embed.set_footer(text="This command has no steal risk.")

        await ctx.channel.send(embed=top_info_embed)

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
        account = Ce.fetch_account(ctx.guild.id, member.id)

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

    @commands.command(aliases=["sgold", "sg", "sellg"])
    @commands.is_owner()
    async def sellgold(self, ctx, num: int):
        """Sells num amount of gold for money.
            Replies an embed stating the amount sold.
            ------------
            num: int
                The amount you wish to sell.
            """
        account = Ce.fetch_account(ctx.guild.id, ctx.author.id)

        if account.g_balance >= num > 0:
            account.add_g_balance(int(-1 * num))
            account.add_m_balance(int(num * self.gvalue))
            soldembed = discord.Embed(title=f"Sold! at the current price of **${self.gvalue}**",
                                      description=f"Added **${int(num * self.gvalue)}**",
                                      colour=discord.Colour.gold())
            soldembed.set_author(name=f"{str(ctx.author)}",
                                 icon_url="https://media.discordapp.net/attachments"
                                          "/871319488002416730/871320277949247508"
                                          "/theif_icon.png?width=523&height=517")
            soldembed.set_thumbnail(url="https://media.discordapp.net/attachments/871319488002416730"
                                        "/878815069666963546/gold.png")
            await ctx.reply(embed=soldembed)
        else:
            await self.do_the_hook(ctx.channel,
                                   f":rage:  Make sure you have the available gold before selling and make "
                                   f"sure that the amount you want to sell is a positive "
                                   f"integer **{ctx.author.mention}**")

    @tasks.loop(hours=1)
    async def once_per_day(self):
        day_check_txt = open(f"Niches/OnceADayCounter.txt", 'r')
        day = None
        for line in day_check_txt:
            day = str(line.strip())
            break
        day_check_txt.close()

        current_day = str(date.today().strftime("%d"))
        if day != current_day:
            day_check_txt = open(f"Niches/OnceADayCounter.txt", 'w')
            day_check_txt.write(current_day)
            day_check_txt.close()

            gold_stonks_txt = open(f"Niches/GoldStonks.txt", 'r+')
            gold_stonks = []
            for line in gold_stonks_txt:
                gold_stonks.append(line.strip())
            gold_stonks_txt.close()
            gold_stonks.reverse()
            while len(gold_stonks) > 9:
                gold_stonks.remove(gold_stonks[0])

            print("Once per day gold stonks")
            print(current_day)

            newnum = -1
            while newnum > 51 or newnum <= 0:
                print('here')
                a = 1
                if random.randint(0, 1) == 1:
                    a = -1
                newnum = round(self.gvalue + (a * (self.gvalue / 10) * random.randint(1, 10)))
            num = newnum
            self.gvalue = num

            gold_stonks.append(str(date.today().strftime("%d/%m/%Y")) + ":" + str(num))
            print(gold_stonks)

            x = []
            y = []
            for i in gold_stonks:
                d = i.split(":")[0]
                val = i.split(":")[1]

                x.append(datetime(int(d.split("/")[2]), int(d.split("/")[1]), int(d.split("/")[0])))
                y.append(int(val))
            plt.style.use('seaborn')
            plt.ylim(0, 50)
            plt.plot_date(x, y, color='green', linestyle='solid')
            for i in range(0, len(y)):
                plt.annotate(f"${y[i]}", (x[i], y[i]), fontsize=15)
            plt.legend(['Gold Value'])
            plt.gcf().autofmt_xdate()
            date_format = mpl_dates.DateFormatter('%d %b %Y')
            plt.gca().xaxis.set_major_formatter(date_format)
            plt.tight_layout()
            plt.savefig("GoldStonks.png")

            gold_stonks.reverse()
            gold_stonks_txt = open(f"Niches/GoldStonks.txt", 'w')
            for i in gold_stonks:
                gold_stonks_txt.write(i + "\n")


def setup(bot):
    bot.add_cog(Top(bot))
