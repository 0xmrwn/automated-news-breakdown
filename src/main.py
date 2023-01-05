import datetime
from os import path

from modules import interpreter, scraper, translater, visualizer


def process_url():
    url = "https://edwardsnowden.substack.com/p/americas-open-wound?utm_source=pocket_saves"
    text = scraper.scrape_article(url)

    # Generate a summary of the article using the context
    title = interpreter.generate_title(text)
    summary = interpreter.summarize_text(text)
    image_prompt = interpreter.generate_prompt(text)

    visualizer.generate_image(image_prompt)
    translated_title = translater.translate_to_fr(title)
    translated_text = translater.translate_to_fr(summary)
    return str(
        build_article(
            title=translated_title,
            text=translated_text,
            image_path=path.join(".", "output", "image.jpeg"),
        )
    )


def build_article(title, text, image_path):
    with open(path.join(".", "data", "template.html"), "r") as template_file:
        template = template_file.read()
    return template.format(title=title, text=text, image=image_path)


def create_and_save_html_file(file_name):
    html_content = process_url()
    with open(file_name, "w") as html_file:
        html_file.write(html_content)


def create_html_file_name():
    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    return f"./output/summary_{date_time_str}.html"


def demo_function():
    url = "https://edwardsnowden.substack.com/p/americas-open-wound?utm_source=pocket_saves"
    text = scraper.scrape_article(url)
    title = interpreter.generate_title(text)
    summary = interpreter.summarize_text(text)
    image_prompt = interpreter.generate_prompt(text)
    visualizer.generate_image(image_prompt)
    translated_title = translater.translate_to_fr(title)
    translated_text = translater.translate_to_fr(summary)
    print("=" * 130)
    print(f"Titre GPT-3: \n{title}\n")
    print("-" * 130)
    print(f"Titre traduit en français: \n{translated_title}\n")
    print("-" * 130)
    print(f"Sommaire GPT-3: \n{summary}\n")
    print("-" * 130)
    print(f"Sommaire traduit: \n{translated_text}\n")
    print("=" * 130)
    print(f"Instruction pour générer une image dévrivant l'article: \n{image_prompt}\n")
    print("=" * 130)


def main():
    file_name = create_html_file_name()
    create_and_save_html_file(file_name)


if __name__ == "__main__":
    main()
