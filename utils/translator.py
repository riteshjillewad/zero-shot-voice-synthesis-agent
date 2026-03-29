# utils/translator.py

from transformers import pipeline

# Load NLLB model
translator = pipeline(
    "translation",
    model="facebook/nllb-200-distilled-600M"
)

# Language mapping (NLLB format)
LANGUAGE_MAP = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "fr": "fra_Latn",
    "de": "deu_Latn",
    "es": "spa_Latn",
    "it": "ita_Latn",
    "pt": "por_Latn",
    "ru": "rus_Cyrl",
    "ja": "jpn_Jpan",
    "ko": "kor_Hang",
    "zh-cn": "zho_Hans",
    "ar": "arb_Arab"
}

def translate_text(text, target_lang, source_lang="en"):
    try:
        if target_lang == source_lang:
            return text

        src_code = LANGUAGE_MAP.get(source_lang, "eng_Latn")
        tgt_code = LANGUAGE_MAP.get(target_lang, "eng_Latn")

        result = translator(
            text,
            src_lang=src_code,
            tgt_lang=tgt_code
        )

        return result[0]["translation_text"]

    except Exception as e:
        print("Translation Error:", e)
        return text