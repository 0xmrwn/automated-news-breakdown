import os

import openai
from dotenv import load_dotenv

load_dotenv()

# Replace YOUR_API_KEY with your actual API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Specify the text you want to summarize
text = "Insert the text you want to summarize here"

# Set the model to use and the summary length
model = "text-davinci-002"
length = 50

# Send the request to the GPT-3 API
response = openai.Completion.create(
    engine=model,
    prompt=f"summarize: {text}",
    max_tokens=length,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)

# Print the summary
print(response.text)
