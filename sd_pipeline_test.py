from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    revision="fp16",
    dtype=torch.float16
)

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)

img = pipe("A minimal glowing marketing poster for wireless earbuds, bold typography, luxury lighting").images[0]
img.save("sd_local_test.png")

print(f"✅ Image generated successfully on {device} and saved as sd_local_test.png")
