from abc import ABC, abstractmethod

import requests
from dataclasses import dataclass
import hanzidentifier
import pinyin


@dataclass
class Sentence:
    chinese: str
    english: str
    pinyin: str


class SentenceFinder(ABC):
    @abstractmethod
    def __call__(self, word: str) -> Sentence:
        ...


class EmptySentenceFinder(SentenceFinder):
    def __call__(self, word: str) -> Sentence:
        return Sentence(chinese='', english='', pinyin='')


class TatoebaSentenceFinder(SentenceFinder):
    def __call__(self, word: str) -> Sentence:
        query = f'https://tatoeba.org/en/api_v0/search?from=cmn&query="{word}"&to=eng'
        response = requests.get(url=query)

        results = response.json()['results']
        for result in results:
            if hanzidentifier.is_simplified(result['text']):

                try:
                    sentence = Sentence(
                        chinese=result['text'],
                        english=result['translations'][0][0]['text'],
                        pinyin=pinyin.get(result['text']),
                    )
                    print(f"{word} - {sentence.chinese} - {sentence.english}")
                    return sentence
                except IndexError:
                    pass

        return Sentence(chinese='', english='', pinyin='')