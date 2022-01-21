# 導入Discord.py
import discord
import json

# client是我們與Discord連結的橋樑
client = discord.Client()

with open("token.json", "r") as f:
    token = json.load(f)


# 調用event函式庫
@client.event
# 當機器人完成啟動時
async def on_ready():
    print("目前登入身份：", client.user)


@client.event
# 當有訊息時
async def on_message(message):
    # 排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    # 如果以「說」開頭
    if message.content.startswith("nm!"):
        try:
            await message.channel.send(
                "Current is in debug mode.\n"
                "All content won't be save now.\n"
                "Please don't use."
            )
        except:
            await message.author.send(
                "Current is in debug mode.\n"
                "All content won't be save now.\n"
                "Please don't use."
            )


client.run(token["token"])  # TOKEN在剛剛Discord Developer那邊「BOT」頁面裡面
