import requests
import json
import time
from dejavu import Dejavu
from dejavu.recognize import MicrophoneRecognizer

config = {
  "database": {
    "host": "127.0.0.1",
    "user": "root",
    "passwd": "password",
    "db": "dejavu",
  }
}

url = "https://na-hackathon-api.arrayent.io:443/v3/devices/33554440"

payload = "[{\"DeviceAction\": \"heater_temp_1=100\" }]"

headers = {
    'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiIzZmUzOTlkMC0wMTMzLTExZTctOTIwNy1iNWMzYjY2M2Y2YTQiLCJlbnZpcm9ubWVudF9pZCI6Ijk0OGUyY2YwLWZkNTItMTFlNi1hZTQ2LTVmYzI0MDQyYTg1MyIsInVzZXJfaWQiOiI5MDAwMDgyIiwic2NvcGVzIjoie30iLCJncmFudF90eXBlIjoiYXV0aG9yaXphdGlvbl9jb2RlIiwiaWF0IjoxNDg4NjcxMjgzLCJleHAiOjE0ODk4ODA4ODN9.hv_XzU1buSjBBpLkBRkuArMtk6w7EiI_BvRfdWW7rKH3h6p2ax6qMQXBSa0f-ZoeVef_J_FNQ4RSJSQaLegagw",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "6bfd9967-ee5b-a1e7-b508-6afe09c00a93"
}

learn_music = ['ToiletFlush']

def start_febreze():
  djv = Dejavu(config)
  for ele in learn_music:
    djv.fingerprint_file('mp3/'+str(ele)+'.mp3')
  print('Sleeping for 5 seconds')
  time.sleep(5)
  print('Listening for sounds')
  song = djv.recognize(MicrophoneRecognizer, seconds=10)
  print(song)
  if song['song_name'] in learn_music and song['confidence'] > 500:
    response = requests.request("PUT", url, data=payload, headers=headers)
    temp = json.loads(response.text)
    if str(temp['status']) == 'OK':
      print('Dispensed Febreze')
  

if __name__ == '__main__':
  start_febreze()
