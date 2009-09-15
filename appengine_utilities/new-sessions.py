# -*- coding: utf-8 -*-
"""
Copyright (c) 2008, appengine-utilities project
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the appengine-utilities project nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# main python imports
import os
import time
import datetime
import random
import md5
import Cookie
import pickle
import __main__
from time import strftime
import logging

#django simplejson import, used for flash
from django.utils import simplejson

# settings
try:
    import settings
except:
    import settings_default as settings

class Session(object):
    """
    Sessions used to maintain user presence between requests.

    Sessions are stored in the browser as cookies. A single cookie is used
    to store the data in key/value pairs. Once loaded this is available as a
    dictionary object you can read and write from.
    
    Data is stored by default in a json format, though an option to pickle the
    data is available. It's recommended to not store pickled data 
    as cookies however.
    
    The security of the file is protected by a checksum value stored in the
    object. The salt can either be configured on initialization of the
    Session object, or a global one can be stored in the settings. It's
    recommended to use a different salt for each user.
    """

    def __init__(self, cookie_name=settings.cookie["COOKIE_NAME"],
                cookie_path=settings.cookie["COOKIE_PATH"],
                session_expire_time=settings.cookie["SESSION_EXPIRE_TIME"],
                integrate_flash=settings.cookie["INTEGRATE_FLASH"],
                set_cookie_expires=settings.cookie["SET_COOKIE_EXPIRES"],
                ):
        """
        Initializer

        Args:
          cookie_name: The name for the session cookie stored in the browser.
          cookie_path: The path on the cookie
          session_expire_time: The amount of time between requests before the
              session expires.
          integrate_flash: If appengine-utilities flash utility should be
              integrated into the session object.
          set_cookie_expires: True adds an expires field to the cookie so
              it saves even if the browser is closed.
        """

        self.cookie_path = cookie_path
        self.cookie_name = cookie_name
        self.session_expire_time = session_expire_time
        self.integrate_flash = integrate_flash
        self.set_cookie_expires = set_cookie_expires

        # load the cookie
        string_cookie = os.environ.get(u"HTTP_COOKIE", u"")
        self.cookie = Cookie.SimpleCookie()
        self.output_cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)
        try:
            # TODO: Need to add the pickle support here
            self.cookie_vals = \
                simplejson.loads(self.cookie[self.cookie_name].value)
                # sync self.cache and self.cookie_vals which will make those
                # values available for all gets immediately.
            for k in self.cookie_vals:
                self.output_cookie[self.cookie_name] = self.cookie[self.cookie_name]
            # sync the input cookie with the output cookie
        except:
            self.cookie_vals = {}

        # Write the cookie back out to the browser
        # TODO: Add checksum here
        if self.set_cookie_expires:
            if not self.output_cookie.has_key(cookie_name):
                self.output_cookie[cookie_name] = u""
            self.output_cookie[cookie_name]["expires"] = \
                self.session_expire_time
        print self.output_cookie.output()

        # fire up a Flash object if integration is enabled
        if self.integrate_flash:
            import flash
            self.flash = flash.Flash(cookie=self.cookie)


    def delete(self):
        """
        stub
        """

    def __getitem__(self, keyname):
        """
        stub
        """

    def __setitem__(self, keyname, value):
        """
        stub
        """

    def __delitem__(self, keyname):
        """
        stub
        """
    def __len__(self):
        """
        stub
        """
    def __contains__(self, keyname):
        """
        stub
        """
    def __iter__(self):
        """
        stub
        """

    def delete_item(self, keyname, throw_exception=False):
        """
        stub
        """

