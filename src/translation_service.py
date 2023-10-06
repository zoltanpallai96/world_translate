import asyncio
from typing import Tuple, Dict, Any

from googletrans import Translator


class NoTranslationException(Exception):
    pass


async def get_translation(word: str, source_language: str = 'en', target_language: str = 'en') -> Tuple[str, str, str]:
    translator = Translator()

    try:
        translation = translator.translate(word, src=source_language, dest=target_language)
    except TypeError:
        raise NoTranslationException()

    text = translation.text

    if text == word:
        raise NoTranslationException()

    definition, example = await asyncio.gather(
        parse_definition(translation.extra_data),
        parse_example(translation.extra_data)
    )
    return text, definition, example


async def parse_definition(translate_dict: Dict[str, Any]) -> str:
    try:
        definition = translate_dict["parsed"][3][2][0][0][1]
    except (IndexError, TypeError):
        return "Definition couldn't be fetched for this word"
    return definition.replace("<b>", "").replace("</b>", "")


async def parse_example(translate_dict: Dict[str, Any]) -> str:
    try:
        example = translate_dict["parsed"][3][1][0][1][1][0][0]
    except (IndexError, TypeError):
        return "Example couldn't be fetched for this word"
    return example.replace("<b>", "").replace("</b>", "")



