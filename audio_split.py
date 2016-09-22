__author__ = 'Vaio-190X'

import re
from subtitles import *
filename = '21x13 - The Color Yellow.srt'
d = produce_dict(filename)

from pydub import AudioSegment
aac = AudioSegment.from_file("21x13 - The Color Yellow.mp3", "mp3")

offset = 0
d['mp3'] = []
for i in range(len(d['text'])):
    part = aac[d['start'][i]*1000+offset:d['end'][i]*1000+offset]
    newname = re.sub('[\s\,\-\'\"?<>/\*]', '', d['text'][i])
    if not newname == '':
        part.export('The color yellow\\' + newname + '.mp3', format='mp3')
        d['mp3'].append(newname)
    else:
        d['mp3'].append(None)

import pandas
pan = pandas.DataFrame.from_csv('subs_with_speaker-s21e13.csv')
pan['mp3'] = d['mp3']
pan.to_csv('subs_with_speaker-s21e13.csv')
#pan.to_csv("The Simpsons.s25e11.csv")

# def go(start, offset):
#     print d['text'][start]
#     part = aac[d['start'][start]+offset:d['end'][start]+offset]
#     part.export('test.wave', format='wave').write()
#
# go(152, -500)