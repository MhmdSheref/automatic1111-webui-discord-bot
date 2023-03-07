import os
import requests
import json
import base64
import enum
from modes import modes_list

os.chdir(os.path.dirname(__file__))

index_file = open("index.txt", "r+")
index = int(index_file.readline(-1))

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

try:
    MODELS = json.loads(requests.get("http://localhost:7860/sdapi/v1/sd-models").content)
    SAMPLERS = json.loads(requests.get("http://localhost:7860/sdapi/v1/samplers").content)
except Exception:
    MODELS = [{'title': 'anime\\AbyssOrangeMix3A3.safetensors [d124fc18f0]', 'model_name': 'anime_AbyssOrangeMix3A3', 'hash': 'd124fc18f0', 'sha256': 'd124fc18f0232d7f0a2a70358cdb1288af9e1ee8596200f50f0936be59514f6d', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\anime\\AbyssOrangeMix3A3.safetensors', 'config': None}, {'title': 'anime\\Anything-V3.0-pruned-fp32.ckpt [67a115286b]', 'model_name': 'anime_Anything-V3.0-pruned-fp32', 'hash': '67a115286b', 'sha256': '67a115286b56c086b36e323cfef32d7e3afbe20c750c4386a238a11feb6872f7', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\anime\\Anything-V3.0-pruned-fp32.ckpt', 'config': None}, {'title': 'anime\\pastelmix-better-vae-fp16.ckpt [cfaf882b0a]', 'model_name': 'anime_pastelmix-better-vae-fp16', 'hash': 'cfaf882b0a', 'sha256': 'cfaf882b0a6dc34f392b12e9ee6c35f39ff794a98ef1a132eebd2873be1896ed', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\anime\\pastelmix-better-vae-fp16.ckpt', 'config': None}, {'title': 'base\\sd-V1.4.ckpt [fe4efff1e1]', 'model_name': 'base_sd-V1.4', 'hash': 'fe4efff1e1', 'sha256': 'fe4efff1e174c627256e44ec2991ba279b3816e364b49f9be2abc0b3ff3f8556', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\base\\sd-V1.4.ckpt', 'config': None}, {'title': 'base\\v1-5-pruned-emaonly.ckpt [cc6cb27103]', 'model_name': 'base_v1-5-pruned-emaonly', 'hash': 'cc6cb27103', 'sha256': 'cc6cb27103417325ff94f52b7a5d2dde45a7515b25c255d8e396c90014281516', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\base\\v1-5-pruned-emaonly.ckpt', 'config': None}, {'title': 'base\\v2-1_768-ema-pruned.safetensors [dcd690123c]', 'model_name': 'base_v2-1_768-ema-pruned', 'hash': 'dcd690123c', 'sha256': 'dcd690123cfc64383981a31d955694f6acf2072a80537fdb612c8e58ec87a8ac', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\base\\v2-1_768-ema-pruned.safetensors', 'config': None}, {'title': 'joebro\\joebro_3300_lora.safetensors [86d28bb776]', 'model_name': 'joebro_joebro_3300_lora', 'hash': '86d28bb776', 'sha256': '86d28bb7768322143104e69426805f78ca5a3282a68823657aeb1248e31a044c', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\joebro\\joebro_3300_lora.safetensors', 'config': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\joebro\\joebro_3300_lora.yaml'}, {'title': 'niche\\openjourneyAka_v1.ckpt [5d5ad06cc2]', 'model_name': 'niche_openjourneyAka_v1', 'hash': '5d5ad06cc2', 'sha256': '5d5ad06cc24170b32f25f0180a357e315848000c5f400ffda350e59142fabd68', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\niche\\openjourneyAka_v1.ckpt', 'config': None}, {'title': 'niche\\samdoesartsUltmerge_v1.ckpt', 'model_name': 'niche_samdoesartsUltmerge_v1', 'hash': None, 'sha256': None, 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\niche\\samdoesartsUltmerge_v1.ckpt', 'config': None}, {'title': 'outdated\\NAI-anime-sfw.ckpt [22fa233c2d]', 'model_name': 'outdated_NAI-anime-sfw', 'hash': '22fa233c2d', 'sha256': '22fa233c2dfd7748d534be603345cb9abf994a23244dfdfc1013f4f90322feca', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\outdated\\NAI-anime-sfw.ckpt', 'config': None}, {'title': 'outdated\\waifumodel-V1.3-07.ckpt [99c1061162]', 'model_name': 'outdated_waifumodel-V1.3-07', 'hash': '99c1061162', 'sha256': '99c1061162c126c59d17cfddaf8b475935a9f0a504f7b305b1d733e7618be82b', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\outdated\\waifumodel-V1.3-07.ckpt', 'config': None}, {'title': 'realistic\\dreamlike-photoreal-2.0.safetensors [92970aa785]', 'model_name': 'realistic_dreamlike-photoreal-2.0', 'hash': '92970aa785', 'sha256': '92970aa785eb76e427847109a8f4ec6abfab36ef941f78d295d323d79f6130c9', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\realistic\\dreamlike-photoreal-2.0.safetensors', 'config': None}, {'title': 'realistic\\illuminatiDiffusionV1_v11.safetensors [cae1bee30e]', 'model_name': 'realistic_illuminatiDiffusionV1_v11', 'hash': 'cae1bee30e', 'sha256': 'cae1bee30e67339dd931925f98c12d2b86fe9f4786795137040e4956f4bfcffe', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\realistic\\illuminatiDiffusionV1_v11.safetensors', 'config': None}, {'title': 'training fun\\Ageha 1.5v_3300_lora.safetensors', 'model_name': 'training fun_Ageha 1.5v_3300_lora', 'hash': None, 'sha256': None, 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Ageha 1.5v_3300_lora.safetensors', 'config': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Ageha 1.5v_3300_lora.yaml'}, {'title': 'training fun\\Ageha Diffusion_3300_lora.ckpt', 'model_name': 'training fun_Ageha Diffusion_3300_lora', 'hash': None, 'sha256': None, 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Ageha Diffusion_3300_lora.ckpt', 'config': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Ageha Diffusion_3300_lora.yaml'}, {'title': 'training fun\\Kana Diffusion_3900_lora.safetensors', 'model_name': 'training fun_Kana Diffusion_3900_lora', 'hash': None, 'sha256': None, 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Kana Diffusion_3900_lora.safetensors', 'config': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Kana Diffusion_3900_lora.yaml'}, {'title': 'training fun\\Kana Mix - V3.safetensors', 'model_name': 'training fun_Kana Mix - V3', 'hash': None, 'sha256': None, 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Kana Mix - V3.safetensors', 'config': None}, {'title': 'training fun\\Kana Mix.safetensors', 'model_name': 'training fun_Kana Mix', 'hash': None, 'sha256': None, 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Kana Mix.safetensors', 'config': None}, {'title': 'training fun\\Kanna_Diffusion_v2_3900_lora.safetensors', 'model_name': 'training fun_Kanna_Diffusion_v2_3900_lora', 'hash': None, 'sha256': None, 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Kanna_Diffusion_v2_3900_lora.safetensors', 'config': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\Kanna_Diffusion_v2_3900_lora.yaml'}, {'title': 'training fun\\mohamed.ckpt [c524974cc7]', 'model_name': 'training fun_mohamed', 'hash': 'c524974cc7', 'sha256': 'c524974cc7563b920319edbbe42d5b997e654db0ea7d32fcfb4051d3b98c24b2', 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\mohamed.ckpt', 'config': None}, {'title': 'training fun\\YamiKawaii_8331_lora.ckpt', 'model_name': 'training fun_YamiKawaii_8331_lora', 'hash': None, 'sha256': None, 'filename': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\YamiKawaii_8331_lora.ckpt', 'config': 'D:\\StableDiffusion\\atomatic1111\\stable-diffusion-webui\\models\\Stable-diffusion\\training fun\\YamiKawaii_8331_lora.yaml'}]
    SAMPLERS = [{'name': 'Euler a', 'aliases': ['k_euler_a', 'k_euler_ancestral'], 'options': {}}, {'name': 'Euler', 'aliases': ['k_euler'], 'options': {}}, {'name': 'LMS', 'aliases': ['k_lms'], 'options': {}}, {'name': 'Heun', 'aliases': ['k_heun'], 'options': {}}, {'name': 'DPM2', 'aliases': ['k_dpm_2'], 'options': {'discard_next_to_last_sigma': 'True'}}, {'name': 'DPM2 a', 'aliases': ['k_dpm_2_a'], 'options': {'discard_next_to_last_sigma': 'True'}}, {'name': 'DPM++ 2S a', 'aliases': ['k_dpmpp_2s_a'], 'options': {}}, {'name': 'DPM++ 2M', 'aliases': ['k_dpmpp_2m'], 'options': {}}, {'name': 'DPM++ SDE', 'aliases': ['k_dpmpp_sde'], 'options': {}}, {'name': 'DPM fast', 'aliases': ['k_dpm_fast'], 'options': {}}, {'name': 'DPM adaptive', 'aliases': ['k_dpm_ad'], 'options': {}}, {'name': 'LMS Karras', 'aliases': ['k_lms_ka'], 'options': {'scheduler': 'karras'}}, {'name': 'DPM2 Karras', 'aliases': ['k_dpm_2_ka'], 'options': {'scheduler': 'karras', 'discard_next_to_last_sigma': 'True'}}, {'name': 'DPM2 a Karras', 'aliases': ['k_dpm_2_a_ka'], 'options': {'scheduler': 'karras', 'discard_next_to_last_sigma': 'True'}}, {'name': 'DPM++ 2S a Karras', 'aliases': ['k_dpmpp_2s_a_ka'], 'options': {'scheduler': 'karras'}}, {'name': 'DPM++ 2M Karras', 'aliases': ['k_dpmpp_2m_ka'], 'options': {'scheduler': 'karras'}}, {'name': 'DPM++ SDE Karras', 'aliases': ['k_dpmpp_sde_ka'], 'options': {'scheduler': 'karras'}}, {'name': 'DDIM', 'aliases': [], 'options': {}}, {'name': 'PLMS', 'aliases': [], 'options': {}}]
    print("Offline Mode")


model_list = {}
for i, model in enumerate(MODELS):
    model_list[model["title"]] = i

model_list = enum.Enum("model_list", model_list)


sampler_list = {}
for i, sample in enumerate(SAMPLERS):
    sampler_list[sample["name"]] = i

sampler_list = enum.Enum("sampler_list", sampler_list)


Modes = enum.Enum("Modes", list(modes_list.keys()) + ["base"])

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
