from pickle import TRUE
import re
from gpt4all import GPT4All
from utils.console_utils import clear_screen
from utils.play_audio import play_audio

system_prompt = "Seu nome é Lunis, você é uma IA personalizada por Gabriel Carvalho para ser uma assistente virtual. Seu papel é ajudar o usuário sempre respondendo em português do Brasil. Você nunca usará palavras em inglês. Procure responder com frases curtas caso possível."
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

class AIModule:
  
  def __init__(self) -> None:
    self.system_prompt = system_prompt
    self.load_model()
      
  def load_model(self):
    self.model = GPT4All(model_name, allow_download=False)
    
  def start_session(self):
    print('[log] iniciando sessão com AI')
    return self.model.chat_session(self.system_prompt)

  def generateLocal(self, speech: str) -> bool:
    print('[log] gerando resposta com AI')
    accumulated_result = ''
    processing_result = ''
    
    try:
      for token in self.model.generate(speech, max_tokens=1024, streaming=True, ):
        sanitized_token = re.sub(r'(\n)|[*]', ' ', token, flags=re.M)
        accumulated_result += sanitized_token
        processing_result += sanitized_token
        match = re.search(r'[.!?,;:-]', processing_result)
        
        if match:
          phrase = processing_result[:match.start()].strip()
          if phrase:
            play_audio(phrase)
          processing_result = processing_result[match.end():].strip()
        clear_screen()
        print(accumulated_result)
      
      if len(processing_result) > 0:
        play_audio(processing_result)
      # play_audio(accumulated_result)
      if '?' in accumulated_result:
        return True
      return False

    except Exception as e:
      print(e)
      raise Exception('Não consegui gerar uma resposta, desculpe')
