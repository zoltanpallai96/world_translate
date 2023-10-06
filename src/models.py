from typing import Dict, Any

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, sessionmaker

from src.database import Base, engine


class MainWord(Base):
    __tablename__ = 'main_words'

    id = Column(Integer, primary_key=True)
    word = Column(String(255), nullable=False, unique=True)
    summary = Column(String(255))
    example = Column(String(255))

    translations = relationship("Translation", back_populates="main_word")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "word": self.word,
            "summary": self.summary,
            "example": self.example,
            "translations": [translation.to_dict() for translation in self.translations]
        }


class Translation(Base):
    __tablename__ = 'translations'

    id = Column(Integer, primary_key=True)
    main_word_id = Column(Integer, ForeignKey('main_words.id'))
    target_language = Column(String(10), nullable=False)
    translation = Column(String(255), nullable=False)

    __table_args__ = (UniqueConstraint('main_word_id', 'target_language', name='_word_language_uc'),)

    main_word = relationship("MainWord", back_populates="translations")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language": self.target_language,
            "translation": self.translation
        }


Session = sessionmaker(bind=engine)
session = Session()


def get_word_by_name(word: str):
    return session.query(MainWord).filter(MainWord.word == word).one_or_none()


def get_word_by_id(id: int):
    return session.query(MainWord).filter(MainWord.id == id).one_or_none()

