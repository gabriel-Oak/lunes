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
from re import sub, findall

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

  def get_device(self, speech: str) -> IotDevice:
    selected_device: IotDevice = None
    selected_device_diffs: int = None
    
    for key in self.devices.keys():
      diff = list(difflib.ndiff(key, speech))
      diff_count = len(list(filter(lambda i: i[0] in ['+', '-'], diff)))
      if not selected_device_diffs or diff_count < selected_device_diffs:
        selected_device_diffs = diff_count
        selected_device = self.devices[key]

    if selected_device_diffs <= 6:
      return selected_device

    play_audio('Você quis dizer: {0} ?'.format(selected_device.name))
    answer = listen()
    if 'sim' in answer: return selected_device
    raise Exception('Desculpe, não encontrei: ' + speech)

  def get_code(self, device: IotDevice, keyword: str) -> str:
    code = None
    for status in device.status:
      if keyword in status.code: 
        code = status.code
    if code: return code
    raise Exception('Desculpe, não encontrei o comando no dispositivo, procurei por: ' + keyword)


  def sanitize_speech(self, speech: str, intent: str ):
    sanitized_speech = speech
    for trigger in self.intents[intent].triggers:
      if trigger in speech: 
        sanitized_speech = sub(r'\s{2}', ' ', ''.join(sanitized_speech.split(trigger)))
    return sanitized_speech

  def process_switch(self, intent: str, speech: str):
    numbers: list = findall('[0-9]+', str)
    if len(numbers) < 1: raise Exception('Vixe, não encontrei o valor da temperatura não')
    temperature = int(numbers.pop())

    sanitized_speech = self.sanitize_speech(
      speech=sub(r'\s{2}', ' ', ''.join(speech.split(str(temperature)))), 
      intent=intent
    )
    device = self.get_device(sanitized_speech)
    code = self.get_code(device=device, keyword='switch')

    try:
      play_audio(random.choice(self.intents[intent].answers))
      res = self.openapi.post(
        '/v1.0/devices/{0}/commands'.format(device.id), 
        {
          'commands': [{
            'code': code, 
            'value':  temperature,
          }]
        }
      )
      if not res['success']: raise Exception()
    except Exception as e:
      print(e)
      raise Exception('Desculpe, não consegui operar o dispositivo, ele pode estar offline, tente denovo!')    

  def process_temperature(self, intent: str, speech: str):
    sanitized_speech = self.sanitize_speech(speech=speech, intent=intent)
    device = self.get_device(sanitized_speech)
    code = self.get_code(device=device, keyword='temp')

  def process_command(self, intent: str, speech: str) -> None:
    if intent in ['turn_on', 'turn_off']:
      return self.process_switch(intent=intent, speech=speech)

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
