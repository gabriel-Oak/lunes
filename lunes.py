import json
import random
from modules.index import MODULES
from utils.play_audio import play_audio
import speech_recognition as sr
from playsound import playsound

with open('intents/general.json') as general:
  general_intents = json.load(general)

def process_command():
  tryies = 0
  while True:
    try:
      print('[log] processando comando')
      speech: str = listen()
      print('[input] ' + speech)

      for module in MODULES:
        intent = module.checkIntent(speech)
        if type(intent) == str: 
          return module.processCommand(intent, speech)
      raise Exception('Não entendi, tente de novo!')

    except sr.UnknownValueError:
      print('[log] Não entendi o quê você disse. Ou você não disse nada haha!')

    except Exception as e:
      if tryies > 3: return None 
      tryies += 1
      play_audio(str(e))
      
        

def listen() -> str:
  mic = sr.Recognizer()
  with sr.Microphone() as source:
    audio = mic.listen(source)
  return mic.recognize_google(audio, language='pt-BR').lower()

def monitor():
  while True:
    try:
      print('[log] monitorando trigger')
      speech = listen()
      print('[input] ' + speech)

      for trigger in general_intents['trigger']['triggers']:
        if trigger in speech: 
          playsound('audios/trigger.mp3')
          process_command()
          break

    except sr.UnknownValueError:
      print('[log] Não entendi o quê você disse. Ou você não disse nada haha!')

    except sr.RequestError as e:
      print('[log] Error; {0}'.format(e))
      play_audio('Algo deu errado, você está conectado à internet?')

play_audio('Olá! Eu sou Lunes!')
monitor()