import scraper
import summarizer

# Scrape the article from the URL
url = "https://edwardsnowden.substack.com/p/americas-open-wound?utm_source=pocket_saves"
text = scraper.scrape_article(url)

# Set the context to the text of the article
context = text

# Generate a summary of the article using the context
summary = summarizer.summarize_text(text)
print(f"Summary: {summary}")

# Ask a question about the article using the context
# question = "What is the main topic of the article?"
# response = summarizer.generate_response(question, context)
# print(f"Response: {response}")

# # Ask another question using the context
# question = "What is the author's stance on the topic?"
# response = summarizer.generate_response(question, context)
# print(f"Response: {response}")
