# from dimits import Dimits
import pygame
from gtts import gTTS
import os

# dt = Dimits("pt_BR-faber-medium")

file_name = 'audios/tts.mp3'

def play_audio(speech: str):
    """
    Converte texto em fala e reproduz usando pygame
    """
    # print('[output] ' + speech)
    # dt.text_2_speech(speech, engine="aplay")
    
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
    
    # Limpar o arquivo temporário (opcional)
    if os.path.exists(file_name):
        os.remove(file_name)

def play_trigger():
    pygame.mixer.init()
    pygame.mixer.music.load('audios/trigger.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)