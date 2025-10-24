from utils.play_audio import play_audio, audio_lock, answers_queue
import speech_recognition as sr
import json
import time


def create_listener(callback):
  def listener(recognizer, audio):
    try:
      speech = recognizer.recognize_google(audio, language='pt-BR')
      print('[input] ' + speech)
      callback(speech.lower())
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
  progress = ['-', '\\', '|', '/']
  index = 0
  
  # Aguardar fila de reprodução esvaziar
  while not answers_queue.empty():
    print('[log] Aguardando fila de reprodução esvaziar... ' + progress[index] + ' ' + str(answers_queue.qsize()), end='\r')
    index += 1
    if index >= len(progress):
      index = 0
    time.sleep(0.5)
  
  # Delay de segurança para garantir que terminou de falar
  time.sleep(0.3)
  
  # Aguardar se estiver falando e escutar com exclusividade
  with audio_lock:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
      recognizer.adjust_for_ambient_noise(source)
      audio = recognizer.listen(source)
    
  speech = recognizer.recognize_google(audio, language='pt-BR')
  print('[input] ' + speech)
  
  return speech.lower()