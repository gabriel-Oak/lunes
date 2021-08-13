from typing import Dict, Hashable, List, Union
from utils.intent import Intent


class Module:
  'Base module class'
  
  def __init__(self, intents: Dict[str, Intent]) -> None:
      self.intents = intents

  def process_command(self, intent: str, speech: str) -> None:
    return

  def checkIntent(self, speech: str) -> Union[str, None]:
    for intent in self.intents:
      for trigger in self.intents[intent].triggers:
        if trigger in speech: return intent

