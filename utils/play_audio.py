from playsound import playsound
import boto3

file_name = 'audios/tts.mp3'
polly = boto3.Session(
  aws_access_key_id='AKIA2YRYCDRJBXS6QS7M',                     
  aws_secret_access_key='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',
  region_name='us-west-2'
).client('polly')


def play_audio(speech: str):
  print('[output] ' + speech)
  response = polly.synthesize_speech(
    Text = speech, 
    OutputFormat = "mp3", 
    VoiceId = 'Camila', 
  )
  body = response['AudioStream'].read()

  with open(file_name, 'wb') as file:
    file.write(body)
    file.close()
    
  playsound('audios/tts.mp3')
