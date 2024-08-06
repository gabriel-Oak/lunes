import sounddevice
from utils.play_audio import play_audio
import speech_recognition as sr

def create_listener(callback):
  def listener(recognizer, audio):
    try:
      speech = recognizer.recognize_google(audio, language='pt-BR').lower()
      print('[input] ' + speech)
      callback(speech)
    except sr.UnknownValueError:
      print("[log] Não entendi o quê você disse. Ou você não disse nada haha!")
    except sr.RequestError as e:
      print('[log] Error; {0}'.format(e))
      play_audio('Algo deu errado, você está conectado à internet?')
  return listener

def listen_background(callback):
  recognizer = sr.Recognizer()
  mic = sr.Microphone()
  with mic as source:
    recognizer.adjust_for_ambient_noise(source)
  return recognizer.listen_in_background(mic, create_listener(callback))


def listen() -> str:
  recognizer = sr.Recognizer()
  with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
  speech = recognizer.recognize_google(audio, language='pt-BR').lower()
  print('[input] ' + speech)
  
  return speech