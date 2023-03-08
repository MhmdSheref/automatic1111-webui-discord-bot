import discord
import time
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
    
    # await interaction.response.defer()
    await interaction.followup.send("Your command is being processed by the server...")
    params = sd.PARAMS.copy()
    if mode.name != "base":
        params = sd.apply_params(params, True, *sd.modes_list[mode.name].values())
    params = sd.apply_params(params, False, prompt, negative_prompt, steps, sampler.name if sampler is not None else None, cfg_scale, seed, width, height, sd_model.name if sd_model is not None else None, clip_skip)
    print(f"Generating an image for user {interaction.user} using slash...")
    sd_thread = threading.Thread(target=sd.make_image, args=(params,))
    sd_thread.start()
    while not sd.returns:
        progress = int(sd.check_progress() * 100)
        if progress == 0:
            await interaction.edit_original_response(content=progress_bar.bar(100) + " Uploading... ")
            break
        elif progress == 1:
            await interaction.edit_original_response(content=progress_bar.bar(0) + " Initializing model...")
        else:
            await interaction.edit_original_response(content=progress_bar.bar(progress) + " " + str(progress) + "%")
        time.sleep(0.1)
    sd_thread.join()
    [image, info] = sd.returns
    sd.returns = []
    # print(main.join())
    # except Exception as e:
    #     await interaction.edit_original_response(content="There was an error with your request, please try again...")
    #     print(e)
    if image == "Error":
        await interaction.edit_original_response(content="There was an error with your request, please try again...")
        return
    await interaction.edit_original_response(content=info, attachments=[discord.File(image)])


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
        params = sd.parse_input(message.content)
        (image, info) = sd.make_image(params)
        await message.channel.send(info, file=discord.File(image))
        print(f"Generating an image for user {message.author} using prefix...")

client.run(TOKEN)
