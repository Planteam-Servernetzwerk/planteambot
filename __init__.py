import discord
from discord import app_commands
from discord.ext import commands
import json
import os

with open(".token", "r") as f:
    TOKEN = f.read()


SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
FILE_SCHERE = os.path.join(SCRIPT_DIR, "schere.json")


try:
    with open(FILE_SCHERE, "r") as f:
        print(f.read())
except FileNotFoundError:
    with open(FILE_SCHERE, "w") as f:
        f.write("{}")


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="schereadd", description="Inkrementiert den Scherecounter für den angegebenen User.")
async def schereadd(interaction: discord.Interaction, user: discord.Member):
    with open(FILE_SCHERE, "r") as f:
        content = json.loads(f.read())
        if user.mention in content:
            content[user.mention] = content[user.mention] + 1
        else:
            content[user.mention] = 1

    print(content)

    with open(FILE_SCHERE, "w") as f:
        f.write(json.dumps(content))

    await interaction.response.send_message("<:okak:1336034690380857476>")
    await interaction.channel.send(f"{user.name} hebt die Schere zum {content[user.mention]}. Male!")


@bot.tree.command(name="scherecount", description="Gibt an, wie oft der User bereits die Schere gehoben hat.")
async def scherecount(interaction: discord.Interaction, user: discord.Member):
    with open(FILE_SCHERE, "r") as f:
        content = json.load(f)
        if user.mention in content:
            count = content[user.mention]
        else:
            count = 0
    await interaction.response.send_message("<:okak:1336034690380857476>")
    await interaction.channel.send(f"{user.name} hat {count} Mal{'e' if count != 1 else ''} die Schere gehoben!")


bot.run(TOKEN)

