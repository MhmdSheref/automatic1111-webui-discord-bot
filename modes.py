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

    "midjourney": {
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
    },

    "illustrationV2": {
        "prompt_prefix": ["", ""],
        "negative_prompt": "nartfixer nfixer nrealfixer",
        "steps": 20,
        "sampler": "Euler a",
        "cfg_scale": 3.0,
        "seed": -1,
        "width": 512,
        "height": 768,
        "sd_model": r"realistic\illuminatiDiffusionV1_v11.safetensors [cae1bee30e]",
        "clip_skip": 1,
    },
}