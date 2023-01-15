import logging
import os

import deepl
from deep_translator import GoogleTranslator

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(process)d] [%(levelname)s] [%(filename)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",
)
logging.getLogger("deepl").setLevel(logging.WARNING)


def deepl_translate(original_text: str, target: str, lang_level: str):
    """
    This function uses the DeepL API to translate a given text from its
    original language to a target language. The formality level of the
    translation can also be controlled. The function returns the
    translated text as a string.
    """
    logging.info("Translating with DeepL")
    auth_key = os.environ["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text=original_text, target_lang=target, formality=lang_level
    )
    return result.text


def google_translate(original_text: str, target: str):
    """
    This function uses the Google Translate API to translate a given
    text from its original language to a target language. The function
    returns the translated text as a string.
    """
    logging.info("Translating with Google Translate")
    return GoogleTranslator(source="auto", target=target.lower()).translate(
        text=original_text
    )
