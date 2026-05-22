import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

# ----------------------------
# Load model once
# ----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    safety_checker=None
)

pipe = pipe.to(device)

# ----------------------------
# AI → Human enhancement
# ----------------------------
def make_real(uploaded_image):

    image = Image.open(uploaded_image).convert("RGB")
    image = image.resize((512, 512))

    prompt = (
        "a real human face, ultra realistic, natural skin texture, "
        "professional portrait photography, high detail, 8k"
    )

    result = pipe(
        prompt=prompt,
        image=image,
        strength=0.65,
        guidance_scale=7.5
    ).images[0]

    return result
