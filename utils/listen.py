import sounddevice
import speech_recognition as sr

def listen() -> str:
  mic = sr.Recognizer()
  with sr.Microphone() as source:
    audio = mic.listen(source)
  speech = mic.recognize_google(audio, language='pt-BR').lower()
  print('[input] ' + speech)
  
  return speech