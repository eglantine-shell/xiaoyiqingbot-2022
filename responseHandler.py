#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import urllib2
import json
import StringIO

# standard app engine imports
import logging

# global variables
from config import TOKEN
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

# for weather forecast
from config import WEATHER_API_KEY
WEATHER_BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall?'
WEATHER_UNITS = 'metric'
WEATHER_LANG = 'zh_cn'

def replyMessage (chat_id, msg_id, text=None):
    if (text):
        resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': text.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(msg_id)
                })).read()
        logging.info('reply to message:')
        logging.info(resp)
    else:
        logging.warning('replyMessage Error')

def sendTextMessage (chat_id, text=None):
    if text:
        resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': text.encode('utf-8'),
                    'disable_web_page_preview': 'true'
                })).read()
        logging.info('send text message:')
        logging.info(resp)
    else:
        logging.warning('sendTextMessage Error')

# location - weather

def locationInput (lat, lon):
    if not lat or not lon:
        logging.warning('No lat or lng input')
    try:
        urlEncode = {
            'lat': str(lat),
            'lon': str(lon),
            'APPID': WEATHER_API_KEY,
            'units': WEATHER_UNITS,
            'lang': WEATHER_LANG
        }
        WEATHER_URL = WEATHER_BASE_URL + urllib.urlencode(urlEncode)
        weather = json.load(urllib2.urlopen(WEATHER_URL))
        return weather
    except Exception as e:
        logging.warning('locationInput Error:' + str(e))

def sendWeather (chat_id, weather):
    temp = weather.get('current').get('feels_like')
    main = weather.get('current').get('weather')[0].get('main')
    description = weather.get('current').get('weather')[0].get('description')
    resp = '现在的体感温度是' + str(temp) + '度，' + main + '：' + description
    sendTextMessage(chat_id, resp)

def forecastWeather (chat_id, weather):
    tempMax = weather.get('daily')[0].get('temp').get('max')
    tempMin = weather.get('daily')[0].get('temp').get('min')
    tempFeel = weather.get('daily')[0].get('feels_like').get('day')
    main = weather.get('daily')[0].get('weather')[0].get('main')
    description = weather.get('daily')[0].get('weather')[0].get('description')
    resp = '明日气温' + str(tempMin) + '-' + str(tempMax) + '度，白天体感温度' + str(tempFeel) + '度，' + main + '：' + description
    sendTextMessage(chat_id, resp)