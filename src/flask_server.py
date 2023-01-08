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
    completion_model = config["openai_config"]["completions_engine"]
    dalle_img_size = config["openai_config"]["image_size"]
    title_config = config["openai_config"]["prompts"]["generate_title"]
    summary_config = config["openai_config"]["prompts"]["summarize"]
    instruction_config = config["openai_config"]["prompts"]["generate_instructions"]
    language = config["translation_target"]

    # Scraping article
    text = scraper.scrape_article(url)

    # OpenAI completions
    title = interpreter.get_completion(
        model=completion_model,
        context=text,
        config=title_config,
    )
    summary = interpreter.get_completion(
        model=completion_model,
        context=text,
        config=summary_config,
    )
    image_prompt = interpreter.get_completion(
        model=completion_model,
        context=text,
        config=instruction_config,
    )
    image_url = visualizer.generate_image(
        input_text=image_prompt, dimensions=dalle_img_size
    )

    # Translation to target language
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
