# discord bot
import discord
import os
import random
import asyncio
import time
import json

client = discord.Client()


# 調用 event 函式庫
@client.event
# 當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)
    game = discord.Game('nm!help')
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await client.change_presence(status=discord.Status.online, activity=game)


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


@client.event
# 當有訊息時
async def on_message(message):
    # 排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    # 如果包含 ping，機器人回傳 pong
    if message.content == 'nm!ping':
        await message.channel.send('pong')
        print(f'Message from {message.author}: {message.content}')
    # 如果包含 help，機器人回傳 help
    if message.content == 'nm!help':
        await message.channel.send('我甚麼都不會...')
        print(f'Message from {message.author}: {message.content}')
    # 如果包含 dinner，機器人回傳 dinner list


with open("token.json", "r") as f:
    token = json.load(f)
token = token["token"]
client.run(token)
