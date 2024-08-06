from gpt4all import GPT4All
from utils.play_audio import play_audio
    
class AIModule:
  
  def __init__(self) -> None:
    self.model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    self.session = self.model.chat_session()

  def generate(self, speech: str) -> None:
    print('[log] gerando resposta com AI')
    result = ''
    try:
      for token in self.model.generate(speech, max_tokens=100, streaming=True, ):
        result += token
        print(result)
      play_audio(result)

    except Exception as e:
      print(e)
      raise Exception('Não consegui gerar uma resposta, desculpe')
