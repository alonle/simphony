__author__ = 'Vaio-190X'

import pysrt


def to_ms(t):
    m,s,micros = t.minute, t.second, t.microsecond
    return ( micros + 1000000*s + 60*1000000*m ) / 1000000

def produce_dict(filename):
    srt = pysrt.open(filename, "iso-8859-1")
    start = []
    end = []
    text = []
    for sub in srt:
        start.append(to_ms(sub.start.to_time()))
        end.append(to_ms(sub.end.to_time()))
        text.append(sub.text)
    srt_dict = dict()
    srt_dict['start'] = start
    srt_dict['end'] = end
    srt_dict['text'] = text
    srt_dict['filename'] = [filename] * len(start)
    return srt_dict

# Usage example:
d = produce_dict('The Simpsons - S13 E17 Gump Roast.en.srt')
import pandas
pan = pandas.DataFrame.from_dict(d)
pan.to_csv("The Simpsons.s13e17.csv")
