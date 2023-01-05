from modules import interpreter, scraper, translater, visualizer

# Scrape the article from the URL
url = "https://edwardsnowden.substack.com/p/americas-open-wound?utm_source=pocket_saves"
text = scraper.scrape_article(url)

# Generate a summary of the article using the context
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
