
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

  def processJoke(self, speech: str) -> None:
    play_audio(random.choice(self.intents['joke'].answers))
    belong = None
    joke = None
    for trigger in belongs:
      if trigger in speech:
        belong = trigger.replace(' ', '')
        break

    if belong:
      category = speech.split(' ')
      i = category.index(belong) + 1
      if i > len(category):
        raise Exception('Desculpe, não entendi o tipo da piada, por favor, tente de novo!')

      category = category[i]
      filteredJokes = list(filter(
        lambda joke: category in joke['category'].lower(), 
        jokes,
      ))
      joke = random.choice(filteredJokes)
    else:
      joke = random.choice(jokes)

    for phrase in joke['joke']:
      play_audio(phrase)

  def processCommand(self, intent: str, speech: str) -> None:
    if (intent == 'joke'): self.processJoke(speech=speech)
    else: play_audio(random.choice(self.intents[intent].answers))

    
