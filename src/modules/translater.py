import os

import deepl


def deepl_translate(original_text: str, target: str, lang_level: str):
    auth_key = os.environ["DEEPL_API_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text=original_text, target_lang=target, formality=lang_level
    )
    return result.text
