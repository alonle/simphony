from gensim.models import Word2Vec
from gensim.models import Doc2Vec
import numpy as np
import pandas
from nltk.corpus import stopwords
import re

model = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
# model = Doc2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)  # C binary format

def clean_text(line):
    new_line = line.replace('\n', ' ')
    new_line = re.sub(re.compile('\(.+\)', re.M), '', new_line)
    new_line = re.sub(re.compile('\[.+\]', re.M), '', new_line)
    new_line = re.sub('[\!:\\\"\,\'/]', '', new_line)
    new_line = new_line.replace('<i>', '').replace('</i>', '').replace('-', '').replace('\.', '')
    new_line = new_line.lower().split()
    if new_line:
        return no_stopwords(new_line)


def no_stopwords(sentence):
    return [w for w in sentence if w not in stopwords]


def read_scv(episode='s21e13'):
    df = pandas.read_csv('subs_with_speaker-' + episode + '.csv')
    score = []
    for i, row in df.iterrows():
        text = row.text
        new_text = clean_text(text)
        if new_text:
            score.append(calcualte_similairy(new_text, sentence_to_compare=['thank','you']))
    # score = [a if a != np.inf else 0 for a in score]
    print score[53]
    min_score_index = np.argmin(score)
    return min_score_index, np.min(score), df.iloc[min_score_index]


def calcualte_similairy(subs_sentence, sentence_to_compare):
    return model.wmdistance(sentence_to_compare, subs_sentence)


stopwords = stopwords.words('english')
# Remove their stopwords.
read_scv()
    # >>> docvec = model2.docvecs[99]
# >>> docvec = model2.docvecs['SENT_99']  # if string tag used in training
# >>> sims = d2v_model.docvecs.most_similar(99)
# >>> sims = d2v_model.docvecs.most_similar('SENT_99')
# >>> sims = d2v_model.docvecs.most_similar(docvec)
#
# model.build_vocab(new_sentences, update=True)
# model.train(new_sentences)