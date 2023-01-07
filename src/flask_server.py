from dotenv import load_dotenv
from flask import Flask, request

from src.modules import interpreter, scraper, translater, visualizer
from src.modules.utils import build_article

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
    Accepts a POST request with a URL in the form data. The function then
    processes the URL by scraping the main content of the corresponding article,
    generating a title, summary, and image prompt based on the text, creating
    an image based on the prompt, translating the title and summary to French,
    and building an HTML article with all of this information. The function
    returns the HTML of the built article.
    """
    url = request.form["url"]
    text = scraper.scrape_article(url)
    title = interpreter.generate_title(text)
    summary = interpreter.summarize_text(text)
    image_prompt = interpreter.generate_prompt(text)
    image_url = visualizer.generate_image(image_prompt)
    translated_title = translater.deepl_translate(
        original_text=title, target="FR", lang_level="more"
    )
    translated_text = translater.deepl_translate(
        original_text=summary, target="FR", lang_level="more"
    )
    return str(
        build_article(
            article_title=translated_title,
            article_body=translated_text,
            image_url=image_url,
            instructions=image_prompt,
        )
    )
