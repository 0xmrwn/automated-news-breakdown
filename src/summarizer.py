import os

import openai
from dotenv import load_dotenv

load_dotenv()

# Replace YOUR_API_KEY with your actual API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize(text, context=None):
    # Use the OpenAI API to generate a summary of the text
    prompt = (
        f"Please summarize the following text in approximately 200 words:\n\n{text}"
    )
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        temperature=0.7,
        stop="\n",
        presence=context,
    )
    return completions.choices[0].text


def generate_response(text, context=None):
    # Use the OpenAI API to generate a response to the text

    prompt = text
    completions = openai.Completion.create(params)
    return completions.choices[0].text


def summarize_text(text):
    # Set the model to use
    model_engine = "text-davinci-002"

    # Set the prompt for the model
    prompt = f"Summarize the following text in 4 sentences more or less : {text}"

    # Set the number of completions to generate
    num_completions = 1

    # Set the temperature for the completions
    temperature = 0.1

    # Set the max length of the completions
    max_length = 250
    params = {
        "model": "text-davinci-003",
        "prompt": "Say this is a test",
        "max_tokens": 7,
        "temperature": 0,
        "top_p": 1,
        "n": 1,
        "stream": False,
        "logprobs": None,
        "stop": "\n",
    }
    # Send the request to the API
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_length,
        n=num_completions,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Get the first completion
    completion = completions.choices[0]

    # Print the completion
    return completion.text
