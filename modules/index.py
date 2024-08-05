# from modules.iot.iot_module import IotModule
# from modules.music.music_module import MusicModule
from modules.news.news_module import NewsModule
from modules.fun.fun_module import FunModule
from typing import List
from utils.module import Module
from modules.dialogue.dialogue_module import DialogueModule

MODULES: List[Module] = [
  FunModule(),
  DialogueModule(),
  NewsModule(),
  # MusicModule(),
  # IotModule()
]