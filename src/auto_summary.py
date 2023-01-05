from os import path

from flask import Flask, request

from src.modules import interpreter, scraper, translater, visualizer

app = Flask(__name__)


def main():
    app.run()


if __name__ == "__main__":
    main()


def build_article(title, text, image_path):
    template = """
    <!doctype html>
    <html>
    <head>
    <title>{title}</title>
    </head>
    <body>
    <h1>{title}</h1>
    <img src="{image}" alt="{title}">
    <p>{text}</p>
    </body>
    </html>
    """
    return template.format(title=title, text=text, image=image_path)


@app.route("/process_url", methods=["POST"])
def process_url():
    url = request.form["url"]
    text = scraper.scrape_article(url)

    # Generate a summary of the article using the context
    title = interpreter.generate_title(text)
    summary = interpreter.summarize_text(text)
    image_prompt = interpreter.generate_prompt(text)

    visualizer.generate_image(image_prompt)
    translated_title = translater.translate_to_fr(title)
    translated_text = translater.translate_to_fr(summary)
    return build_article(
        title=translated_title,
        text=translated_text,
        image_path=path.join(".", "output", "image.jpeg"),
    )
