import os
import random
# import asyncio
from datetime import datetime
import json
import logging

import load_command

import discord
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
if not os.path.exists('Log'):
    os.mkdir('Log')
if not os.path.exists('db'):
    os.mkdir('db')
handler = logging.FileHandler(filename='Log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if not os.path.exists("token.json"):
    print("No token detected\n"
          "please input your token from https://discord.com/developers/applications:")
    token_json = input()
    print("Please input your user id:")
    user_id = input()
    print("Please input your bot prefix:")
    prefix = input()
    with open("token.json", "w") as f:
        token_dump = {
            "token": token_json,
            "owner": user_id,
            "prefix": prefix
        }
        json.dump(token_dump, f, indent=4)
with open("token.json", "r") as f:
    token = json.load(f)

bot = commands.Bot(command_prefix=token["prefix"], help_command=None)

help_zh_tw = load_command.read_description("help", "zh-tw")
add_zh_tw = load_command.read_description("add", "zh-tw")
remove_zh_tw = load_command.read_description("remove", "zh-tw")
list_zh_tw = load_command.read_description("list", "zh-tw")
random_zh_tw = load_command.read_description("random", "zh-tw")

bot.remove_command("help")


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
    try:
        server_id = str(ctx.message.guild.id)
    except:
        server_id = "user_" + str(ctx.message.author.id)
    print(server_id)
    try:
        if args[0] not in ["breakfast", "lunch", "dinner"]:
            await ctx.send(add_zh_tw)
            print("Error 01")
            # Check args is correct
        elif args[1] is type(None):
            await ctx.send(add_zh_tw)
            print("Error 02")
            # Check add data exists
        elif os.path.exists('db/{}.json'.format(server_id)):
            # Check json exists
            with open('db/{}.json'.format(server_id), 'r') as f:
                data = json.load(f)
                del meal_list[0]
                # del args[0] from meal_list
                before_del = len(meal_list)
                try:
                    print(f"data in {args[0]} is {data[args[0]]}")
                except KeyError:
                    data[args[0]] = []
                # Check Key exists
                print(f"data is {data}")
                del_list = []
                for i in range(len(data[args[0]])):
                    print(f"i is {i}")
                    for j in range(len(meal_list)):
                        print(f"j is {j}")
                        if data[args[0]][i] == meal_list[j]:
                            del_list.append(meal_list[j])
                # Add duplicate to del_list to delete
                print(del_list)
                for k in range(len(del_list)):
                    meal_list.remove(del_list[k])
                # Cleanup duplicate meal_list
                for meal in meal_list:
                    data[args[0]].append(meal)
                # Append meal_list to data
                after_del = len(meal_list)
                print(args[0])
                print(meal_list)
                print(data)
                duplicate_len = before_del - after_del
                json.dump(data, open('db/{}.json'.format(server_id), 'w'), indent=4)
                # Save data to json
        else:
            with open('db/{}.json'.format(server_id), 'w') as f:
                del meal_list[0]
                add_meal = {
                    args[0]: meal_list
                }
                json.dump(add_meal, f, indent=4)
                # Add new json to db
                print("Warning 01")
        if len(meal_list) == 0:
            await ctx.send(f"0 food added to {args[0]}")
        elif len(meal_list) >= 2:
            await ctx.send('{} foods add into {} ({} duplicate)'.format(len(meal_list), args[0], duplicate_len))
        elif len(meal_list) == 1:
            await ctx.send('{} food add into {} ({} duplicate)'.format(len(meal_list), args[0], duplicate_len))
    except IndexError:
        await ctx.send(add_zh_tw)
        print("Error 03")
    # If no args given


@bot.command(Name="remove")
async def remove(ctx, *args):
    del_list = list(args)
    try:
        server_id = str(ctx.message.guild.id)
    except:
        server_id = "user_" + str(ctx.message.author.id)
    print(server_id)
    try:
        if args[0] not in ["breakfast", "lunch", "dinner"]:
            await ctx.send(remove_zh_tw)
            print("Error 01")
            # Check args is correct
        elif args[1] is type(None):
            await ctx.send(remove_zh_tw)
            print("Error 02")
            # Check remove data exists
        elif os.path.exists('db/{}.json'.format(server_id)):
            # Check json exists
            with open('db/{}.json'.format(server_id), 'r') as f:
                data = json.load(f)
                del del_list[0]
                # del args[0] from del_list
                before_del = len(del_list)
                try:
                    print(f"data in {args[0]} is {data[args[0]]}")
                except KeyError:
                    data[args[0]] = []
                # Check Key exists
                del_key = []
                print(f"data is {data}")
                for i in range(len(data[args[0]])):
                    for j in range(len(del_list)):
                        if data[args[0]][i] == del_list[j]:
                            del_key.append(del_list[j])
                # Cleanup duplicate meal_list
                print(del_list)
                for k in range(len(del_key)):
                    data[args[0]].remove(del_key[k])
                # Remove del_list to data
                after_del = len(del_key)
                wrong_data = before_del - after_del
                json.dump(data, open('db/{}.json'.format(server_id), 'w'), indent=4)
                # Save data to json
        else:
            with open('db/{}.json'.format(server_id), 'w') as f:
                json.dump({}, f, indent=4)
                # Add new json to db
                await ctx.send(f"No food in {args[0]}")
                print("Warning 01")
    except IndexError:
        await ctx.send(remove_zh_tw)
        print("Error 03")
    if len(del_key) == 0:
        await ctx.send(f"0 food deleted from {args[0]}")
    elif len(del_key) >= 2:
        await ctx.send('{} foods deleted from {} ({} not found)'.format(len(del_key), args[0], wrong_data))
    elif len(del_key) == 1:
        await ctx.send('{} food deleted from {} ({} duplicate)'.format(len(del_key), args[0], wrong_data))


@bot.command(Name="show")
async def show(ctx, *args):
    try:
        server_id = str(ctx.message.guild.id)
    except:
        server_id = "user_" + str(ctx.message.author.id)
    print(server_id)
    try:
        if args[0] not in ["breakfast", "lunch", "dinner"]:
            await ctx.send(list_zh_tw)
            print("Error 01")
            # Check args is correct
        elif os.path.exists('db/{}.json'.format(server_id)):
            # Check json exists
            with open('db/{}.json'.format(server_id), 'r') as f:
                data = json.load(f)
                # Load json to data
            try:
                print(data[args[0]])
            except KeyError:
                await ctx.send(f"No food in {args[0]}")
            else:
                if len(data[args[0]]) == 0:
                    await ctx.send(f"No food in {args[0]}")
                else:
                    str_data = ", ".join(data[args[0]])
                    await ctx.send(f"{args[0]} list: {str_data}")
        else:
            with open('db/{}.json'.format(server_id), 'w') as f:
                json.dump({}, f, indent=4)
                await ctx.send(f"No food in {args[0]}")
                print("Warning 01")
    except IndexError:
        if os.path.exists('db/{}.json'.format(server_id)):
            with open('db/{}.json'.format(server_id), 'r') as f:
                data = json.load(f)
                # Load json to data
            if len(data) == 0:
                await ctx.send('No food in any list')
            else:
                try:
                    breakfast = data['breakfast']
                except KeyError:
                    breakfast = []
                try:
                    lunch = data['lunch']
                except KeyError:
                    lunch = []
                try:
                    dinner = data['dinner']
                except KeyError:
                    dinner = []
                breakfast = ", ".join(breakfast)
                lunch = ", ".join(lunch)
                dinner = ", ".join(dinner)
                await ctx.send(f"breakfast list: {breakfast}\n"
                               f"lunch list: {lunch}\n"
                               f"dinner list: {dinner}")
        else:
            with open('db/{}.json'.format(server_id), 'w') as f:
                json.dump({}, f, indent=4)
                await ctx.send('No food in any list')
        print("Error 03")


@bot.command(Name="lists")
async def lists(ctx, *args):
    try:
        server_id = str(ctx.message.guild.id)
    except:
        server_id = "user_" + str(ctx.message.author.id)
    print(server_id)
    try:
        if args[0] not in ["breakfast", "lunch", "dinner"]:
            await ctx.send(list_zh_tw)
            print("Error 01")
            # Check args is correct
        elif os.path.exists('db/{}.json'.format(server_id)):
            # Check json exists
            with open('db/{}.json'.format(server_id), 'r') as f:
                data = json.load(f)
                # Load json to data
            try:
                print(data[args[0]])
            except KeyError:
                await ctx.send(f"No food in {args[0]}")
            else:
                if len(data[args[0]]) == 0:
                    await ctx.send(f"No food in {args[0]}")
                else:
                    str_data = ", ".join(data[args[0]])
                    await ctx.send(f"{args[0]} list: {str_data}")
        else:
            with open('db/{}.json'.format(server_id), 'w') as f:
                json.dump({}, f, indent=4)
                await ctx.send(f"No food in {args[0]}")
                print("Warning 01")
    except IndexError:
        if os.path.exists('db/{}.json'.format(server_id)):
            with open('db/{}.json'.format(server_id), 'r') as f:
                data = json.load(f)
                # Load json to data
            if len(data) == 0:
                await ctx.send('No food in any list')
            else:
                try:
                    breakfast = data['breakfast']
                except KeyError:
                    breakfast = []
                try:
                    lunch = data['lunch']
                except KeyError:
                    lunch = []
                try:
                    dinner = data['dinner']
                except KeyError:
                    dinner = []
                breakfast = ", ".join(breakfast)
                lunch = ", ".join(lunch)
                dinner = ", ".join(dinner)
                await ctx.send(f"breakfast list: {breakfast}\n"
                               f"lunch list: {lunch}\n"
                               f"dinner list: {dinner}")
        else:
            with open('db/{}.json'.format(server_id), 'w') as f:
                json.dump({}, f, indent=4)
                await ctx.send('No food in any list')
        print("Error 03")


@bot.command(Name="choose")
async def choose(ctx, *args):
    try:
        server_id = str(ctx.message.guild.id)
    except:
        server_id = "user_" + str(ctx.message.author.id)
    print(server_id)
    try:
        if args[0] not in ["breakfast", "lunch", "dinner"]:
            await ctx.send(random_zh_tw)
            print("Error 01")
            # Check args is correct
        elif os.path.exists('db/{}.json'.format(server_id)):
            # Check json exists
            with open('db/{}.json'.format(server_id), 'r') as f:
                data = json.load(f)
                # Load json to data
            try:
                print(data[args[0]])
            except KeyError:
                await ctx.send(f"No food in {args[0]}")
            else:
                if len(data[args[0]]) == 0:
                    await ctx.send(f"No food in {args[0]}")
                else:
                    random.seed(str(datetime.now()))
                    print(datetime.now())
                    random_food = random.choice(data[args[0]])
                    await ctx.send(f"Random food in {args[0]}: {random_food}")
        else:
            with open('db/{}.json'.format(server_id), 'w') as f:
                json.dump({}, f, indent=4)
                await ctx.send(f"No food in {args[0]}")
                print("Warning 01")
    except IndexError:
        # TODO: Get Time To Auto Choose Type
        current_utc = datetime.utcnow()
        current_utc = current_utc.hour
        if os.path.exists('db/{}.json'.format(server_id)):

            try:
                with open('db/{}.json'.format(server_id), 'r') as f:
                    data = json.load(f)
                # Load json to data
            except KeyError:
                await ctx.send(f'Please use `{token["prefix"]}time` to setup timezone.')
            else:
                current_time = current_utc + data['timezone']
                if current_time in range(5,10):
                    if len(data['breakfast']) == 0:
                        await ctx.send('No food in breakfast')
                    else:
                        random.seed(str(datetime.now()))
                        print(datetime.now())
                        random_food = random.choice(data['breakfast'])
                        await ctx.send(f"Random food in breakfast: {random_food}")
                elif current_time in range(10,15):
                    if len(data['lunch']) == 0:
                        await ctx.send('No food in lunch')
                    else:
                        random.seed(str(datetime.now()))
                        print(datetime.now())
                        random_food = random.choice(data['lunch'])
                        await ctx.send(f"Random food in lunch: {random_food}")
                elif current_time in range(15,17):
                    await ctx.send('Current not support afternoon tea.')
                elif current_time in range(17,22):
                    if len(data['dinner']) == 0:
                        await ctx.send('No food in dinner')
                    else:
                        random.seed(str(datetime.now()))
                        print(datetime.now())
                        random_food = random.choice(data['dinner'])
                        await ctx.send(f"Random food in dinner: {random_food}")
                elif current_time in range(22, 24) or current_time in range(5):
                    await ctx.send('Go to sleep.')
                else:
                    await ctx.send('I don't know how did you trigger this, please contact `@.')

        await ctx.send(random_zh_tw)
        print("Error 03")


@bot.command(Name="shutdown")
async def shutdown(ctx):
    sender = ctx.message.author.id
    with open('token.json', 'r') as f:
        owner = json.load(f)
    owner = owner['owner']
    if sender == owner:
        await ctx.send("Shutting down...")
        await bot.close()


bot.run(token["token"])
