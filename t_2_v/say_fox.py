import pyttsx

engine = pyttsx.init()
voices = engine.getProperty('voices')
for i,voice in enumerate(voices):
    print '{} {} {} {} {}'.format(i,voice.age,voice.gender,voice.id,voice.languages)
    engine.setProperty('voice', voice.id)  # changes the voice
    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()

engine = pyttsx.init()
engine.setProperty('voice', 15)  # use whatever voice_id you'd like
# engine.setProperty('female', 30)
engine.setProperty('rate', 50)# use whatever voice_id you'd like
engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()

