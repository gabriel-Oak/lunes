import json
import threading
import time
from utils.is_running import is_running
from utils.listen import listen
from modules.index import MODULES
from utils.play_audio import play_audio, play_trigger, speak_thread
import speech_recognition as sr
from re import sub
from modules.ai.ai_module import AIModule

speakThread = threading.Thread(target=speak_thread, daemon=True)
speakThread.start()

with open('intents/general.json') as general:
  general_intents = json.load(general)

ai = AIModule()

def process_command(trigger: str, speech_initial: str) -> bool:
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
          return module.process_command(intent, speech).__bool__()
      return ai.generateLocal(speech) 

    except sr.UnknownValueError:
      print('[log] Não entendi o quê você disse. Ou você não disse nada haha!')

    except Exception as e:
      if tries > 3: return None 
      tries += 1
      play_audio(str(e))
      play_trigger()

def monitor():
  with ai.start_session():
    continueConversation = False
    while True:
      try:
        if continueConversation:
          continueConversation = process_command(speech, speech)
        else:
          print('[log] monitorando trigger')
          speech = listen()

          for trigger in general_intents['trigger']['triggers']:
            if trigger in speech: 
              play_trigger()
              continueConversation = process_command(trigger, speech)
              break

      except sr.UnknownValueError:
        print('[log] Não entendi o quê você disse. Ou você não disse nada haha!')

      except sr.RequestError as e:
        print('[log] Error; {0}'.format(e))
        play_audio('Algo deu errado, você está conectado à internet?')
        
      except KeyboardInterrupt:
        print("\n ⚠️  \033[1mEncerrando...\033[0m")
        is_running.clear()
        time.sleep(0.3)
        break

play_audio('Olá! Eu sou Lúnis!')
monitor()

is_running.clear()