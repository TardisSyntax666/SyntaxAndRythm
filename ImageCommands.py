import random
import shutil
from PIL import Image
import discord
import requests
from discord.ext import commands
import Image_Functions as IF


class RGBGuessMessage:
    def __init__(self, ctx, lifespan, value, filename, right_emoji):
        self.a = None
        self.right_emoji = right_emoji
        self.filename = filename
        self.value = value
        self.lifespan = lifespan
        self.title = "RGB Guesser!"
        self.description = "React with the appropriate emoji to guess which colour is the closest to the RGB value."
        self.author = ctx.author
        self.ctx = ctx

    async def send(self):
        embed = self.createEmbed()
        a = await self.ctx.channel.send(embed=embed[0], file=embed[1])
        self.a = a
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        for i in emojis:
            await a.add_reaction(i)

    def createEmbed(self):
        embed = discord.Embed(title=self.title, description=self.description)
        embed.add_field(name="RGB Value", value=self.value)
        file = discord.File(self.filename)
        embed.set_image(url="attachment://output.png")
        embed.set_footer(text=f"This message will close after {self.lifespan} hour.")
        return [embed, file]

    async def edit(self):
        embed = discord.Embed(title=self.title, description=self.description)
        embed.add_field(name="RGB Value", value=self.value)
        embed.add_field(name="Correct!✅", value="Good Job!")
        embed.set_image(url="attachment://output.png")
        await self.a.edit(embed=embed)

    def kill(self):
        self.lifespan -= 1
        if self.lifespan == 0:
            return True
        else:
            return False


def get_pfp(url, size, name):
    filename = f"Image_Commands/Pfps/{name}.png"
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        img = Image.open(filename).convert('RGBA')
        if size is not None:
            img = img.resize(size)
    else:
        img = None
        print("Error when getting pfp")
    return img


class ImageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sums = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣']:
            for message in self.sums:
                if (message.a.id == payload.message_id) and (payload.member == message.author):
                    if str(payload.emoji) == str(message.right_emoji):
                        await message.edit()
                        self.sums.remove(message)

    @commands.command(aliases=["rgbguess", "rgbg", "colour_gusse", "colourg"])
    async def rgb_guess(self, ctx):
        colours = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                   (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                   (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                   (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))]
        num = random.randint(0, 3)
        colour_to_use = colours[num]

        temp_imgs = []
        for i in colours:
            img = Image.new("RGB", (200, 200), i)
            temp_imgs.append(img)

        img1 = Image.new("RGB", (400, 400), (0, 0, 0))

        img1.paste(temp_imgs[0], (0, 0))
        img1.paste(temp_imgs[1], (200, 0))
        img1.paste(temp_imgs[2], (0, 200))
        img1.paste(temp_imgs[3], (200, 200))

        img2 = Image.open("Image_Commands/RGB/1.png").convert("RGBA")
        img1.paste(img2, (0, 0), img2)
        img2 = Image.open("Image_Commands/RGB/2.png").convert("RGBA")
        img1.paste(img2, (200, 0), img2)
        img2 = Image.open("Image_Commands/RGB/3.png").convert("RGBA")
        img1.paste(img2, (0, 200), img2)
        img2 = Image.open("Image_Commands/RGB/4.png").convert("RGBA")
        img1.paste(img2, (200, 200), img2)

        filename = "Image_Commands/RGB/output.png"
        img1.save(filename)
        if num == 0:
            emoji = '1️⃣'
        elif num == 1:
            emoji = '2️⃣'
        elif num == 2:
            emoji = '3️⃣'
        elif num == 3:
            emoji = '4️⃣'

        special = RGBGuessMessage(ctx, 2, colour_to_use, filename, emoji)
        await special.send()
        self.sums.append(special)

    @commands.command()
    async def les(self, ctx, member: discord.Member = None, img_url=None):
        """Make someone's profile picture the same colour scheme as the lesbian flag.
        Replies with edited Image.
        ------------
        member: user mention [defaults to author]
            The member who's profile picture will be edited.
        img_url: a image url [NOT NECESSARY]
            Mention yourself and then add an image url to use the command on a different image.
        """
        size = (500, 500)
        if member is None:
            member = ctx.author
        if img_url is not None:
            img_url_to_use = img_url
            size = None
        else:
            img_url_to_use = member.avatar_url
        pfp = get_pfp(img_url_to_use, size, member.name)
        img = IF.image_palette_les(pfp)
        img.save(f"Image_Commands/Les/{member.name}.png")

        file = discord.File(f"Image_Commands/Les/{member.name}.png")
        await ctx.channel.send(file=file)

    @commands.command()
    async def gay(self, ctx, member: discord.Member = None, img_url=None):
        """Make someone's profile picture the same colour scheme as the gay flag.
        Replies with edited Image.
        ------------
        member: user mention [defaults to author]
            The member who's profile picture will be edited.
        img_url: a image url [NOT NECESSARY]
            Mention yourself and then add an image url to use the command on a different image.
        """
        size = (500, 500)
        if member is None:
            member = ctx.author
        if img_url is not None:
            img_url_to_use = img_url
            size = None
        else:
            img_url_to_use = member.avatar_url
        pfp = get_pfp(img_url_to_use, size, member.name)
        img = IF.image_palette_gay(pfp)
        img.save(f"Image_Commands/Gay/{member.name}.png")

        file = discord.File(f"Image_Commands/Gay/{member.name}.png")
        await ctx.channel.send(file=file)

    @commands.command()
    async def bi(self, ctx, member: discord.Member = None, img_url=None):
        """Make someone's profile picture the same colour scheme as the bi-sexual flag.
        Replies with edited Image.
        ------------
        member: user mention [defaults to author]
            The member who's profile picture will be edited.
        img_url: a image url [NOT NECESSARY]
            Mention yourself and then add an image url to use the command on a different image.
        """
        size = (500, 500)
        if member is None:
            member = ctx.author
        if img_url is not None:
            img_url_to_use = img_url
            size = None
        else:
            img_url_to_use = member.avatar_url
        pfp = get_pfp(img_url_to_use, size, member.name)
        img = IF.image_palette_bi(pfp)
        img.save(f"Image_Commands/Bi/{member.name}.png")

        file = discord.File(f"Image_Commands/Bi/{member.name}.png")
        await ctx.channel.send(file=file)

    @commands.command()
    async def sus(self, ctx, member: discord.Member = None, img_url=None):
        """Someone looking real sus? Maybe time they put on their real space suit.
        Replies with edited Image.
        ------------
        member: user mention [defaults to author]
            The member who's profile picture will be edited.
        img_url: a image url [NOT NECESSARY]
            Mention yourself and then add an image url to use the command on a different image.
        """
        size = (511, 511)
        if member is None:
            member = ctx.author
        if img_url is not None:
            img_url_to_use = img_url
            size = (511, 511)
        else:
            img_url_to_use = member.avatar_url
        pfp = get_pfp(img_url_to_use, size, member.name)
        img1 = Image.open("Image_Commands/Sus/sus.png").convert('RGBA')
        img2 = Image.open("Image_Commands/Sus/sus_mask.png").convert('RGBA')
        img = IF.transparent_layered_image_mask(img1, pfp, img2, (759, 279))
        img.save(f"Image_Commands/Bi/{member.name}.png")

        file = discord.File(f"Image_Commands/Bi/{member.name}.png")
        await ctx.channel.send(file=file)


def setup(bot):
    bot.add_cog(ImageCommands(bot))
