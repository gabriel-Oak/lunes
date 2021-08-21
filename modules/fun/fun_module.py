
import json
import random
from typing import List
from utils.intent import Intent
from utils.module import Module
from utils.play_audio import play_audio

with open('modules/fun/jokes.json') as jokes:
  jokes: List[dict] = list(json.load(jokes))

with open('intents/general.json') as intents:
  belongs: List[str] = list(json.load(intents)['belongs']['triggers'])

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

  def process_joke(self, speech: str) -> None:
    play_audio(random.choice(self.intents['joke'].answers))
    joke = random.choice(jokes)

    for trigger in belongs:
      if trigger in speech:
        query = speech.split(trigger)
        if len(query) < 2: 
          raise Exception('Desculpe, não entendi o tipo da piada, por favor, tente de novo!')
        filteredJokes = list(filter(
          lambda joke: query[1] in joke['category'].lower(), 
          jokes,
        ))
        joke = random.choice(filteredJokes)
      break

    for phrase in joke['joke']:
      play_audio(phrase)

  def process_command(self, intent: str, speech: str) -> None:
    if (intent == 'joke'): self.process_joke(speech=speech)
    else: play_audio(random.choice(self.intents[intent].answers))

    
