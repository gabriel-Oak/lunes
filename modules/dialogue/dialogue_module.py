
import json
import random
from utils.intent import Intent
from utils.module import Module
from utils.play_audio import play_audio

class DialogueModule(Module):
  
  def __init__(self) -> None:
    with open('modules/dialogue/intents.json') as dialogue:
      intents: dict = json.load(dialogue)

    for key in intents:
      intent = intents[key]
      intents[key] = Intent(
        id=key, 
        triggers=intent['triggers'], 
        answers=intent['answers'],
      )

    super().__init__(intents)

  def process_command(self, intent: str, speech: str) -> None:
    answer = random.choice(self.intents[intent].answers)
    print('[dialogue]', answer)
    play_audio(answer)
    return False
