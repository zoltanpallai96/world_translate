from typing import Tuple, Dict, Any

from src import translation_service
from src.models import session, Translation, MainWord, get_word_by_name


async def translation_if_word_exists(source_language: str, target_language: str,
                                     existing_word: MainWord) -> Tuple[Dict[str, Any], int]:
    translated_version = session.query(Translation).filter(existing_word.id ==
                                                           Translation.main_word_id,
                                                           Translation.target_language == target_language).one_or_none()
    if translated_version:
        return existing_word.to_dict(), 200

    translation, _, _ = await translation_service.get_translation(existing_word.word, source_language, target_language)

    new_translation = Translation(main_word_id=existing_word.id, target_language=target_language,
                                  translation=translation)
    session.add(new_translation)
    session.commit()

    return get_word_by_name(existing_word.word).to_dict(), 200


async def handle_new_word(source_language: str, target_language: str, word_name: str) -> Tuple[Dict[str, Any], int]:
    translation, definition, summary = await translation_service.get_translation(word_name, source_language, target_language)
    new_word = MainWord(word=word_name, summary=summary, example=definition)
    session.add(new_word)
    session.commit()
    existing_word = get_word_by_name(word_name)
    new_translation = Translation(main_word_id=existing_word.id, target_language=target_language,
                                  translation=translation)
    session.add(new_translation)
    session.commit()
    return get_word_by_name(word_name).to_dict(), 200


async def handle_if_neither_is_english(source_language: str, target_language: str, word_name: str) -> Tuple[Dict[str, Any], int]:
    new_word_name, definition, summary = await translation_service.get_translation(word_name, source_language, "en")

    main_word = get_word_by_name(new_word_name)
    if not main_word:
        main_word = MainWord(word=new_word_name, summary=summary, example=definition)
        session.add(main_word)
        session.commit()

    translated_version = session.query(Translation).filter(main_word.id ==
                                                           Translation.main_word_id,
                                                           Translation.target_language == source_language).one_or_none()

    if not translated_version:
        new_translation = Translation(main_word_id=main_word.id, target_language=source_language,
                                      translation=word_name)
        session.add(new_translation)
        session.commit()

    return await translation_if_word_exists("en", target_language, main_word)


def create_dict_for_list(w: MainWord, include_example: bool, include_trans: bool, include_summary: bool) -> Dict[str, Any]:
    return_dict = {"word": w.word}

    if include_example:
        return_dict["example"] = w.example

    if include_trans:
        return_dict["translations"] = [translation.to_dict() for translation in w.translations]

    if include_summary:
        return_dict["definition"] = w.summary

    return return_dict
