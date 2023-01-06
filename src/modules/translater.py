import os
from html import unescape

from google.cloud import translate_v2 as translate


def translate_to_fr(text):
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = "./cloud-sandbox-373810-e58ea32500ca.json"

    # Use the translate client to translate the text
    client = translate.Client()
    result = client.translate(text, target_language="fr")
    return unescape(result["translatedText"])
