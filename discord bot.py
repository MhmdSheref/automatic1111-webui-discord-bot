import enum
import os
import discord
import requests
import json
import base64
from dotenv import load_dotenv

os.chdir(os.path.dirname(__file__))
index_file = open("index.txt", "r+")
index = int(index_file.readline(-1))
load_dotenv()
TOKEN = os.getenv("TOKEN")

TXT2IMG_URL = "http://localhost:7860/sdapi/v1/txt2img"

PNGINFO_URL = "http://localhost:7860/sdapi/v1/png-info"

translate = {
    "steps": "steps",
    "sampler": "sampler_name",
    "cfg scale": "cfg_scale",
    "seed": "seed",
    "size": "size",
    "model": "sd_model_checkpoint",
    "clip skip": "CLIP_stop_at_last_layers",
}


MODELS = json.loads(requests.get("http://localhost:7860/sdapi/v1/sd-models").content)
SAMPLERS = json.loads(requests.get("http://localhost:7860/sdapi/v1/samplers").content)

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

PARAMS = {
    "prompt": "",
    "seed": -1,
    "sampler_name": "DPM++ 2M Karras",
    "steps": 24,
    "cfg_scale": 10.0,
    "width": 512,
    "height": 768,
    "negative_prompt": "bad quality",
    "override_settings": {
      "sd_model_checkpoint": "anime_AbyssOrangeMix3A3",
      "CLIP_stop_at_last_layers": 2,
    },
    "override_settings_restore_afterwards": False,
}


model_list = {}
for i, model in enumerate(MODELS):
    model_list[model["title"]] = i

model_list = enum.Enum("model_list", model_list)


sampler_list = {}
for i, sample in enumerate(SAMPLERS):
    sampler_list[sample["name"]] = i

sampler_list = enum.Enum("sampler_list", sampler_list)

modes_list = {
    "anime": {
        "prompt_prefix": ["masterpiece, best quality, ", ""],
        "negative_prompt": "bad quality, nsfw, nude, lewd",
        "steps": 24,
        "sampler": "DPM++ SDE Karras",
        "cfg_scale": 10.0,
        "seed": -1,
        "width": 512,
        "height": 768,
        "sd_model": r"anime\AbyssOrangeMix3A3.safetensors [d124fc18f0]",
        "clip_skip": 2,
    },

    "pastel": {
        "prompt_prefix": ["masterpiece, best quality, ultra-detailed, illustration, portrait, ", ""],
        "negative_prompt": "lowres, ((bad anatomy)), ((bad hands)), text, missing finger, extra digits, fewer digits, blurry, ((mutated hands and fingers)), (poorly drawn face), ((mutation)), ((deformed face)), (ugly), ((bad proportions)), ((extra limbs)), extra face, (double head), (extra head), ((extra feet)), monster, logo, cropped, worst quality, low quality, normal quality, jpeg, humpbacked, long body, long neck, ((jpeg artifacts))",
        "steps": 20,
        "sampler": "DPM++ 2M Karras",
        "cfg_scale": 7.0,
        "seed": -1,
        "width": 512,
        "height": 768,
        "sd_model": r"anime\pastelmix-better-vae-fp16.ckpt [cfaf882b0a]",
        "clip_skip": 2,
    },

    "realistic": {
        "prompt_prefix": ["high quality photography, ", ", photo realism, ultra - detailed, Canon EOS R3, film, composition, backlit, atmospheric light, volumetric lightning, hyper detailed, intricate details, photorealistic"],
        "negative_prompt": "bad quality, cartoon, blurry, out of frame, duplicate, watermark, signature, text, bokeh",
        "steps": 30,
        "sampler": "Euler a",
        "cfg_scale": 7.5,
        "seed": -1,
        "width": 768,
        "height": 768,
        "sd_model": r"realistic\dreamlike-photoreal-2.0.safetensors [92970aa785]",
        "clip_skip": 2,
    },

    "illustration": {
        "prompt_prefix": ["masterpiece, highly detailed illustration, ", ", made by midjourney"],
        "negative_prompt": "bad quality, low quality, out of frame, duplicate, watermark, signature, text, bokeh",
        "steps": 20,
        "sampler": "Euler a",
        "cfg_scale": 7.5,
        "seed": -1,
        "width": 768,
        "height": 768,
        "sd_model": r"base\v2-1_768-ema-pruned.safetensors [dcd690123c]",
        "clip_skip": 2,
    }
}

Modes = enum.Enum("Modes", list(modes_list.keys()) + ["base"])


def apply_params(params, is_default, *args):
    if params.get("pre_prompt") is None:
        params["pre_prompt"] = ["", ""]
    if is_default:
        params["pre_prompt"] = args[0]
    else:
        params["prompt"] = params["pre_prompt"][0] + args[0] + params["pre_prompt"][1]
        del params["pre_prompt"]
    params["negative_prompt"] = args[1] if args[1] is not None else params["negative_prompt"]
    params["steps"] = args[2] if args[2] is not None else params["steps"]
    params["sampler_name"] = args[3] if args[3] is not None else params["sampler_name"]
    params["cfg_scale"] = args[4] if args[4] is not None else params["cfg_scale"]
    params["seed"] = args[5] if args[5] is not None else params["seed"]
    params["width"] = args[6] if args[6] is not None else params["width"]
    params["height"] = args[7] if args[7] is not None else params["height"]
    params["override_settings"]["sd_model_checkpoint"] = args[8] if args[8] is not None else params["override_settings"]["sd_model_checkpoint"]
    params["override_settings"]["CLIP_stop_at_last_layers"] = args[9] if args[9] is not None else params["override_settings"]["CLIP_stop_at_last_layers"]
    return params


def parse_input(message_txt: str):
    params = PARAMS.copy()
    message_txt = message_txt.removeprefix("%sd ")
    message_txt = message_txt.split("|")
    params["prompt"] = message_txt[0]
    if len(message_txt) == 1:
        return params
    params["negative_prompt"] = message_txt[1]
    if len(message_txt) == 2:
        return params
    settings = message_txt[2]
    settings = settings.split(",")
    for setting in settings:
        setting = setting.strip()
        setting = setting.split(":")
        setting[0] = setting[0].strip().lower()
        setting[1] = setting[1].strip()
        setting[0] = translate.get(setting[0])
        if "size" in setting[0]:
            size = setting[1].split("x")
            params["width"] = int(size[0])
            params["height"] = int(size[1])
            continue
        if setting[0] == ("sd_model_checkpoint" or "CLIP_stop_at_last_layers"):
            params["override_settings"][setting[0]] = setting[1]
            continue
        params[setting[0]] = setting[1]
    return params


def make_image(params):
    global index, index_file
    index += 1
    created_image = requests.post(url=TXT2IMG_URL, data=json.dumps(params)).content
    created_image = json.loads(created_image)
    created_image = created_image["images"][0]
    image_data = requests.post(url=PNGINFO_URL, data=json.dumps({"image": created_image})).content
    image_data = json.loads(image_data)["info"]
    created_image = base64.b64decode(created_image)
    image_file = open(f"images/image{index}.png", "wb")
    image_file.write(created_image)
    index_file.seek(0)
    index_file.write(str(index))
    index_file.truncate()
    return f"images/image{index}.png", image_data


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
    except Exception as e:
        await interaction.followup.send("There was an error with your request, please try again...")
    else:
        await interaction.followup.send(info, file=discord.File(image))


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
