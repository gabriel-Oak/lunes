import json
from utils.listen import listen
from modules.iot.iot_device import IotDevice
import random
import logging
from typing import Dict, Union
from tuya_iot.openapi import TuyaTokenInfo
from utils.intent import Intent
from utils.module import Module
from utils.play_audio import play_audio
from tuya_iot import TuyaOpenAPI , tuya_logger
from decouple import config
import difflib
from re import sub

TUYA_URL = config('TUYA_URL')
TUYA_ID = config('TUYA_ID')
TUYA_SECRET = config('TUYA_SECRET')
TUYA_USER = config('TUYA_USER')
TUYA_PASS = config('TUYA_PASS')
TUYA_USER_ID = config('TUYA_USER_ID')

class IotModule(Module):
  
  def __init__(self) -> None:
    with open('modules/iot/intents.json') as iot:
      intents: dict = json.load(iot)

    for key in intents:
      intent = intents[key]
      intents[key] = Intent(
        id=key, 
        triggers=intent['triggers'], 
        answers=intent['answers'],
      )

    self.devices: Dict[str, IotDevice] = {}
    self.setup_iot()

    super().__init__(intents)

  def process_command(self, intent: str, speech: str) -> None:
    play_audio(random.choice(self.intents[intent].answers))
    if intent in ['turn_on', 'turn_off']:
      self.process_switch(intent=intent, speech=speech)

  def process_switch(self, intent: str, speech: str):
    sanitized_speech = speech
    for trigger in self.intents[intent].triggers:
      if trigger in speech: 
        sanitized_speech = sub(r'\s{2}', ' ', ''.join(sanitized_speech.split(trigger)))

    device = self.get_device(sanitized_speech)
    if not device: raise Exception('Desculpe, não encontrei: ' + sanitized_speech)

    try:
      res = self.openapi.post(
        '/v1.0/devices/{0}/commands'.format(device.id), 
        {
          'commands': [{
            'code': 'switch_led', 
            'value':  True if intent == 'turn_on' else False,
          }]
        }
      )
      if not res['success']: raise Exception()
    except Exception as e:
      print(e)
      raise Exception('Desculpe, não consegui operar o dispositivo, ele pode estar offline, tente denovo!')
      
    
  def get_device(self, speech: str) -> Union[IotDevice, None]:
    selected_device: IotDevice = None
    selected_device_diffs: int = None
    
    for key in self.devices.keys():
      diff = list(difflib.ndiff(key, speech))
      diff_count = len(list(filter(lambda i: i[0] in ['+', '-'], diff)))
      if not selected_device_diffs or diff_count < selected_device_diffs:
        selected_device_diffs = diff_count
        selected_device = self.devices[key]
        print(key)

    if selected_device_diffs <= 4:
      return selected_device

    play_audio('Você quis dizer: {0} ?'.format(selected_device.name))
    answer = listen()
    if 'sim' in answer: return selected_device
    

  def setup_iot(self):
    try:
      tuya_logger.setLevel(logging.DEBUG)
      self.openapi = TuyaOpenAPI(TUYA_URL, TUYA_ID, TUYA_SECRET)
      res = self.openapi.get('/v1.0/token?grant_type=1')
      self.openapi.token_info = TuyaTokenInfo(res)

      res = self.openapi.get('/v1.0/users/{0}/devices'.format(TUYA_USER_ID))
      if not res['success']: raise Exception(res)
      
      devices = res['result']
      for device in devices:
        self.devices[device['name'].lower()] = IotDevice(device)

    except Exception as e:
      print('Error ', e)
      play_audio('Desculpe, a funcionalidade casa inteligente não pôde iniciar, estou com algum problema!')
