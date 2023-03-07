import os
import discord
from dotenv import load_dotenv
from sd_link import *

load_dotenv()
TOKEN = os.getenv("TOKEN")

HELP = """put your prompt right after %sd
After your prompt, seperated by a "|" you can include: (default values included)
```
Negative prompt: bad quality,
Steps: 24,
Sampler: DPM++ 2M Karras,
CFG scale: 10,
Seed: -1,
Size: 512x768,
Model: anime_AbyssOrangeMix3A3,
Clip skip: 2,
```
don't forget the commas
sample input: Masterpiece, best quality, anime girl | bad quality | Steps: 69, Sampler: Euler a, Size: 512x960
I dont have any checks to actually see if your values break anything so please be gentle, senpai~
"""


intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('Bot is Online!'))


@tree.command(name="help", description="get Help.")
async def help_command(interaction):
    # await interaction.response.defer()
    await interaction.followup.send(HELP)
    print(f"{interaction.user} requested the help using slash command...")


@tree.command(name="create", description="Create an image.")
async def generate(interaction: discord.Interaction,
                   prompt: str,
                   mode: Modes,
                   negative_prompt: str = None,
                   steps: int = None,
                   sampler: sampler_list = None,
                   cfg_scale: float = None,
                   seed: int = None,
                   width: int = None,
                   height: int = None,
                   sd_model: model_list = None,
                   clip_skip: int = None,
                   ):
    
    # await interaction.response.defer()
    # await interaction.followup.send("Your command is being processed by the server...")
    params = PARAMS.copy()
    if mode.name != "base":
        params = apply_params(params, True, *modes_list[mode.name].values())
    params = apply_params(params, False, prompt, negative_prompt, steps, sampler.name if sampler is not None else None, cfg_scale, seed, width, height, sd_model.name if sd_model is not None else None, clip_skip)
    print(f"Generating an image for user {interaction.user} using slash...")
    try:
        (image, info) = make_image(params)
    except Exception:
        await interaction.followup.send("There was an error with your request, please try again...")
    else:
        await interaction.followup.send(info, file=discord.File(image))


# To sync with the botshard bot
@tree.command(name="chat", description="Talk to chatGPT.")
async def chat(interaction, message: str, clear: bool = False):
    pass


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content.startswith("%sd help"):
        await message.channel.send(HELP)
        print("help command")
        return
    if message.content.startswith('%sd '):
        await message.channel.send("Creating your image...")
        params = parse_input(message.content)
        (image, info) = make_image(params)
        await message.channel.send(info, file=discord.File(image))
        print(f"Generating an image for user {message.author} using prefix...")

client.run(TOKEN)
