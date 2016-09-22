__author__ = 'Vaio-190X'

import pysrt
import re

def to_sec(t):
    m,s,micros = t.minute, t.second, t.microsecond
    return ( micros + 1000000*s + 60*1000000*m ) / 1000000

def produce_dict(filename):
    m = re.search("offset ([\+\-\d.]+)", open(filename, "r", encoding="iso-8859-1").readlines()[0].lower())
    offset = float(m.group(1)) if m else 0
    if offset != 0:
        print("File {} with offset {}".format(filename, offset))    
    srt = pysrt.open(filename, "iso-8859-1")
    start = []
    end = []
    text = []
    for sub in srt:
        start.append(to_sec(sub.start.to_time()) + offset)
        end.append(to_sec(sub.end.to_time()) + offset)
        text.append(sub.text)
    srt_dict = dict()
    srt_dict['start'] = start
    srt_dict['end'] = end
    srt_dict['text'] = text
    return srt_dict

# Usage example: 
#d = produce_dict('The Simpsons.s25e11.srt')
#import pandas
#pan = pandas.DataFrame.from_dict(d)
#pan.to_csv("The Simpsons.s25e11.csv")
