from typing import Dict, Any, Tuple, List, Optional

from fastapi import APIRouter
from sqlalchemy import desc, asc

from src import translation_service
from src.models import session, Translation, get_word_by_name, get_word_by_id, MainWord
from src.route_helper_functions import translation_if_word_exists, handle_new_word, handle_if_neither_is_english, \
    create_dict_for_list
from src.translation_service import NoTranslationException

translate_router = APIRouter()


@translate_router.get("/word/{word_name}/", response_model=Tuple[Dict[str, Any], int])
async def get_word_details(word_name: str, target_language: str, source_language: str = "en") -> Tuple[Dict[str, Any], int]:
    try:

        existing_word = get_word_by_name(word_name)

        if existing_word:
            return await translation_if_word_exists(target_language, source_language, existing_word)

        if target_language == "en" and source_language != "en":
            translation, _, _ = await translation_service.get_translation(word_name, source_language, target_language)
            target_language, source_language = source_language, target_language
            word_name = translation

        elif target_language != "en" and source_language != "en":
            return await handle_if_neither_is_english(source_language, target_language, word_name)

        return await handle_new_word(source_language, target_language, word_name)
    except NoTranslationException:
        return {"error": "no translation for the word in the given languages"}, 500


@translate_router.get("/words/", response_model=Tuple[List[Any], int])
async def get_words(skip: Optional[int] = 0, limit: Optional[int] = 10, sort: Optional[str] = None,
                    word_name: Optional[str] = None, include_summary: bool = False, include_trans: bool = False,
                    include_example: bool = False) -> Tuple[List[Any], int]:
    query = session.query(MainWord)

    if word_name:
        query = query.filter(MainWord.word.ilike(f"%{word_name}%"))

    if query.count() <= skip:
        skip = 0

    if sort:
        if sort.lower() == "asc":
            order = asc(MainWord.word)
        if sort.lower() == "desc":
            order = desc(MainWord.word)
    else:
        order = asc(MainWord.id)

    words = query.order_by(order).offset(skip).limit(limit).all()

    return [create_dict_for_list(w, include_example, include_trans, include_summary) for w in words], 200


@translate_router.delete("/word/{word_name}/", response_model=Tuple[Dict[str, Any], int])
async def delete_word(word_name: str) -> Tuple[Dict[str, Any], int]:
    existing_word = get_word_by_name(word_name)
    if existing_word:
        session.query(Translation).filter(Translation.main_word_id == existing_word.id).delete()
        session.delete(existing_word)
        session.commit()
        return {"response": "deletion successful"}, 200

    existing_translation = session.query(Translation).filter(Translation.translation == word_name).one_or_none()

    if existing_translation:
        existing_word = get_word_by_id(existing_translation.main_word_id)
        session.query(Translation).filter(Translation.main_word_id == existing_word.id).delete()
        session.delete(existing_word)
        session.commit()
        return {"response": "deletion successful"}, 200

    return {"error": "the given word was not in the database"}, 404

