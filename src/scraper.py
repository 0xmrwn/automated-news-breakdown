import re
import string

import requests
from bs4 import BeautifulSoup


def scrape_article(url: str):
    # Trying request with provided url
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    soup = BeautifulSoup(response.text, "html.parser")

    # Trying to find the main content using different CSS classes
    article_content = None
    for element in ["article-body", "article-text", "articleBody"]:
        article_content = soup.find(class_=element)
        if article_content:
            break
    if not article_content:
        # If the main content is not found, fall back to searching for the body tag
        article_content = soup.find("body")

    # Removing junk
    for element in article_content(["aside", "nav"]):
        element.extract()

    # Remove any HTML tags and return kind of clean text
    raw_text = article_content.get_text().strip()

    return clean_text(raw_text)


def clean_text(text):
    # remove excess whitespace at the beginning and end of the string
    text = text.strip()

    # remove excess whitespace between words
    text = re.sub(r"\s+", " ", text)

    # remove mentions of social media widgets
    text = re.sub(r"TwitterFacebookEmail", "", text)

    # remove other junk coming from HTML extraction
    text = re.sub(r"<.*?>", "", text)

    return text
