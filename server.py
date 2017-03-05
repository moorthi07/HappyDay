#!/usr/bin/env python3

import json
import os
import random
import time

import requests
from japronto import Application

FEBREZE_URL = 'https://na-hackathon-api.arrayent.io/v3/devices/33554440'
FEBREZE_HEADERS = {
	'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiIzZmUzOTlkMC0wMTMzLTExZTctOTIwNy1iNWMzYjY2M2Y2YTQiLCJlbnZpcm9ubWVudF9pZCI6Ijk0OGUyY2YwLWZkNTItMTFlNi1hZTQ2LTVmYzI0MDQyYTg1MyIsInVzZXJfaWQiOiI5MDAwMDgyIiwic2NvcGVzIjoie30iLCJncmFudF90eXBlIjoiYXV0aG9yaXphdGlvbl9jb2RlIiwiaWF0IjoxNDg4NjcxMjgzLCJleHAiOjE0ODk4ODA4ODN9.hv_XzU1buSjBBpLkBRkuArMtk6w7EiI_BvRfdWW7rKH3h6p2ax6qMQXBSa0f-ZoeVef_J_FNQ4RSJSQaLegagw",
	'content-type': "application/json",
}

FEBREZE_ACTIONS = {
	'LIGHT_ON': {'DeviceAction': 'led_mode=1'},
	'LIFTH_OFF': {'DeviceAction': 'led_mode=0'},
	'COLOR_GREEN': {'DeviceAction': 'led_color=0,1,4,4,4'},
	'COLOR_EMERALD': {'DeviceAction': 'led_color=0,5,4,4,4'},
	'COLOR_FREE_GREEN': {'DeviceAction': 'led_color=0,6,4,4,4'},
	'COLOR_SPRING': {'DeviceAction': 'led_color=0,7,4,4,4'},
	'COLOR_AQUA': {'DeviceAction': 'led_color=0,2,4,4,4'},
	'COLOR_DODGER': {'DeviceAction': 'led_color=0,8,4,4,4'},
	'COLOR_BLUE2': {'DeviceAction': 'led_color=0,9,4,4,4'},
	'COLOR_BLUE': {'DeviceAction': 'led_color=0,10,4,4,4'},
	'COLOR_PURPLE': {'DeviceAction': 'led_color=0,11,4,4,4'},
	'COLOR_ELECTRIC': {'DeviceAction': 'led_color=0,12,4,4,4'},
	'COLOR_MAGENTA': {'DeviceAction': 'led_color=0,3,4,4,4'},
	'COLOR_WHITE': {'DeviceAction': 'led_color=0,4,4,4,4'},
	'COLOR_SUN': {'DeviceAction': 'led_color=0,13,4,4,4'},
	'COLOR_ICE': {'DeviceAction': 'led_color=0,14,4,4,4'}
}

FEBREZE_COLORS = list(filter(lambda x: 'COLOR' in x, FEBREZE_ACTIONS.keys()))


def default(request):
	"""
	Index route just retuns smple response
	:param request: 
	:return: 
	"""
	return request.Response(text='Hello world!')


def play(request):
	"""
	This will handle the schedule request for IFTTT trigger and plays corresponding audio
	:param request: 
	:return: 
	"""
	os.system('say -v Samantha "Alexa"')
	time.sleep(1)

	title = request.json['Title'].lower()

	if 'birthday' in title:
		os.system('say -v Samantha "celebrate birthday"')
	elif 'romance' in title:
		os.system('say -v Samantha "celebrate romance"')
	elif 'party' in title:
		os.system('say -v Samantha "celebrate party"')

	return request.Response(json={'success': True})


def parse_alexa(request):
	"""
	This is handler for Echo skill which takes request from Echo and responds with appropriate audo files
	:param request: 
	:return: 
	"""
	if request.json['request']['type'] != 'IntentRequest':
		# Invalid intet type so can't do anything with it
		return request.Response(json={
			'version': '1.0',
			'response': {
				'outputSpeech': {
					'type': 'PlainText',
					'text': "I can't understand you"
				},
				'shouldEndSession': True
			}
		})
	intent = request.json['request']['intent']

	if intent['name'] not in ['Romance']:
		return request.Response(code=200)

	if intent['name'] == 'Romance':
		occation = intent['slots']['occation']['value'].lower()
		if occation == 'party':
			return play_party(request)
		if occation == 'lullaby':
			return play_lullaby(request)
		if occation in ['happy birthday', 'happy', 'birthday', 'birth day']:
			return play_birtyday(request)

		response = {
			"version": "1.0",
			"sessionAttributes": {},
			"response": {
				"outputSpeech": {
					"type": "PlainText",
					"text": "Can't play the requested song. Something interesting though..."
				},
				"card": {
					"type": "Simple",
					"title": "Play Audio",
					"content": "Playing the requested song."
				},
				"reprompt": {
					"outputSpeech": {
						"type": "PlainText",
						"text": None
					}
				},
				"directives": [
					{
						"type": "AudioPlayer.Play",
						"playBehavior": "REPLACE_ALL",
						"audioItem": {
							"stream": {
								"token": "7b94d4ea-c60a-4df0-99dd-5e6156eea2d4",
								"url": "https://moorthi07.github.io/HappyDay/Lullaby.mp3",
								"offsetInMilliseconds": 0
							}
						}
					}
				],
				"shouldEndSession": True
			}
		}
		return request.Response(json=response)


def play_lullaby(request):
	response = {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			"outputSpeech": {
				"type": "PlainText",
				"text": None
			},
			"card": {
				"type": "Simple",
				"title": "Play Audio",
				"content": "Playing lullaby song."
			},
			"reprompt": {
				"outputSpeech": {
					"type": "PlainText",
					"text": None
				}
			},
			"directives": [
				{
					"type": "AudioPlayer.Play",
					"playBehavior": "REPLACE_ALL",
					"audioItem": {
						"stream": {
							"token": "7b94d4ea-c60a-4df0-99dd-5e6156eea2d4",
							"url": "https://moorthi07.github.io/HappyDay/Lullaby.mp3",
							"offsetInMilliseconds": 0
						}
					}
				}
			],
			"shouldEndSession": True
		}
	}
	request.Response(json=response)

	payload = [FEBREZE_ACTIONS['LIGHT_ON']]
	r = requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))
	for i in range(100):
		payload = [FEBREZE_ACTIONS[random.choice(FEBREZE_COLORS)]]
		requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))
		time.sleep(0.3)
	payload = [FEBREZE_ACTIONS['LIFTH_OFF']]
	requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))


def play_party(request):
	"""
	Play party scenes 
	:param request: 
	:return: 
	"""
	response = {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			"outputSpeech": {
				"type": "PlainText",
				"text": None
			},
			"card": {
				"type": "Simple",
				"title": "Play Audio",
				"content": "Playing party song."
			},
			"reprompt": {
				"outputSpeech": {
					"type": "PlainText",
					"text": None
				}
			},
			"directives": [
				{
					"type": "AudioPlayer.Play",
					"playBehavior": "REPLACE_ALL",
					"audioItem": {
						"stream": {
							"token": "7b94d4ea-c60a-4df0-99dd-5e6156eea2d4",
							"url": "https://moorthi07.github.io/HappyDay/HappyMichaelJacksonBad.mp3",
							"offsetInMilliseconds": 0
						}
					}
				}
			],
			"shouldEndSession": True
		}
	}
	request.Response(json=response)

	payload = [FEBREZE_ACTIONS['LIGHT_ON']]

	r = requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))
	for i in range(100):
		payload = [FEBREZE_ACTIONS[random.choice(FEBREZE_COLORS)]]
		requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))
		time.sleep(0.1)
	payload = [FEBREZE_ACTIONS['LIFTH_OFF']]
	requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))


def play_birtyday(request):
	response = {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			"outputSpeech": {
				"type": "PlainText",
				"text": None
			},
			"card": {
				"type": "Simple",
				"title": "Play Audio",
				"content": "Playing party song."
			},
			"reprompt": {
				"outputSpeech": {
					"type": "PlainText",
					"text": None
				}
			},
			"directives": [
				{
					"type": "AudioPlayer.Play",
					"playBehavior": "REPLACE_ALL",
					"audioItem": {
						"stream": {
							"token": "7b94d4ea-c60a-4df0-99dd-5e6156eea2d4",
							"url": "https://moorthi07.github.io/HappyDay/HappyMichaelJacksonBad.mp3",
							"offsetInMilliseconds": 0
						}
					}
				}
			],
			"shouldEndSession": True
		}
	}
	request.Response(json=response)

	payload = [FEBREZE_ACTIONS['LIGHT_ON']]

	r = requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))
	for i in range(100):
		payload = [FEBREZE_ACTIONS[random.choice(FEBREZE_COLORS)]]
		requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))
		time.sleep(0.1)
	payload = [FEBREZE_ACTIONS['LIFTH_OFF']]
	requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))

def play_romance(request):
	response = {
		"version": "1.0",
		"sessionAttributes": {},
		"response": {
			"outputSpeech": {
				"type": "PlainText",
				"text": None
			},
			"card": {
				"type": "Simple",
				"title": "Play Audio",
				"content": "Playing party song."
			},
			"reprompt": {
				"outputSpeech": {
					"type": "PlainText",
					"text": None
				}
			},
			"directives": [
				{
					"type": "AudioPlayer.Play",
					"playBehavior": "REPLACE_ALL",
					"audioItem": {
						"stream": {
							"token": "7b94d4ea-c60a-4df0-99dd-5e6156eea2d4",
							"url": "https://moorthi07.github.io/HappyDay/Greesleeves_Mantovani.mp3",
							"offsetInMilliseconds": 0
						}
					}
				}
			],
			"shouldEndSession": True
		}
	}
	request.Response(json=response)

	payload = [FEBREZE_ACTIONS['LIGHT_ON']]

	r = requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))
	for i in range(100):
		payload = [FEBREZE_ACTIONS['LIFTH_OFF'], FEBREZE_ACTIONS[random.choice(FEBREZE_COLORS)]]
		requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))
		time.sleep(0.1)
	payload = [FEBREZE_ACTIONS['LIFTH_OFF']]
	requests.put(FEBREZE_URL, headers=FEBREZE_HEADERS, data=json.dumps(payload))

def parse_recognition(request):
	"""
	:param request: 
	:return: 
	"""
	if 'type' not in request.query:
		return request.Response(code=200)
	if request.query['type'].lower() == 'bark':
		os.system('say -v Samantha "Alexa"')
		time.sleep(1)
		os.system('say -v Samantha "play scene bark from Happy Day"')
	else:
		os.system('say -v Samantha "Alexa"')
		time.sleep(1)
		os.system('say -v Samantha "play scene lalubaby from Happy Day"')

	return request.Response(code=200)


app = Application()

app.router.add_route('/', default, method='GET')
app.router.add_route('/', parse_alexa, method='POST')
app.router.add_route('/calendar', play, method='POST')
app.router.add_route('/alexa', parse_alexa, method='POST')
app.router.add_route('/play', parse_recognition, method='GET')

app.run(debug=True, port=4000)
