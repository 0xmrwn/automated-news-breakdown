import os

from google.cloud import translate_v2 as translate


def translate_to_fr(text):
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to the path to your service account key file.
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = "./cloud-sandbox-373810-e58ea32500ca.json"

    # Use the translate client to translate the text
    client = translate.Client()
    result = client.translate(text, target_language="fr")

    return result["translatedText"]
