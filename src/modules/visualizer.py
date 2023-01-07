import os

import openai
import requests

from src.modules.utils import create_file_name


def generate_image(input_text):
    """
    Generates an image based on a given input text using the OpenAI API.
    The generated image is saved to a file in the `output` directory.
    """
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.Image.create(prompt=input_text, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    image_file_name = create_file_name(item="image", file_type="jpeg")
    with open(image_file_name, "wb") as file:
        response = requests.get(image_url)
        file.write(response.content)
    return image_url
