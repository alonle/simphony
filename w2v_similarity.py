from gensim.models import Word2Vec
from gensim.models import Doc2Vec
import numpy as np
import pandas
from nltk.corpus import stopwords
import re

# model = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
# model = Doc2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)  # C binary format

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


def no_stopwords(sentence):
    return [w for w in sentence if w not in stopwords]


def read_scv(episode='s21e13', sentence_to_compare='lets have another beer'):
    # df = pandas.read_csv('subs_with_speaker-' + episode + '.csv')
    df = pandas.read_csv('segments.csv')
    score = []
    for i, row in df.iterrows():
        # if i != 1392:
        #     continue
        text = row.text
        new_text = clean_text(text)
        # print new_text
        if new_text:
            score.append(calcualte_similairy(new_text, sentence_to_compare=sentence_to_compare.split()))
        else:
            score.append(np.inf)
    # score = [a if a != np.inf else 0 for a in score]
    min_score_index = np.argmin(score)
    return min_score_index, np.min(score), df.iloc[min_score_index]


def calcualte_similairy(subs_sentence, sentence_to_compare):
    return model.wmdistance(sentence_to_compare, subs_sentence)


# stopwords = stopwords.words('english')
# Remove their stopwords.
read_scv()
