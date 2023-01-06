from os import path

from flask import Flask, request

from src.modules import interpreter, scraper, translater, visualizer

app = Flask(__name__)


def main():
    app.run()


if __name__ == "__main__":
    main()


@app.route("/", methods=["GET"])
def index():
    return "Server OK"


def build_article(title, text, image_path, instructions, image):
    with open(path.join(".", "data", "template.html"), "r") as template_file:
        template = template_file.read()
    return template.format(
        title=title, text=text, image=image_path, prompt=instructions, base64=image
    )


@app.route("/process_url", methods=["POST"])
def process_url():
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
