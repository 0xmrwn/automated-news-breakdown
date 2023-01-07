import re
from html import unescape

import requests
from bs4 import BeautifulSoup


def scrape_article(url: str):
    """
    Scrapes the main content from an HTML article given a URL by searching
    for specific class names in the page's HTML and removing certain elements
    from the content. Returns the cleaned up text of the article's main content.
    """
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    article_content = None
    for element in ["article-body", "article-text", "articleBody"]:
        article_content = soup.find(class_=element)
        if article_content:
            break
    if not article_content:
        article_content = soup.find("body")
    for element in article_content(["aside", "nav"]):
        element.extract()
    raw_text = article_content.get_text().strip()
    return clean_text(raw_text)


def clean_text(text):
    """
    Cleans up raw text by removing excess whitespace, certain substrings,
    and HTML tags, and unescaping any HTML character entities.
    """
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"TwitterFacebookEmail", "", text)
    text = re.sub(r"<.*?>", "", text)
    return unescape(text)
