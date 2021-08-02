import discord
from discord.ext import commands

intents = discord.Intents(members=True, guilds=True, emojis=True, voice_states=True, presences=True, messages=True,
                          guild_messages=True, dm_messages=True, reactions=True, guild_reactions=True)
bot = commands.Bot(command_prefix='&', description="Syntax and Rhythm, Precision and Harmony")
cogs = ['Default', 'Logs', 'Music', 'ImageCommands', 'Top']
for cog in cogs:
    bot.load_extension(f"{cog}")


@bot.event
async def on_ready():
    print("--ONLINE--")
    await bot.change_presence(activity=discord.Game("Version 0.1.0"))


@bot.command()
@commands.is_owner()
async def load(ctx, cog_name=None):
    if cog_name is None:
        for cog in cogs:
            bot.load_extension(f"{cog}")
        await ctx.channel.send("Loaded **all**")
    else:
        bot.load_extension(f"{cog_name}")
        await ctx.channel.send(f"Loaded **{cog_name}**")


@bot.command()
@commands.is_owner()
async def unload(ctx, cog_name=None):
    if cog_name is None:
        for cog in cogs:
            bot.unload_extension(f"{cog}")
        await ctx.channel.send("Unloaded **all**")
    else:
        bot.unload_extension(f"{cog_name}")
        await ctx.channel.send(f"Unloaded **{cog_name}**")


@bot.command()
@commands.is_owner()
async def reload(ctx, cog_name=None):
    if cog_name is None:
        for cog in cogs:
            bot.reload_extension(f"{cog}")
        await ctx.channel.send("Reloaded **all**")
    else:
        bot.reload_extension(f"{cog_name}")
        await ctx.channel.send(f"Reloaded **{cog_name}**")

tokentxt = open("C:/Users/Michael/Desktop/token.txt", 'r')
token = None
for line in tokentxt:
    token = line.strip()
tokentxt.close()
bot.run(token)
