from gensim.models import Word2Vec
import numpy as np
import re
# import pandas
# from nltk.corpus import stopwords


def clean_text(line):
    if isinstance(line, str):
        new_line = line.replace('\n', ' ')
        new_line = re.sub(re.compile('\(.+\)', re.M), '', new_line)
        new_line = re.sub(re.compile('\[.+\]', re.M), '', new_line)
        new_line = re.sub('[\.\!:\\\"\,\'/]', '', new_line)
        new_line = new_line.replace('<i>', '').replace('</i>', '').replace('-', '')
        new_line = new_line.lower().split()
        return new_line
    # if new_line:
    #     return no_stopwords(new_line)


# def no_stopwords(sentence):
#     return [w for w in sentence if w not in stopwords]

def calculate_similarity(subs_sentence, sentence_to_compare):
    return model.wmdistance(sentence_to_compare, subs_sentence)


def find_sentence(sentences, sentence_to_compare='Lets have another beer!'):
    # df = pandas.read_csv('subs_with_speaker-' + episode + '.csv')
    # df = pandas.read_csv('segments.csv')
    score = []
    sentence_to_compare = clean_text(sentence_to_compare)
    for text in sentences:
        new_text = clean_text(text)
        # print new_text
        if new_text:
            score.append(calculate_similarity(new_text, sentence_to_compare=sentence_to_compare))
        else:
            score.append(np.inf)
    min_score_index = np.argmin(score)
    # return min_score_index, np.min(score), df.iloc[min_score_index]
    return min_score_index


# stopwords = stopwords.words('english')
model = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

## example
# df = pandas.read_csv('segments.csv')
# sentences = df.text
# find_sentence(sentences)