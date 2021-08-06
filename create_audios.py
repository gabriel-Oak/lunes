from gtts import gTTS
from playsound import playsound


def play_audio(audio):
  tts = gTTS(audio, lang='pt-br')
  tts.save('audios/tts.mp3')
  playsound('audios/tts.mp3')
