'''
Copyright (c) 2008, appengine-utilities project
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the appengine-utilities project nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import os
import __main__
import time
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from appengine_utilities import sessions
from appengine_utilities import flash
from appengine_utilities import event
from appengine_utilities import cache
from appengine_utilities.rotmodel import ROTModel
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext import db
from django.utils import simplejson

class MainPage(webapp.RequestHandler):
  def __init__(self):
    self.test = "event not fired"

  def get(self):
    template_values = {}

    path = os.path.join(os.path.dirname(__file__), 'templates/index-new.html')
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
        path = os.path.join(os.path.dirname(__file__), 'templates/flash-new.html')
        self.response.out.write(template.render(path, template_values))

class AjaxSessionPage(webapp.RequestHandler):
  def get(self):
    self.sess = sessions.Session()
    if not 'viewCount' in self.sess:
      self.sess['viewCount'] = 1
    else:
      self.sess['viewCount'] = int(self.sess['viewCount']) + 1
    self.response.out.write('viewcount is ' + str(self.sess['viewCount']))

class SessionTestModel(db.Model):
    testval = db.StringProperty()

class SessionPage(webapp.RequestHandler):
  def get(self):
    self.sess = sessions.Session()
    if not self.sess.has_key("model_test"):
        self.sess["model_test"] = SessionTestModel(testval="test")
        self.sess["model_test"].put()
        # give the datastore time to submit the commit
        time.sleep(1)
    self.cookie_sess = sessions.Session(writer="cookie")
    if self.request.get('deleteSession') == "true":
        self.sess.delete()
        print "Location: /session\n\n"
    elif self.request.get('setflash') == "true":
        self.sess['flash'] = 'You set a flash message! <a href="/session">Refresh this page</a> and this message is gone!'
        print "Location: /session\n\n"
    elif self.request.get('setTestKey') == "true":
        self.sess['DeletableKey'] = 'delete me'
        print "Location: /session\n\n"
    elif self.request.get('clearTestKey') == "true":
        self.sess.delete_item('DeletableKey')
        print "Location: /session\n\n"
    else:
        keyname = 'testKey'
        self.sess[keyname] = "test"
        self.sess[keyname + '2'] = "test2"
        self.sess[3] = "test3"
        self.cookie_sess['cookie_test'] = "testing cookie values"
        self.sess[u"unicode_key"] = u"unicode_value"

        if not 'viewCount' in self.sess:
            self.sess['viewCount'] = 1
        else:
            self.sess['viewCount'] = int(self.sess['viewCount']) + 1
        self.sess["model_test"].testval = unicode(self.sess['viewCount'])
        testkey = self.sess["model_test"].put()
        session_length = len(self.sess)
        self.memcacheStats = memcache.get_stats()
        template_values = {
            'sess': self.sess,
            'sess_str': str(self.sess),
            'cookie_sess': self.cookie_sess,
            'session_length': session_length,
            'memcacheStats': self.memcacheStats,
            'model_test': self.sess["model_test"].testval,
            'testkey': testkey,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/session-new.html')
        self.response.out.write(template.render(path, template_values))

class CookieSessionPage(webapp.RequestHandler):
  def get(self):
    self.sess = sessions.Session(writer="cookie")
    if self.request.get('deleteSession') == "true":
        self.sess.delete()
        print "Location: /cookiesession\n\n"
    elif self.request.get('setflash') == "true":
        self.sess['flash'] = 'You set a flash message! <a href="/cookiesession">Refresh this page</a> and this message is gone!'
        print "Location: /cookiesession\n\n"
    else:
        keyname = 'testKey'
        self.sess[keyname] = "test"
        self.sess[keyname + '2'] = "test2"
        self.sess[3] = "test3"
        if not 'viewCount' in self.sess:
            self.sess['viewCount'] = 1
        else:
            self.sess['viewCount'] = int(self.sess['viewCount']) + 1
        self.sess[u"unicode_key"] = u"unicode_value"
        session_length = len(self.sess)
        self.memcacheStats = memcache.get_stats()
        template_values = {
            'sess': self.sess,
            'sess_str': str(self.sess),
            'session_length': session_length,
            'memcacheStats': self.memcacheStats
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/cookie_session-new.html')
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
    path = os.path.join(os.path.dirname(__file__), 'templates/event-new.html')
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
    path = os.path.join(os.path.dirname(__file__), 'templates/cache-new.html')
    self.response.out.write(template.render(path, template_values))


class TestROTModel(ROTModel):
    testval = db.IntegerProperty()

class ROTModelPage(webapp.RequestHandler):
  def get(self):
      template_values = {}

      # create a model test
      model1 = TestROTModel(key_name="testmodel1", testval=1)
      if model1:
          template_values["modelcreate"] = "OK"
      else:
          template_values["modelcreate"] = "ERROR"

      # is_saved test 1
      if model1.is_saved() is False:
          template_values["savedtest1"] = "OK"
      else:
          template_values["savedtest1"] = "ERROR"

      # model put test
      model_key = model1.put()
      if model_key:
          template_values["puttest"] = "OK"
      else:
          template_values["puttest"] = "ERROR"

      # is_saved test 2
      if model1.is_saved() == True:
          template_values["savedtest2"] = "OK"
      else:
          template_values["savedtest2"] = "ERROR"

      # get test single
      singletest = TestROTModel.get(model_key)
      if singletest:
          template_values["singleget"] = "OK"
      else:
          template_values["singleget"] = "ERROR"

      # get_or_insert test
      model2 = TestROTModel.get_or_insert("testmodel2", parent=model1, testval=2)
      if model2:
          template_values["get_or_insert"] = "OK"
          model2_key = model2.put()
      else:
          template_values["get_or_insert"] = "ERROR"

      # get test multi
      multitest = TestROTModel.get([model_key, model2_key])
      if len(multitest) > 1:
          template_values["multiget"] = "OK"
      else:
          template_values["multiget"] = "ERROR"

      # key test
      model2_key = model2.key()
      if model2_key:
          template_values["keytest"] = "OK"
      else:
          template_values["keytest"] = "ERROR"

      # set strings for key names
      model_keyname = "testmodel1"
      model2_keyname = "testmodel2"

      # get_by_key_name single
      singlekeyname = TestROTModel.get_by_key_name(model_keyname)
      if singlekeyname:
          template_values["getbykeynamesingle"] = "OK"
      else:
          template_values["getbykeynamesingle"] = "ERROR"

      # get_by_key_name multi
      multikeyname = TestROTModel.get_by_key_name([model_keyname, model2_keyname])
      if multikeyname:
          template_values["getbykeynamemulti"] = "OK"
      else:
          template_values["getbykeynamemulti"] = "ERROR"

      # all test
      alltest = TestROTModel.all()
      results = alltest.fetch(20)
      if len(results) > 0:
          template_values["alltest"] = "OK"
      else:
          template_values["alltest"] = "ERROR"

      # gql test
      gqltest = TestROTModel.gql("WHERE testval = :1", 1)
      results = gqltest.fetch(20)
      if len(results) > 0:
          template_values["gqltest"] = "OK"
      else:
          template_values["gqltest"] = "ERROR"

      # parent test
      parenttest = model2.parent()
      if parenttest:
          template_values["parenttest"] = "OK"
      else:
          template_values["parenttest"] = "ERROR"

      # parent_key test
      parentkeytest = model2.parent_key()
      if parentkeytest == model_key:
          template_values["parentkeytest"] = "OK"
      else:
          template_values["parentkeytest"] = "ERROR"

      # delete test
      model1.delete()
      model2.delete()

      if TestROTModel.get(model_key) == None:
          template_values["deletetest"] = "OK"
      else:
          template_values["deletetest"] = "ERROR"


      path = os.path.join(os.path.dirname(__file__), 'templates/rotmodel-new.html')
      self.response.out.write(template.render(path, template_values))


class PageTestModel(db.Model):
    testval = db.IntegerProperty()

class PaginatorPage(webapp.RequestHandler):
  def get(self):
        template_values = {}

        query = PageTestModel.all()
        results = query.fetch(20)
        if len(results) < 20:
            for i in range(0, 20):
                model = PageTestModel(testval=i)
                model.put()
            time.sleep(1)

        
        page1 = Paginator.get(model=PageTestModel, count=10)
        page2 = Paginator.get(model=PageTestModel, count=10, start=page1["next"])

        template_values["page1"] = page1
        template_values["page2"] = page2
        template_values["page_1_results"] = page1["results"]
        template_values["page_1_previous"] = page1["previous"]
        template_values["page_1_next"] = page1["next"]
        template_values["page_2_results"] = page2["results"]
        template_values["page_2_previous"] = page2["previous"]
        template_values["page_2_next"] = page2["next"]

        path = os.path.join(os.path.dirname(__file__), 'templates/paginator.html')
        self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                       ('/session', SessionPage),
                                       ('/cookiesession', CookieSessionPage),
                                       ('/ajaxsession', AjaxSessionPage),
                                       ('/flash', FlashPage),
                                       ('/event', EventPage),
                                       ('/cache', CachePage),
                                       ('/paginator', PaginatorPage),
                                       ('/rotmodel', ROTModelPage)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
