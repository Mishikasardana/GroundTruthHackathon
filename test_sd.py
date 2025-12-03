import requests
from PIL import Image
import io

prompt = "Luxury tech ad poster design for wireless earbuds, bold typography, neon glow, 4k quality"
prompt_url = prompt.replace(" ", "%20")

url = f"https://image.pollinations.ai/prompt/{prompt_url}"

response = requests.get(url)
img = Image.open(io.BytesIO(response.content))
img.save("pollinations_test.png")

print("✅ Image generated and saved as pollinations_test.png")
