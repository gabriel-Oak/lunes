
import json
import random
from typing import List
from utils.intent import Intent
from utils.module import Module
from utils.play_audio import play_audio

class FunModule(Module):
  
  def __init__(self) -> None:
    with open('modules/fun/intents.json') as fun:
      intents: dict = json.load(fun)

    for key in intents:
      intent = intents[key]
      intents[key] = Intent(
        id=key, 
        triggers=intent['triggers'], 
        answers=intent['answers'],
      )

    super().__init__(intents)

  def processJoke(self) -> None:
    play_audio(random.choice(self.intents['joke'].answers))
    
    with open('modules/fun/jokes.json') as jokes:
      jokes: List[dict] = list(json.load(jokes))
      
    joke = random.choice(jokes)
    for phrase in joke['joke']:
      play_audio(phrase)

  def processCommand(self, intent: str, speech: str) -> None:
    if (intent == 'joke'): self.processJoke()
    else: play_audio(random.choice(self.intents[intent].answers))

    
