#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import StringIO
import json
import logging
import random
import urllib
import urllib2

# functions
import responseHandler

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

# global variables
from config import TOKEN
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        location = message.get('location')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        # location - weather

        if location:
            lat = location.get('latitude')
            lon = location.get('longitude')
            weather = responseHandler.locationInput(lat, lon)
            responseHandler.sendWeather(chat_id, weather)
            return
        

        # command

        if text:
            if text.startswith('/'):
                if text.lower() == '/start':
                    responseHandler.sendTextMessage(chat_id, '幸会。')
                    setEnabled(chat_id, True)
                # 待办：最好把这里做成每晚定时
                elif text.lower() == '/weathertmr':
                    LAT = 57.63
                    LON = 18.31
                    weather = responseHandler.locationInput(LAT, LON)
                    responseHandler.forecastWeather(chat_id, weather)
                elif text.lower() == '/stop':
                    responseHandler.sendTextMessage(chat_id, '好，下次再说。')
                    setEnabled(chat_id, False)
                else:
                    responseHandler.sendTextMessage(chat_id, '什么？')
            else:
                responseHandler.replyMessage(chat_id, message_id, '嗯')

    

app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)

