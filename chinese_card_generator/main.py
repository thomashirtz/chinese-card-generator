import pinyin
import pandas as pd

from chinese_card_generator import utilities
from chinese_card_generator import tatoeba
from chinese_card_generator import chatopera


def process_file(
        input_path: str,
        output_path: str,
        num_synonyms: int = 3,
        threshold_synonyms: float = 0.8
):
    dataframe = utilities.get_dataframe(input_path)

    tmp = []
    for index, row in dataframe.iterrows():

        word = row['Simplified']
        sentence = tatoeba.get_sentence(word=word)
        synonym_list = chatopera.get_synonym_list(
            word=word,
            n=num_synonyms,
            threshold=threshold_synonyms,
        )

        tmp.append({
            'Hint': row['Pinyin'][0],
            'SentenceSimplified': sentence.chinese,
            'SentenceMeaning': sentence.english,
            'SentencePinyin': pinyin.get(sentence.chinese),
            'Synonyms': chatopera.format_synonym_list(synonym_list)
        })

        if index > 3:
            break

    tmp_dataframe = pd.DataFrame(tmp)
    output_dataframe = pd.concat([dataframe, tmp_dataframe], axis=1)
    output_dataframe.to_csv(
        path_or_buf=output_path,
        sep='\t',
        index=False,
        header=False
    )
    print()


if __name__ == '__main__':
    input_path = r'..\data\input.txt'
    output_path = r'..\data\output.csv'
    process_file(
        input_path=input_path,
        output_path=output_path,

    )
