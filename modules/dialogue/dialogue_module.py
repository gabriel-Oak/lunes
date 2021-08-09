
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

  def processCommand(self, intent: str, speech: str) -> None:
    play_audio(random.choice(self.intents[intent].answers))
