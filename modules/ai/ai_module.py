import re
from gpt4all import GPT4All
from utils.play_audio import play_audio

system_prompt = "Seu nome é Lunis, você é uma IA personalizada por Gabriel Carvalho para ser uma assistente virtual. Seu papel é ajudar o usuário sempre respondendo em português do Brasil. Você nunca usará palavras em inglês. Procure responder com frases curtas caso possível."
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

class AIModule:
  
  def __init__(self) -> None:
    self.system_prompt = system_prompt
    self.load_model()
      
  def load_model(self):
    self.model = GPT4All(model_name)
    
  def start_session(self):
    print('[log] iniciando sessão com AI')
    return self.model.chat_session(self.system_prompt)

  def generateLocal(self, speech: str) -> None:
    print('[log] gerando resposta com AI')
    result = ''
    try:
      for token in self.model.generate(speech, max_tokens=1024, streaming=True, ):
        result += re.sub(r'(\n)|[*]', ' ', token, flags=re.M)
        print(result, end="\r")
      print("")
      play_audio(result)

    except Exception as e:
      print(e)
      raise Exception('Não consegui gerar uma resposta, desculpe')
