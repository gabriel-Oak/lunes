import json
from utils.listen import listen
from modules.index import MODULES
from utils.play_audio import play_audio
import speech_recognition as sr
from playsound import playsound
from re import sub
from modules.ai.ai_module import AIModule

with open('intents/general.json') as general:
  general_intents = json.load(general)

ai = AIModule()

def process_command(trigger: str, speech_initial: str):
  tries = 0
  while True:
    try:
      print('[log] processando comando')
      speech: str = sub(r'\s{2}', ' ', ''.join(speech_initial.split(trigger)))
      
      if len(speech_initial) == len(trigger) or tries > 0: 
        speech = listen()

      for module in MODULES:
        intent = module.checkIntent(speech)
        if type(intent) == str: 
          return module.process_command(intent, speech)
      return ai.generateLocal(speech) 

    except sr.UnknownValueError:
      print('[log] Não entendi o quê você disse. Ou você não disse nada haha!')

    except Exception as e:
      if tries > 3: return None 
      tries += 1
      play_audio(str(e))
      playsound('audios/trigger.mp3')

def monitor():
  with ai.model.chat_session(ai.system_prompt):
    while True:
      try:
        print('[log] monitorando trigger')
        speech = listen()

        for trigger in general_intents['trigger']['triggers']:
          if trigger in speech: 
            playsound('audios/trigger.mp3')
            process_command(trigger, speech)
            break

      except sr.UnknownValueError:
        print('[log] Não entendi o quê você disse. Ou você não disse nada haha!')

      except sr.RequestError as e:
        print('[log] Error; {0}'.format(e))
        play_audio('Algo deu errado, você está conectado à internet?')

play_audio('Olá! Eu sou Lúnis!')
monitor()