import re
from html import unescape

import requests
from bs4 import BeautifulSoup
from goose3 import Goose
from newspaper import Article
from tenacity import retry, stop_after_attempt, wait_random_exponential


def scrape_article(url: str, config: dict):
    parsed_data = parse_url_goose(url, config)
    if not len(parsed_data["text"]) or len(parsed_data["text"]) < 100:
        parsed_data = parse_url_newspaper(url)
    if not len(parsed_data["text"]) or len(parsed_data["text"]) < 100:
        parsed_data = manual_scraping(url)
    return parsed_data


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def parse_url_goose(url: str, config: dict):
    with Goose(config) as g:
        article = g.extract(url)
    return {
        "title": article.title,
        "authors": article.authors,
        "publish_data": article.publish_date,
        "text": article.cleaned_text,
        "url": article.final_url,
        "domain": article.domain,
        "meta_description": article.meta_description,
    }


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def parse_url_newspaper(url: str):
    article = Article(url)
    article.download()
    article.parse()
    return {
        "title": article.title,
        "authors": article.authors,
        "publish_data": article.publish_date,
        "text": article.text,
        "url": url,
        "domain": None,
        "meta_description": None,
    }


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def manual_scraping(url: str):
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
    text = raw_text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"TwitterFacebookEmail", "", text)
    text = re.sub(r"<.*?>", "", text)
    return {
        "title": None,
        "authors": None,
        "publish_data": None,
        "text": unescape(text),
        "url": url,
        "domain": None,
        "meta_description": None,
    }
