# discord bot
import os
import random
import asyncio
import time
import json
import logging
import load_command
from load_command import *

import discord
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='Log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="nm!", help_command=None)
help_zh_tw = load_command.help_zh_tw_def()



# 調用 event 函式庫
@bot.event
# 當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', bot.user)
    game = discord.Game('nm!help')
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.online, activity=game)


'''
@client.event

async def status():
    game1 = discord.Game('吃拉麵')
    game2 = discord.Game('吃咖哩')
    game3 = discord.Game('吃壽司')
    game4 = discord.Game('吃火鍋')
    game5 = discord.Game('吃麵包')

    async def game_status():
        await client.change_presence(activity=game1)
        await asyncio.sleep(5)
        await client.change_presence(activity=game2)
        await asyncio.sleep(5)
        await client.change_presence(activity=game3)
        await asyncio.sleep(5)
        await client.change_presence(activity=game4)
        await asyncio.sleep(5)
        await client.change_presence(activity=game5)
        await asyncio.sleep(5)

    await game_status()

    await status()
'''

'''
@bot.event
# 當有訊息時
async def on_message(message):
    # 排除自己的訊息，避免陷入無限循環
    if message.author == bot.user:
        return
    # 如果包含 ping，機器人回傳 pong



    if message.content == 'nm!ping':
        await message.channel.send()
        print(f'Message from {message.author}: {message.content}')

# 如果包含 help，機器人回傳 help



    if message.content == 'nm!help':
        await message.channel.send(help_zh_tw)
        print(f'Message from {message.author}: {message.content}')
'''


# 如果包含 dinner，機器人回傳 dinner list


@bot.command
async def help(ctx):
    await ctx.send(help_zh_tw)


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


with open("token.json", "r") as f:
    token = json.load(f)
token = token["token"]
bot.run(token)
