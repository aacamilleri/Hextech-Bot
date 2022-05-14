import discord
from discord.ext import commands
from runepage import get_runes
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

@hextechbot.command(aliases=['items'])
async def build(ctx, *args):
    '''
    Build/Items Command
    Lists builds for champion from OP.GG

    To use: 
     !build <lane> <champion>
     !items <lane> <champion>
    '''
    print('build command triggered')
    if len(args) != 2:
        await ctx.send('Usage: !build [lane] [champion]')
    else:
        async with ctx.typing():
            prev_time = time.time()

            pool = ThreadPool(processes=4)
            rune_img = pool.apply_async(get_runes, args=(args[1], args[0]))

            build_url = f'https://na.op.gg/champions/{args[0]}/{args[1]}/build'
            build = ''

            if requests.get(build_url).status_code != 500:
                await ctx.send(f'Lane: {args[0].capitalize()}')
                await ctx.send(f'Champ: {args[1].capitalize()}')

                '''
                Loads items from OP.GG
                '''
                with urllib.request.urlopen(build_url) as url:
                    data = json.loads(url.read().decode())
                    for num in range(1, 6):
                        build += f'Build {num}: '
                        for item in data[f'build_{num}']:
                            build += (item.lstrip("(\"\'")) + ', '
                        build += '\n'
                        build = re.sub(r'(,)[\s]$', '', build)
                await ctx.send(build)

                '''
                Sends runes from OP.GG
                '''
                with io.BytesIO() as image_binary:
                    rune_img.get().save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(
                        file=discord.File(
                            fp=image_binary,
                            filename=f'{args[1]} runes.png'
                        )
                    )

                '''
                Prints the time taken to compute to the console.
                '''
                print(f"Took approximately {time.time() - prev_time} seconds")
                await ctx.send(f"That took {time.time() - prev_time} seconds")
            else:
                await ctx.send('Spelling Error')

hextechbot.run('OTc1MDk2NzU5MjY3MjM3OTU1.G4nqfj.P8U82ifgIDWiHkuMeUbC5nxtCQt9aGU16IZZpk')    
