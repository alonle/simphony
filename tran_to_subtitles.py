import re
import pandas
from difflib import SequenceMatcher


def clean_text(row):
    new_line = row.replace('\n', '')
    new_line = re.sub(re.compile('\(.+\)', re.M), '', new_line)
    new_line = re.sub(re.compile('\[.+\]', re.M), '', new_line)
    new_line = re.sub('["\,\'\/\\\-]', '', new_line)
    new_line = new_line.replace('<i>', '').replace('</i>', '')
    return new_line.lower()


def extract_speaker(row):
    if ':' in row:
        sep = row.find(':')
        if sep + 2 < len(row):
            return row[0: sep], row[sep + 2:]


def find_speaker(sentence, df):
    def calc_diff_score(sentence):
        return lambda row: SequenceMatcher(None, sentence, row.text).ratio()

    df = pandas.DataFrame(df)
    df['score'] = df.apply(calc_diff_score(sentence), axis=1)
    return df.sort_values(by="score", ascending=False).iloc[0]


def read_subtitles(filepath, df):
    sub = pandas.read_csv(filepath)
    for i, row in sub.iterrows():
        text = row.text
        if len(text) > 1:
            sentence = clean_text(text)
            spe_res = find_speaker(sentence, df)
            if spe_res.score > 0.5:
                speaker = spe_res.speaker
            else:
                speaker = 'UNKNOWN'
        print i, text, speaker


def build_df(filepath):
    text = []
    speaker = []
    with open(filepath, 'rb') as sub:
        for line in sub:
            if (line) != '\n':
                new_line = clean_text(line)
                categorized = extract_speaker(new_line)
                if categorized:
                    text.append(categorized[1])
                    speaker.append(categorized[0])
    d = {'text': text, 'speaker': speaker}
    return pandas.DataFrame.from_dict(d)


transcript = 'subscript_s21e13.txt'
df = build_df(transcript)

subtitles = 'The Simpsons.s21e13.csv'
read_subtitles(subtitles, df)