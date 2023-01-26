import logging
import re
from html import unescape

import requests
from bs4 import BeautifulSoup
from goose3 import Goose
from newspaper import Article
from tenacity import retry, stop_after_attempt, wait_random_exponential

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",
)


def is_valid_url(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    header = {"User-Agent": user_agent}
    try:
        return requests.get(url, headers=header).status_code == 200
    except requests.exceptions.MissingSchema as e:
        logging.warning(e)
        return False


def scrape_article(url: str, config: dict):
    """
    Tries 3 methods for scraping url contents. Each time checks if
    extraction was successful before trying the less efficient methods.
    """
    if not is_valid_url(url):
        return False
    parsed_data = parse_url_goose(url, config)
    if not parsed_data["text"] or len(parsed_data["text"]) < 100:
        logging.warning("Text contents not located with Goose3")
        parsed_data = parse_url_newspaper(url)
    if not parsed_data["text"] or len(parsed_data["text"]) < 100:
        logging.warning("Text contents not located with Newspaper3k")
        parsed_data = manual_scraping(url)
    content_len = len(str(parsed_data["text"]).split())
    logging.info(f"Extracted {content_len} tokens from URL")
    return parsed_data


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def parse_url_goose(url: str, config: dict):
    """
    Scrape url contents with goose3. This methods extracts several
    attributes but is sensitive to website formats.
    """
    logging.info("Scraping URL contents with Goose3")
    with Goose(config) as g:
        article = g.extract(url)
    return {
        "title": article.title,
        "authors": article.authors,
        "publish_date": article.publish_date,
        "text": article.cleaned_text,
        "url": article.final_url,
        "domain": article.domain,
        "meta_description": article.meta_description,
    }


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def parse_url_newspaper(url: str):
    """
    Scrape url contents with newspaper3k. This methods gets less
    metadata but works on more websites.
    """
    logging.info("Scraping URL contents with Newspaper3k")
    article = Article(url)
    article.download()
    article.parse()
    return {
        "title": article.title,
        "authors": article.authors,
        "publish_date": article.publish_date,
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
    logging.info("Scraping URL contents with BeautifulSoup")
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    article_content = None
    for element in ["article-body", "article-text", "articleBody", "p"]:
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
        "publish_date": None,
        "text": unescape(text),
        "url": url,
        "domain": None,
        "meta_description": None,
    }
