import os

import openai
import requests
from dotenv import load_dotenv

# Replace YOUR_API_KEY with your actual API key
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_image(input_text):
    response = openai.Image.create(prompt=input_text, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    with open(os.path.join(".", "output", "image.jpeg"), "wb") as file:
        response = requests.get(image_url)
        file.write(response.content)
