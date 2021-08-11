
import json
from posixpath import expanduser
import random
from utils.intent import Intent
from utils.module import Module
from utils.play_audio import play_audio
from requests import get
from bs4 import BeautifulSoup

class NewsModule(Module):
  
  def __init__(self) -> None:
    with open('modules/news/intents.json') as news:
      intents: dict = json.load(news)

    for key in intents:
      intent = intents[key]
      intents[key] = Intent(
        id=key, 
        triggers=intent['triggers'], 
        answers=intent['answers'],
      )

    super().__init__(intents)

  def processCommand(self, intent: str, speech: str) -> None:
    try:
      source = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419')
      news = BeautifulSoup(source.text, 'html.parser')

      play_audio(random.choice(self.intents[intent].answers))
      for item in news.findAll('item')[:3]:
        title = item.title.text
        play_audio(title)
    except Exception as e:
      print(e)
      raise Exception('Não consegui buscar as notícias, desculpe')
