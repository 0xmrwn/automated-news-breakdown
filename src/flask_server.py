from os import path

from flask import Flask, request

from src.modules import interpreter, scraper, translater, visualizer
from src.modules.utils import build_article

app = Flask(__name__)


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
    visualizer.generate_image(image_prompt)
    translated_title = translater.translate_to_fr(title)
    translated_text = translater.translate_to_fr(summary)
    image_abs_path = path.abspath("./output/image.jpeg")
    return str(
        build_article(
            title=translated_title,
            text=translated_text,
            image_path=image_abs_path,
            instructions=image_prompt,
            image=visualizer.encode_image(),
        )
    )
