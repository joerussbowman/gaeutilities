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

import time
from google.appengine.ext import db
from django.utils import simplejson


class ROTModel(db.Model):
    """
    ROTModel overrides the db.Model functions, retying each method each time
    a timeout exception is raised.

    Also adds a to_json() method, to compliment to_xml()
    """

    @classmethod
    def _run_query(cls, method, retries=3, *args, **kwargs):
        count = 0
        while count < retries:
            try:
                return method(*args, **kwargs)
            except db.Timeout:
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()


    @classmethod
    def get(cls, *args, **kwargs):
        return cls._run_query(db.Model.get, args, kwargs)
        pass

    @classmethod
    def get_by_id(cls, *args, **kwargs):
        return cls._run_query(db.Model.get_by_id, args, kwargs)
        pass

    @classmethod
    def get_by_key_name(cls, *args, **kwargs):
        return cls._run_query(db.Model.get_by_key_name, args, kwargs)
        pass

    @classmethod
    def get_or_insert(cls, *args, **kwargs):
        return cls._run_query(db.Model.get_or_insert, args, kwargs)
        pass

    @classmethod
    def all(cls):
        return cls._run_query(db.Model.all)
        pass

    @classmethod
    def gql(cls, *args, **kwargs):
        return cls._run_query(db.Model.gql, args, kwargs)
        pass

    @classmethod
    def kind(cls):
        return cls._run_query(db.Model.kind)
        pass

    @classmethod
    def properties(cls):
        return cls._run_query(db.Model.properties)
        pass

    def put(self):
        return self._run_query(db.Model.put, self, args, kwargs)

    def key(self):
        return self._run_query(db.Model.key, self, args, kwargs)
        pass

    def delete(self):
        return self._run_query(db.Model.delete, self, args, kwargs)
        pass

    def is_saved(self):
        return self._run_query(db.Model.is_saved, self, args, kwargs)
        pass

    def parent(self):
        return self._run_query(db.Model.parent, self, args, kwargs)
        pass

    def parent_key(self):
        return self._run_query(db.Model.parent_key, self, args, kwargs)
        pass

    def to_xml(self):
        return self._run_query(db.Model.to_xml, self, args, kwargs)
        pass

    '''
    def to_json(self):
        """
        Extra method added to return a model as json. Since to_xml is there
        and simplejson exists in appengine, why not?
        """
        # stub
        pass
    '''
