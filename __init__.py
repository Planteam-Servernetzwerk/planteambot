import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import requests
import datetime as dt

with open(".token", "r") as f:
    TOKEN = f.read()


SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
FILE_SCHERE = os.path.join(SCRIPT_DIR, "schere.json")
FILE_SAMS = os.path.join(SCRIPT_DIR, "sams.json")


def json_check_file(file: str):
    try:
        with open(file, "r") as f:
            print(f.read())
    except FileNotFoundError:
        with open(file, "w") as f:
            f.write("{}")


json_check_file(FILE_SCHERE)
json_check_file(FILE_SAMS)


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


def json_increment(file: str, key: str) -> int:
    with open(file, "r") as f:
        content = json.loads(f.read())
        if key in content:
            content[key] = content[key] + 1
        else:
            content[key] = 1

    with open(file, "w") as f:
        f.write(json.dumps(content))

    return content[key]


def json_get_count(file: str, key: str) -> int:
    with open(file, "r") as f:
        content = json.load(f)
        if key in content:
            count = content[key]
        else:
            count = 0
    return count


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="schereadd", description="Inkrementiert den Scherecounter für den angegebenen User.")
async def schereadd(interaction: discord.Interaction, user: discord.Member):
    count = json_increment(FILE_SCHERE, user.mention)
    await interaction.response.send_message("<:okak:1336034690380857476>")
    await interaction.channel.send(f"{user.name} hebt die Schere zum {count}. Male!")


@bot.tree.command(name="scherecount", description="Gibt an, wie oft der User bereits die Schere gehoben hat.")
async def scherecount(interaction: discord.Interaction, user: discord.Member):
    count = json_get_count(FILE_SCHERE, user.mention)
    await interaction.response.send_message("<:okak:1336034690380857476>")
    await interaction.channel.send(f"{user.name} hat schon {count} Mal{'e' if count != 1 else ''} die Schere gehoben!")


@bot.tree.command(name="samsadd", description="Inkrementiert den Samsreference-Counter für den angegebenen User.")
async def samsadd(interaction: discord.Interaction, user: discord.Member):
    count = json_increment(FILE_SAMS, user.mention)
    await interaction.response.send_message("<:okak:1336034690380857476>")
    await interaction.channel.send(f"{user.name} bringt zum {count}. Male einen Samsreference!")


@bot.tree.command(name="samscount", description="Gibt an, wie oft der User bereits einen Sams-Reference gebracht hat.")
async def samscount(interaction: discord.Interaction, user: discord.Member):
    count = json_get_count(FILE_SAMS, user.mention)
    await interaction.response.send_message("<:okak:1336034690380857476>")
    await interaction.channel.send(f"{user.name} hat schon {count} Mal{'e' if count != 1 else ''} das Sams zitiert!")


@bot.tree.command(name="metar", description="Wie ist das Wetter?")
async def metar(interaction: discord.Interaction, icao: str):
    response = requests.get(f"https://aviationweather.gov/api/data/metar?ids={icao}&format=raw&taf=true&date={dt.datetime.now().strftime('%Y-%m-%d')}")

    if response.status_code == 200:
        await interaction.response.send_message(f"```METAR {response.text}```")
    else:
        await interaction.response.send_message("Föhler")


bot.run(TOKEN)

