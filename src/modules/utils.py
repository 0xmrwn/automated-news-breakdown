import datetime
from os import path


def create_file_name(item: str, file_type: str):
    """
    Creates a file name in the format `./output/{item}_{datetime}.{file_type}`
    using the current date and time.
    """
    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    return f"./output/{item}_{date_time_str}.{file_type}"


def build_article(article_title, article_body, image_url, instructions):
    """
    Builds an HTML article using a template file and the provided title,
    text, image path, instructions for image generation, and image data.
    """
    with open(path.join(".", "data", "template.html"), "r") as template_file:
        template = template_file.read()
    return template.format(
        title=article_title, text=article_body, url=image_url, prompt=instructions
    )
