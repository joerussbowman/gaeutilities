'''
Copyright (c) 2008, appengine-utilities project
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the appengine-utilities project nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import os, cgi, __main__
from google.appengine.ext.webapp import template
from appengine_utilities import sessions
from appengine_utilities import flash
from appengine_utilities import event
from appengine_utilities import cache
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import memcache

class MainPage(webapp.RequestHandler):
  def __init__(self):
    self.test = "event not fired"

  def get(self):
    template_values = {
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, template_values))

class FlashPage(webapp.RequestHandler):
  def get(self):
    self.flash = flash.Flash()
    if self.request.get('setflash') == "true":
        self.flash.msg = 'You set a flash message! <a href="/flash">Refresh this page</a> and this message is gone!'
        print "Location: /flash\n\n"
    else:
        template_values = {
            'flash': self.flash,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/flash.html')
        self.response.out.write(template.render(path, template_values))

class AjaxSessionPage(webapp.RequestHandler):
  def get(self):
    self.sess = sessions.Session()
    if not 'viewCount' in self.sess:
      self.sess['viewCount'] = 1
    else:
      self.sess['viewCount'] = int(self.sess['viewCount']) + 1
    self.response.out.write('viewcount is ' + str(self.sess['viewCount']))

class SessionPage(webapp.RequestHandler):
  def get(self):
    self.sess = sessions.Session()
    self.cookie_sess = sessions.Session(writer="cookie")
    if self.request.get('deleteSession') == "true":
        self.sess.delete()
        print "Location: /session\n\n"
    elif self.request.get('setflash') == "true":
        self.sess['flash'] = 'You set a flash message! <a href="/session">Refresh this page</a> and this message is gone!'
        print "Location: /session\n\n"
    else:
        keyname = 'testKey'
        self.sess[keyname] = "test"
        self.sess[keyname + '2'] = "test2"
        self.sess[3] = "test3"
        self.cookie_sess['cookie_test'] = "testing cookie values"
        if not 'viewCount' in self.sess:
            self.sess['viewCount'] = 1
        else:
            self.sess['viewCount'] = int(self.sess['viewCount']) + 1
        session_length = len(self.sess)
        self.memcacheStats = memcache.get_stats()
        template_values = {
            'sess': self.sess,
            'sess_str': str(self.sess),
            'cookie_sess': self.cookie_sess,
            'session_length': session_length,
            'memcacheStats': self.memcacheStats
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/session.html')
        self.response.out.write(template.render(path, template_values))

class CookieSessionPage(webapp.RequestHandler):
  def get(self):
    #TODO: Check to see if a datastore session exists, and reset
    # the session if so.
    self.sess = sessions.Session(writer="cookie")
    if self.request.get('deleteSession') == "true":
        self.sess.delete()
        print "Location: /session\n\n"
    elif self.request.get('setflash') == "true":
        self.sess['flash'] = 'You set a flash message! <a href="/session">Refresh this page</a> and this message is gone!'
        print "Location: /session\n\n"
    else:
        keyname = 'testKey'
        self.sess[keyname] = "test"
        self.sess[keyname + '2'] = "test2"
        self.sess[3] = "test3"
        if not 'viewCount' in self.sess:
            self.sess['viewCount'] = 1
        else:
            self.sess['viewCount'] = int(self.sess['viewCount']) + 1
        session_length = len(self.sess)
        self.memcacheStats = memcache.get_stats()
        template_values = {
            'sess': self.sess,
            'sess_str': str(self.sess),
            'session_length': session_length,
            'memcacheStats': self.memcacheStats
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/cookie_session.html')
        self.response.out.write(template.render(path, template_values))


class EventPage(webapp.RequestHandler):
  def __init__(self):
        self.msg = ""
        self.triggermsg = "I have not been triggered"

  def get(self):
    if self.request.get('trigger') == "true":
        AEU_Events.subscribe("myTriggeredEventFired", self.myTriggeredCallback, {"msg": "Triggered!"})
    AEU_Events.subscribe("myEventFired", self.myCallback, {"msg": "This message was set in myCallback."})
    AEU_Events.fire_event("myEventFired")
    AEU_Events.fire_event("myTriggeredEventFired")
    template_values = {
        'msg': self.msg,
        'triggermsg': self.triggermsg,
    }
    AEU_Events.subscribe("myEventFired", self.myCallback, {"msg": "You will never see this message because the event to set it is fired after the template_values have already been set."})
    AEU_Events.fire_event("myEventFired")
    path = os.path.join(os.path.dirname(__file__), 'templates/event.html')
    self.response.out.write(template.render(path, template_values))

  def myCallback(self, msg):
    self.msg = msg

  def myTriggeredCallback(self, msg):
    self.triggermsg = msg

class CachePage(webapp.RequestHandler):
  def get(self):
    self.cache = cache.Cache()
    # test deleting a cache object
    del self.cache["sampleStr"]
    # set a string
    if not "sampleStr" in self.cache:
        self.cache["sampleStr"] = "This is a string passed to the cache"
    # store an object
    if not "sampleObj" in self.cache:
        self.cache["sampleObj"] = ["this was set up as a list to test object caching"]
    keyname = 'dynamic' + 'key'
    if not keyname in self.cache:
        self.cache[keyname] = 'this is a dynamically created keyname'
    self.memcacheStats = memcache.get_stats()
    template_values = {
        'cacheItemStr': self.cache["sampleStr"],
        'cacheItemObj': self.cache["sampleObj"],
        'dynamickey': self.cache["dynamickey"],
        'memcacheStats': self.memcacheStats,
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/cache.html')
    self.response.out.write(template.render(path, template_values))


def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                       ('/session', SessionPage),
                                       ('/cookiesession', CookieSessionPage),
                                       ('/ajaxsession', AjaxSessionPage),
                                       ('/flash', FlashPage),
                                       ('/event', EventPage),
                                       ('/cache', CachePage)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
