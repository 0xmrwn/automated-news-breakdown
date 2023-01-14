import datetime
import logging
import os

import openai
import requests

logging.basicConfig(
    level=logging.INFO,
    format=f'[%(asctime)s] [%(process)d] [%(levelname)s] [{os.path.basename(__file__).split(".")[0]}] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S %z",
)


def create_file_name(item: str, file_type: str):
    """
    Creates a file name in the format `./output/{item}_{datetime}.{file_type}`
    using the current date and time.
    """
    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    return f"./output/{item}_{date_time_str}.{file_type}"


def generate_image(input_text: str, config: dict):
    """
    Generates an image based on a given input text using the OpenAI API.
    The generated image is saved to a file in the `output` directory.
    """
    openai.api_key = os.environ["OPENAI_API_KEY"]
    context_len = len(input_text.split())
    logging.info(f"Generating image with {context_len} tokens in instructions")
    dimensions = config["image_size"]
    response = openai.Image.create(prompt=input_text, n=1, size=dimensions)
    image_url = response["data"][0]["url"]
    image_file_name = create_file_name(item="image", file_type="jpeg")
    with open(image_file_name, "wb") as file:
        response = requests.get(image_url)
        file.write(response.content)
    return image_url
