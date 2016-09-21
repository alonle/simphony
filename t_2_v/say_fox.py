import pyttsx

engine = pyttsx.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)  # changes the voice
   engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()

engine = pyttsx.init()
engine.setProperty('voice', 60)  # use whatever voice_id you'd like
engine.say('The quick brown fox jumped over the lazy dog.')