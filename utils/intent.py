from typing import List


class Intent:
  'Intents define what user want'

  def __init__(self, id: str, triggers: List[str], answers: List[str]) -> None:
    self.id = id
    self.triggers = triggers
    self.answers = answers