import shutil
from PIL import Image
import discord
import requests
from discord.ext import commands
import Image_Functions as IF


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
