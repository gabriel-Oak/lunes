from modules.fun.fun_module import FunModule
from typing import List
from utils.module import Module
from modules.dialogue.dialogue_module import DialogueModule

MODULES: List[Module] = [
  FunModule(),
  DialogueModule(),
]