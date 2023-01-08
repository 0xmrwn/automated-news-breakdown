import os

import openai


def get_completion(
    model: str, context: str, template_prompt: str, temp: float, max_t: float
):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    formatted_prompt = template_prompt.format(text=context)
    completions = openai.Completion.create(
        engine=model,
        prompt=formatted_prompt,
        max_tokens=max_t,
        n=1,
        temperature=temp,
        top_p=1,
    )
    completion = completions.choices[0]
    return completion.text
