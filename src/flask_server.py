from dotenv import load_dotenv
from flask import Flask, request

from src.modules import interpreter, scraper, translater, visualizer
from src.modules.utils import build_article, get_config

app = Flask(__name__)
load_dotenv()


def main():
    app.run()


if __name__ == "__main__":
    main()


@app.route("/", methods=["GET"])
def index():
    """
    Test endpoint. Returns "Server OK" when a GET request
    is made to the `/` route.
    """
    return "Server OK"


@app.route("/process_url", methods=["POST"])
def process_url():
    """
    This function is a Flask route that receives a POST request with
    a URL in the form data. The function uses this URL to extract an
    articleand then uses the OpenAI API to generate a title, summary,
    and set of instructions for the article. The generated instructions
    are used to generate an image with DALLE, and the DeepL API is used
    to translate the title and summary to a target language specified
    in the configuration. Finally, the function builds and returns
    an article object with the translated title, summary, image, and
    instructions.
    """
    # Setting configutation
    config = get_config()
    url = request.form["url"]

    # Scraping article
    text = scraper.scrape_article(url)

    # OpenAI completions
    completion_model = config["completions_engine"]
    title_prompt = config["prompts"]["generate_title"]["prompt"]
    title_temp = config["prompts"]["generate_title"]["temperature"]
    title_max_t = config["prompts"]["generate_title"]["max_tokens"]
    title = interpreter.get_completion(
        model=completion_model,
        context=text,
        template_prompt=title_prompt,
        temp=title_temp,
        max_t=title_max_t,
    )
    summary_prompt = config["prompts"]["summarize"]["prompt"]
    summary_temp = config["prompts"]["summarize"]["temperature"]
    tsummary_max_t = config["prompts"]["summarize"]["max_tokens"]
    summary = interpreter.get_completion(
        model=completion_model,
        context=text,
        template_prompt=summary_prompt,
        temp=summary_temp,
        max_t=tsummary_max_t,
    )
    instruction_prompt = config["prompts"]["generate_instructions"]["prompt"]
    instruction_temp = config["prompts"]["generate_instructions"]["temperature"]
    instruction_max_t = config["prompts"]["generate_instructions"]["max_tokens"]
    image_prompt = interpreter.get_completion(
        model=completion_model,
        context=text,
        template_prompt=instruction_prompt,
        temp=instruction_temp,
        max_t=instruction_max_t,
    )
    image_url = visualizer.generate_image(image_prompt)

    # Translation to target language
    language = config["translation_target"]
    translated_title = translater.deepl_translate(
        original_text=title, target=language, lang_level="more"
    )
    translated_text = translater.deepl_translate(
        original_text=summary, target=language, lang_level="more"
    )
    return str(
        build_article(
            article_title=translated_title,
            article_body=translated_text,
            image_url=image_url,
            instructions=image_prompt,
        )
    )
