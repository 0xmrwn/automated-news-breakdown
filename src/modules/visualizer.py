import base64
import os

import openai
import requests
from dotenv import load_dotenv


def generate_image(input_text):
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.Image.create(prompt=input_text, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    with open(os.path.join(".", "output", "image.jpeg"), "wb") as file:
        response = requests.get(image_url)
        file.write(response.content)


def encode_image():
    with open("./output/image.jpeg", "rb") as f:
        image_data = f.read()
        return base64.b64encode(image_data)
