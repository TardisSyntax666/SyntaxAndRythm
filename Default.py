import os
import random
import csv
import time
import webbrowser
from PIL import Image
import discord
import pyautogui
import requests
from discord.ext import commands, tasks
import channel_order_db as cod
import asyncio
from datetime import datetime


def screenshot_this_message(msg_url=None):
    webbrowser.open(msg_url)
    a = 0
    fname = "PrototypeReasources/screenshots/dasBoom.png"
    spot = pyautogui.locateOnScreen("PrototypeReasources/screenshots/tester.png")
    while spot is None:
        time.sleep(0.2)
        a += 1
        if a == 600:
            break
        spot = pyautogui.locateOnScreen("PrototypeReasources/screenshots/tester.png")
    print(a)
    if a != 600:
        print("YES!!!")
        print(spot)
        time.sleep(1)
        pyautogui.screenshot(imageFilename=fname)
        im = Image.open(fname)
        im = im.crop((312, 151, 1359, 829))
        im.save(fname)

        return discord.File(fname)
    else:
        return None


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_pin = True
        self.auto_pin_num = 7
        self.auto_delete = False
        self.time_default_locations = ["America/New_York", "Australia/Melbourne"]
        self.last_time_sorted = "N/A"

    @commands.Cog.listener()
    async def on_ready(self):
        #self.sort_all_channels.start()
        pass

    async def do_the_hook(self, channel, string):
        with open("Evil.png", 'rb') as f:
            bot_pfp = f.read()
        hook = await channel.create_webhook(name="S&R", avatar=bot_pfp)
        await hook.send(string)
        await hook.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.get(self.bot.guilds, id=payload.guild_id)
        channel = discord.utils.get(guild.channels, id=payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        if self.auto_pin:
            for r in msg.reactions:
                if r.count == self.auto_pin_num:
                    # await msg.pin()
                    await asyncio.sleep(5)
                    data = []
                    with open("Niches/starboard.txt", encoding="UTF-8") as f:
                        for line in f:
                            data.append(line.strip())
                    print(msg.jump_url)
                    print(data)
                    if str(msg.jump_url) not in data:
                        channel1 = discord.utils.get(msg.guild.channels, id=977825506399518761)  # 977825506399518761

                        await channel1.send(content=msg.jump_url, file=screenshot_this_message(msg.jump_url))
                        await msg.add_reaction("✨")
                        with open("Niches/starboard.txt", "a", encoding="UTF-8") as f:
                            f.write(msg.jump_url + "\n")
                        break
        if self.auto_delete:
            if str(payload.emoji) == "🪓":
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
    @commands.is_owner()
    async def collect_data(self, ctx):
        a = await ctx.channel.send("This may take a while. You will be pinged when the data is ready.")
        channels = ctx.guild.channels
        header = ['author', 'content']
        filename = f"{ctx.author.name}_message_logs.csv"
        with open(filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for channel in channels:
                str1 = f"This may take a while. You will be pinged when the data is ready. **{int(os.stat(filename).st_size) / 1000000}mb** **{channels.index(channel) + 1}/{len(channels)}**"
                b = await ctx.channel.send(str1)
                await a.delete()
                a = b
                if type(channel) is discord.TextChannel:
                    async for msg in channel.history(limit=10000):
                        writer.writerow([msg.author, msg.content])

        await a.reply(f"{ctx.author.mention} Data Collected.", file=discord.File(filename))
        if int(os.stat(filename).st_size) / 1000000 > 8:
            await a.reply("The file was too big.")
        else:
            os.remove(filename)

    @commands.command()
    @commands.is_owner()
    async def edit(self, ctx, *, new_content):
        pass

    @commands.command()
    @commands.is_owner()
    async def sort_all_channels_manual(self, ctx):
        print(self.bot.guilds)
        guild = discord.utils.get(self.bot.guilds, id=715341363746439250)
        if guild is not None:
            for category_id in [715341363746439252, 715349646364377098]:
                category = discord.utils.get(guild.categories, id=category_id)

                def takesecond(elm):
                    return elm[1]

                unsorted = []
                for channel in category.channels:
                    points = int(cod.get_channel_points(category.id, channel.id))
                    if points != 0:
                        unsorted.append((channel.id, points))
                unsorted.sort(key=takesecond)
                sorted = unsorted
                sorted.reverse()
                for i in sorted:
                    channel = discord.utils.get(guild.channels, id=i[0])
                    await asyncio.sleep(5)
                    await channel.edit(position=sorted.index(i) + 1)

    @commands.command()
    @commands.is_owner()
    async def sort_channels(self, ctx):
        def takesecond(elm):
            return elm[1]

        category = ctx.channel.category
        unsorted = []
        for channel in category.channels:
            points = int(cod.get_channel_points(category.id, channel.id))
            if points != 0:
                unsorted.append((channel.id, points))
        unsorted.sort(key=takesecond)
        sorted = unsorted
        sorted.reverse()
        for i in sorted:
            channel = discord.utils.get(ctx.guild.channels, id=i[0])
            await asyncio.sleep(5)
            await channel.edit(position=sorted.index(i) + 1)

    @commands.command()
    async def channel_points(self, ctx, allQ=False):
        if allQ:
            for category_id in [715341363746439252, 715349646364377098]:
                category = discord.utils.get(ctx.guild.categories, id=category_id)
                msg = "**Channel Points:**\n\n"
                for channel in category.channels:
                    points = cod.get_channel_points(category.id, channel.id)
                    msg += f"{channel.name}: {points}\n"
                await ctx.channel.send(msg)
        else:
            points = cod.get_channel_points(ctx.channel.category.id, ctx.channel.id)
            embed = discord.Embed(title=f"{ctx.channel.name}: {points}",
                                  description="This message will be deleted in 5 seconds.")
            await ctx.message.delete()
            a = await ctx.channel.send(embed=embed)
            await asyncio.sleep(5)
            await a.delete()

    @commands.command(aliases=["lp"])
    async def listpins(self, ctx):
        """Lists all the pins in the channel that the command is ran in.
        ------------
        No Parameters
        """
        if str(ctx.author.id) in ["331681967437512705", str(ctx.guild.owner_id)]:
            pin_messages = await ctx.channel.pins()
            with open("temp_pins.txt", "w") as f:
                for m in pin_messages:
                    f.write(f"{m.jump_url}\n")
            await ctx.channel.send(file=discord.File("temp_pins.txt"))
        else:
            await self.do_the_hook(ctx.channel, f":rage:  I can not let you do that **{ctx.author.mention}**")

    @commands.command(aliases=["rp"])
    async def randompin(self, ctx):
        pin_messages = await ctx.channel.pins()
        await ctx.channel.send(pin_messages[random.randint(0, len(pin_messages) - 1)].jump_url)

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
    async def emoji_bomb(self, ctx):
        """Send a bunch of random emojis.
        ------------
        no parameters

        """
        data = []
        with open("Niches/raw_emojis.txt", encoding="UTF-8") as f:
            for line in f:
                data.append(line.strip())
        str_to_send = ""
        for i in range(0, 500):
            str_to_send += data[random.randint(0, len(data) - 1)] + " "
        await ctx.channel.send(str_to_send)

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx, msg):
        print(msg)

    @commands.command(aliases=["cap"])
    @commands.is_owner()
    async def changeautopin(self, ctx, num: int):
        self.auto_pin_num = num
        await ctx.channel.send(f"Changed AUTO_PIN_NUM to {num}.")

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

    @tasks.loop(hours=1)
    async def sort_all_channels(self):
        self.last_time_sorted = datetime.now().strftime("%H:%M:%S")
        guild = discord.utils.get(self.bot.guilds, id=715341363746439250)
        if guild is not None:
            for category_id in [715341363746439252, 715349646364377098]:
                category = discord.utils.get(guild.categories, id=category_id)

                def takesecond(elm):
                    return elm[1]

                unsorted = []
                for channel in category.channels:
                    points = int(cod.get_channel_points(category.id, channel.id))
                    if points != 0:
                        unsorted.append((channel.id, points))
                unsorted.sort(key=takesecond)
                sorted = unsorted
                sorted.reverse()
                for i in sorted:
                    channel = discord.utils.get(guild.channels, id=i[0])
                    print(channel.name)
                    await asyncio.sleep(5)
                    await channel.edit(position=sorted.index(i) + 1)
            channel = discord.utils.get(guild.channels, id=740454789007278120)
            await channel.edit(topic=f"Last sorted at {self.last_time_sorted}.")


def setup(bot):
    bot.add_cog(Default(bot))
