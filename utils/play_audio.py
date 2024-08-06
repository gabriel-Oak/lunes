# from dimits import Dimits
from playsound import playsound
from gtts import gTTS

# dt = Dimits("pt_BR-faber-medium")

file_name = 'audios/tts.mp3'

def play_audio(speech: str):
  # print('[output] ' + speech)
  # dt.text_2_speech(speech, engine="aplay")
  tts = gTTS(speech, lang="pt-BR")
  tts.save(file_name)
  playsound(file_name)
