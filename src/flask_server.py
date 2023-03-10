from dotenv import load_dotenv
from flask import Flask, make_response, request

from src.modules import interpreter, scraper, translater, visualizer
from src.modules.utils import build_article, get_config

load_dotenv()
app = Flask(__name__)


def main():
    app.run()


if __name__ == "__main__":
    main()


@app.route("/", methods=["GET"])
def index():
    """
    Test endpoint.
    """
    return make_response("", 200)


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
    goose_config = config["goose"]
    openai_config = config["openai"]
    translation = config["translation"]

    # Scraping article
    url_data = scraper.scrape_article(url, config=goose_config)
    if not url_data:
        return "Error while scraping"
    text = url_data["text"]
    original_title = url_data["title"]
    author = url_data["authors"]
    pub_date = url_data["publish_date"]
    source = url_data["domain"]
    description = url_data["meta_description"]

    # OpenAI completions
    summary = interpreter.get_completion(
        command="summarize",
        context=text,
        config=openai_config,
    )
    title = interpreter.get_completion(
        command="generate_title",
        context=summary,
        config=openai_config,
    )
    image_prompt = interpreter.get_completion(
        command="generate_instructions",
        context=summary,
        config=openai_config,
    )
    image_url = visualizer.generate_image(input_text=image_prompt, config=openai_config)

    # Translation to target language
    state = translation["state"]
    if state:
        language = translation["translation_target"]
        title = translater.deepl_translate(
            original_text=title, target=language, lang_level="more"
        )
        summary = translater.deepl_translate(
            original_text=summary, target=language, lang_level="more"
        )
    return str(
        build_article(
            article_title=title,
            article_body=summary,
            image_url=image_url,
            instructions=image_prompt,
            raw_title=original_title,
            date=pub_date,
            author=author,
            article_description=description,
            domain=source,
            original_url=url,
        )
    )
