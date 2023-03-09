import asyncio
import time
import discord
import os
import threading
from dotenv import load_dotenv
import sd_link as sd
import progress_bar

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
lock = asyncio.Lock()
@client.event
async def on_ready():
    # await tree.sync()
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
                   mode: sd.Modes,
                   negative_prompt: str = None,
                   steps: int = None,
                   sampler: sd.sampler_list = None,
                   cfg_scale: float = None,
                   seed: int = None,
                   width: int = None,
                   height: int = None,
                   sd_model: sd.model_list = None,
                   clip_skip: int = None,
                   ):
    await interaction.followup.send("Your image is in queue...")
    global lock
    async with lock:
        await interaction.edit_original_response(content="Your image is being processed by the server...")
        params = sd.PARAMS.copy()
        if mode.name != "base":
            params = sd.apply_params(params, True, *sd.modes_list[mode.name].values())
        params = sd.apply_params(params, False, prompt, negative_prompt, steps, sampler.name if sampler is not None else None, cfg_scale, seed, width, height, sd_model.name if sd_model is not None else None, clip_skip)
        print(f"Generating an image for user {interaction.user} using slash...")
        sd_thread = threading.Thread(target=sd.make_image, args=(params,))
        sd_thread.start()
        while not sd.returns:
            time.sleep(0.1)
            progress = int(sd.check_progress() * 100)
            if progress == 0:
                await interaction.edit_original_response(content=progress_bar.bar(100) + " Uploading... ")
                break
            elif progress == 1:
                await interaction.edit_original_response(content=progress_bar.bar(0) + " Initializing model...")
            else:
                await interaction.edit_original_response(content=progress_bar.bar(progress) + " " + str(progress) + "%")
        sd_thread.join()
        [image, info] = sd.returns
        sd.returns = []

    if image == "Error":
        await interaction.edit_original_response(content="There was an error with your request, please try again...")
        return
    await interaction.edit_original_response(content=info, attachments=[discord.File(image)])


@tree.command(name="kill", description="ADMIN ONLY")
async def kill(interaction: discord.Interaction):
    await interaction.response.defer()

    if interaction.user.id == 324519572806041600:
        await interaction.followup.send("The bot has been killed")
        await quit()
    else:
        await interaction.followup.send("You dont have access to this command")


@tree.command(name="chat", description="Talk to chatGPT.")
async def chat(interaction, message: str, clear: bool = False):
    # To sync with the botshard bot
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
        params = sd.parse_input(message.content)
        (image, info) = sd.make_image(params)
        await message.channel.send(info, file=discord.File(image))
        print(f"Generating an image for user {message.author} using prefix...")


client.run(TOKEN)
