from modules.index import MODULES
from utils.play_audio import play_audio
import speech_recognition as sr
import json
import random

with open('intents/general.json') as general:
  general_intents = json.load(general)

def process_command():
  while True:
    try:
      print('[log] processando comando')
      speech: str = listen()
      print('[input] ' + speech)

      for module in MODULES:
        intent = module.checkIntent(speech)
        if type(intent) == str: 
          return module.processCommand(intent, speech)

      play_audio('Não entendi, tente de novo!')
    except:
      return print('[log] Não entendi, tente de novo!')
        

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
          play_audio(random.choice(general_intents['trigger']['answers']))
          process_command()
          break

    except sr.UnknownValueError:
      print('[log] Não entendi o quê você disse. Ou você não disse nada haha!')

    except sr.RequestError as e:
      print('[log] Error; {0}'.format(e))
      play_audio('Algo deu errado, você está conectado à internet?')

play_audio('Olá! Eu sou Lunes!')
monitor()