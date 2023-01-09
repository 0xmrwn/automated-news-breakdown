import os

import deepl


def deepl_translate(original_text: str, target: str, lang_level: str):
    """
    This function uses the DeepL API to translate a given text from its
    original language to a target language. The formality level of the
    translation can also be controlled. The function returns the
    translated text as a string.
    """
    auth_key = os.environ["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text=original_text, target_lang=target, formality=lang_level
    )
    return result.text
