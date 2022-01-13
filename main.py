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
if not os.path.exists('Log'):
    os.mkdir('Log')
handler = logging.FileHandler(filename='Log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="nm!", help_command=None)
help_zh_tw = load_command.read_description("help/zh-tw.txt")
add_zh_tw = load_command.read_description("add/zh-tw.txt")
bot.remove_command("help")

'''
def check_meal(food):
    if food not in ["breakfast", "lunch", "dinner"]:
        return False
'''


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


# 如果包含 dinner，機器人回傳 dinner list
@bot.command(Name="help")
async def help(ctx):
    await ctx.send(help_zh_tw)


@bot.command(Name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command(Name="sl")
async def sl(ctx):
    await ctx.send("Social Credit 👎\n"
                   "https://www.idlememe.com/wp-content/uploads/2021/10/social-credit-meme-idlememe.jpg")


@bot.command(Name="add")
async def add(ctx, *args):
    meal_list = list(args)
    server_id = ctx.message.guild.id
    print(server_id)
    try:
        if args[0] not in ["breakfast", "lunch", "dinner"]:
            await ctx.send(add_zh_tw)
            print("Error 01")
        elif args[1] is type(None):
            await ctx.send(add_zh_tw)
            print("Error 02")
        elif os.path.exists('db/{}.json'.format(server_id)):
            with open('db/{}.json'.format(server_id), 'r') as f:
                data = json.load(f)
                del meal_list[0]
                print(data)
                for meal in meal_list:
                    data[args[0]].append(meal)
                # TODO: Remove Duplicate
                print(args[0])
                print(meal_list)
                print(data)
                json.dump(data, open('db/{}.json'.format(server_id), 'w'), indent=4)
        else:
            with open('db/{}.json'.format(server_id), 'w') as f:
                del meal_list[0]
                add_meal = {
                    args[0]: meal_list
                }
                json.dump(add_meal, f, indent=4)
                print("Warning 01")
        await ctx.send('{} foods add into database'.format(len(args) - 1))
    except IndexError:
        await ctx.send(add_zh_tw)
        print("Error 03")

if not os.path.exists("token.json"):
    print("No token detected\n"
          "please input your token from https://discord.com/developers/applications")
    token_json = input()
    with open("token.json", "w") as f:
        token_dump = {
            "token": token_json
        }
        json.dump(token_dump, f, indent=4)
with open("token.json", "r") as f:
    token = json.load(f)
bot.run(token["token"])
