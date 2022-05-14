import discord
from discord.ext import commands
import json
import urllib.request
import re
import io
import time
from multiprocessing.pool import ThreadPool
import requests

hextechbot = commands.Bot(command_prefix = "!")

@hextechbot.event
async def on_ready():
    '''
    Prints to console when the bot is ready to be used.
    '''
    print('Hextech Bot is ready.')

@hextechbot.command(aliases=['opgg', 'search', 'ugg'])
async def user(ctx, *args):
    '''
    Scrapes OP.GG to gather link to user's stat page.
    
    To use:
     !user <region> (defaults to NA) <name>
     !search <region> (defaults to NA) <name>
     !opgg <region> (defaults to NA) <name>
     !ugg <region> (defaults to NA) <name>
    '''
    print("user command triggered")
    arg_len = len(args)
    regions = ['oce', 'na', 'las', 'jp', 'br', 'tr', 'ru', 'eune', 'kr', 'lan', 'euw']
    default_region = regions[1]
    async with ctx.typing():
        if arg_len == 0:
            '''
            If no name inputted, uses users discord name.
            '''
            name = str(ctx.message.author).split('#')[0]
            if default_region == 'kr':
                await ctx.send(f"https://www.op.gg/summoner/userName={name}")
            else:
                await ctx.send(f"https://{default_region}.op.gg/summoner/userName={name}")

        elif arg_len >= 2 and args[0].lower() in regions:
            '''
            If user has a large name, use re.sub to subsitute chars. And has region specified.
            '''
            name = re.sub(r'\s', r'+', ' '.join(args[1:]))
            if args[0].lower() == 'kr':
                await ctx.send(f"https://www.op.gg/summoner/userName={name}")
            else:
                await ctx.send(f"https://{args[0].lower()}.op.gg/summoner/userName={name}")

        elif arg_len >= 1:
            '''
            If user has a large name, use re.sub to subsitute chars. No region specified, defaults to NA.
            '''
            name = re.sub(r'\s', r'+', ' '.join(args[0:]))
            await ctx.send(f"https://na.op.gg/summoner/userName={name}")

        else:
            await ctx.send(f"Usage: !user <region>(defaults to NA) <name>")


hextechbot.run('OTc1MDk2NzU5MjY3MjM3OTU1.G4nqfj.P8U82ifgIDWiHkuMeUbC5nxtCQt9aGU16IZZpk')    
