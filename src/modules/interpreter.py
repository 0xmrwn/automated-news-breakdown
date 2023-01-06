import os

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def summarize_text(text):
    prompt = f"""As a brilliant article reviewer, give a short 
    summary in more or less 200 words and give a honest opinion in 
    one sentence about this article : {text}"""
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=250,
        n=1,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    completion = completions.choices[0]
    return completion.text


def generate_prompt(text):
    prompt = f"""Give a creative prompt to be fed to an LLM that generates images.
    Suggest an appropriate art style and general tone of the image. Be safe in your words to avoid triggering
    any safety blocks from the API.The generated image should serve as an illustration of this article : {text}"""
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        temperature=0.1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    completion = completions.choices[0]
    return completion.text


def generate_title(text):
    prompt = f"""Think of an interesting title for this article 
    that will captivate readers : {text}"""
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=30,
        n=1,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    completion = completions.choices[0]
    return completion.text
