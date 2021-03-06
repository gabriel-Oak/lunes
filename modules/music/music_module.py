
import json
import random
from typing import Dict, List, Union
import webbrowser as browser 
from utils.intent import Intent
from utils.module import Module
from utils.play_audio import play_audio
from spotify2py import Spotify
from decouple import config

SPOTIFY_ID = config('SPOTIFY_ID')
SPOTIFY_SECRET = config('SPOTIFY_SECRET')

with open('intents/music.json') as intents:
  music_intents: dict = json.load(intents)
  
class MusicModule(Module):
  
  def __init__(self) -> None:
    with open('modules/music/intents.json') as music:
      intents: dict = json.load(music)

    for key in intents:
      intent = intents[key]
      intents[key] = Intent(
        id=key, 
        triggers=intent['triggers'], 
        answers=intent['answers'],
      )

    self.token = Spotify().get_token()
    self.spotify = Spotify(token=self.token)
    super().__init__(intents)

  def process_command(self, intent: str, speech: str) -> None:
    intention = self.get_intention(speech=speech)
    try:
      if not intention or intention['query'] == 'música':
        play_audio(random.choice(self.intents['playlist']['answers']))
        browser.open('https://open.spotify.com/collection/tracks')
      else:

        if intention['intent'] == 'music': 
          self.spotify.play(intention['query'])
          play_audio(
            random.choice(music_intents['music']['answers']) + intention['query']
          )
        elif intention['intent'] == 'artist':
          artist = self.spotify.get_artist(intention['query'])
          play_audio(
            random.choice(music_intents['artist']['answers']) + artist['name']
          )
          browser.open(artist['artist_url'])
        elif intention['intent'] == 'album':
          album = self.spotify.get_album(intention['query'])
          play_audio(
            random.choice(music_intents['album']['answers']) + album['name']
          )
          browser.open(album['album_url'])
        else:
          browser.open('https://open.spotify.com/search/{0}'.format(intention['query']))        
          play_audio(random.choice(self.intents['playlist']['answers']))

    except Exception as e:
      print(e)
      raise Exception('Desculpe, não consegui reproduzir.')

  def get_intention(self, speech: str) -> Union[Dict[str, str], None]:
    res = None
    for key in music_intents.keys():
      for trigger in music_intents[key]['triggers']:
        if trigger in speech:
          query = speech.split(trigger)
          if len(query) < 2: 
            raise Exception('Não consegui identificar o pedido, desculpe!')
          res = { 'query': query[1], 'intent': key }
          if key != 'music': break

    return res