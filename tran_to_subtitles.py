import re
import pandas
from difflib import SequenceMatcher


def clean_text(row):
    new_line = row.replace('\n', ' ')
    new_line = re.sub(re.compile('\(.+\)', re.M), '', new_line)
    new_line = re.sub(re.compile('\[.+\]', re.M), '', new_line)
    new_line = re.sub('[:\.\\\"\,\'/]', '', new_line)
    new_line = new_line.replace('<i>', '').replace('</i>', '').replace('-', '')
    return new_line.lower()


def extract_speaker(row):
    if ':' in row:
        sep = row.find(':')
        if sep + 2 < len(row):
            return row[0: sep], row[sep + 2:]


def find_speaker(sentence, df, previous_loc):
    def calc_diff_score(sentence):
        return lambda row: SequenceMatcher(None, sentence, row.text).ratio()

    def find_subsentence(sentence):
        return lambda row: sentence in row.text

    def dist_from_previous(previous_loc, loc):
        return abs(loc-previous_loc)

    # df = df.copy()
    df['subsentence'] = df.apply(find_subsentence(sentence), axis=1)
    len_exact = len(df[df['subsentence'] == True])
    if len_exact > 0:
        loc_list = df[df['subsentence'] == True].index.tolist()
        list_dist = [dist_from_previous(previous_loc, i) for i in loc_list]
        col_index = loc_list[list_dist.index(min(list_dist))]
        df.loc[col_index, 'score'] = 1
        return col_index, df.iloc[col_index]

    else:
        df['score'] = df.apply(calc_diff_score(sentence), axis=1)
        df = df.sort_values(by="score", ascending=False)

        return df.index[0], df.iloc[0]


def read_subtitles(filepath, df):
    sub = pandas.read_csv(filepath)
    loc = 0
    count_uk = 0
    speakers = []
    for i, row in sub.iterrows():
        text = row.text
        if text is not 'nan' and len(text) > 1:
            sentence = clean_text(text)
            new_loc, spe_res = find_speaker(sentence, df, loc)
            if i == 148:
                pass
            # if text[0] is not ('(' or '<'):
            if sentence != '':
                if not spe_res.score or spe_res.score > 0.5:
                    speakers.append(spe_res.speaker)
                    loc = new_loc
                else:
                    speakers.append('UNKNOWN')
                    count_uk += 1
            else:
                speakers.append('NONE')
        else:
            speakers.append('NONE')
        print str(i) + ', ' + speakers[i] + ': ' + text
    print count_uk
    return speakers


def build_df(filepath):
    text = []
    speaker = []
    with open(filepath, 'rb') as sub:
        for line in sub:
            if line != '\n':
                categorized = extract_speaker(line)
                if categorized:
                    new_line = clean_text(categorized[1])
                    text.append(new_line)
                    speaker.append(categorized[0])
    d = {'text': text, 'speaker': speaker}
    return pandas.DataFrame.from_dict(d)


episode = 's21e13'
transcript = 'transcript_' + episode + '.txt' # 'transcript_s13e17.txt'
df = build_df(transcript)
subtitles = 'The Simpsons.' + episode + '.csv'
speakers = read_subtitles(subtitles, df)
sub = pandas.read_csv(subtitles)
sub['speaker'] = speakers
sub = sub.drop('Unnamed: 0', 1)
sub.to_csv('subs_with_speaker-' + episode + '.csv')
