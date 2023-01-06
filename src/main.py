import datetime
from os import path

from modules import file_manager as fm
from modules import interpreter, scraper, translater, visualizer


def process_url():
    url = "https://edwardsnowden.substack.com/p/americas-open-wound?utm_source=pocket_saves"
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
        )
    )


def build_article(title, text, image_path, instructions):
    with open(path.join(".", "data", "template.html"), "r") as template_file:
        template = template_file.read()
    return template.format(
        title=title, text=text, image=image_path, prompt=instructions
    )


def create_and_save_html_file(file_name):
    html_content = process_url()
    with open(file_name, "w") as html_file:
        html_file.write(html_content)


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
    file_name = fm.create_file_name(item="summary", file_type="html")
    create_and_save_html_file(file_name)


if __name__ == "__main__":
    main()
