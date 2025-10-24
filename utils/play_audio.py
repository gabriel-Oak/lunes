# from dimits import Dimits
import pygame
from gtts import gTTS
import os
import uuid
import threading
import queue
from utils.is_running import is_running

# dt = Dimits("pt_BR-faber-medium")

audio_lock = threading.Lock()



answers_queue = queue.Queue()

def speak_thread():
    while is_running.is_set():
        try:
            # Pega resposta da fila
            resposta = answers_queue.get(timeout=1)
            with audio_lock:  # Garante exclusividade do áudio
                speak(resposta)
            
            answers_queue.task_done()
            
        except queue.Empty:
            continue


def play_audio(speech: str):
    if is_running.is_set():
        answers_queue.put(speech)
    else:
        speak(speech)
    
def speak(text: str):
    """
    Converte texto em fala e reproduz usando pygame
    """
    speech = text.strip()
    if speech == '':
        return
    file_name = 'audios/tts_' + uuid.uuid4().hex + '.mp3'
    
    # Gerar áudio com gTTS
    tts = gTTS(speech, lang="pt-BR")
    tts.save(file_name)
    
    # Inicializar pygame mixer
    pygame.mixer.init()
    
    # Carregar e reproduzir o arquivo de áudio
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    
    # Aguardar a reprodução terminar
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
    
    # Limpar o arquivo temporário 
    if os.path.exists(file_name):
        os.remove(file_name)

def play_trigger():
    pygame.mixer.init()
    pygame.mixer.music.load('audios/trigger.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)