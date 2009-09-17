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

class ROTModel(db.Model):
    """
    ROTModel overrides the db.Model functions, retying each method each time
    a timeout exception is raised.
    """

    @classmethod
    def get(cls, keys):
        count = 0
        while count < 3:
            try:
                return db.Model.get(keys)
            except db.Timeout():
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()

    @classmethod
    def get_by_id(cls, ids, parent=None):
        count = 0
        while count < 3:
            try:
                return db.Model.get_by_id(ids, parent)
            except db.Timeout():
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()

    # TODO: this isn't working
    #@classmethod
    #def get_by_key_name(cls, key_names, parent=None):
    #    count = 0
    #    while count < 3:
    #        try:
    #            return db.Model.get_by_key_name(key_names, parent)
    #        except db.Timeout():
    #            count += 1
    #            time.sleep(count)
    #    else:
    #        raise db.Timeout()

    # TODO: This isn't working for some reason when specifying a parent
    # It's creating an entity of kind Model, rather than the model kind
    # it should be
    #@classmethod
    #def get_or_insert(cls, key_name, **kwargs):
    #    count = 0
    #    while count < 3:
    #        try:
    #            return db.Model.get_or_insert(key_name, **kwargs)
    #        except db.Timeout():
    #            count += 1
    #            time.sleep(count)
    #    else:
    #        raise db.Timeout()

    def put(self):
        count = 0
        while count < 3:
            try:
                return db.Model.put(self)
            except db.Timeout():
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()

    def key(self):
        count = 0
        while count < 3:
            try:
                return db.Model.key(self)
            except db.Timeout():
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()

    def delete(self):
        count = 0
        while count < 3:
            try:
                return db.Model.delete(self)
            except db.Timeout():
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()

    def is_saved(self):
        count = 0
        while count < 3:
            try:
                return db.Model.is_saved(self)
            except db.Timeout():
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()
        pass

    def parent(self):
        count = 0
        while count < 3:
            try:
                return db.Model.parent(self)
            except db.Timeout():
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()
        pass

    def parent_key(self):
        count = 0
        while count < 3:
            try:
                return db.Model.parent_key(self)
            except db.Timeout():
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()
        pass

    def to_xml(self):
        count = 0
        while count < 3:
            try:
                return db.Model.to_xml(self)
            except db.Timeout():
                count += 1
                time.sleep(count)
        else:
            raise db.Timeout()
        pass

