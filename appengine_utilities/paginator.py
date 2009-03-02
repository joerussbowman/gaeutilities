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

from google.appengine.ext import db
from cache import Cache

class Paginator(object):
    """
    This class is used for maintaining pagination objects.
    """

    @classmethod
    def get(cls, count=10, q_filter_attr=None, q_filter="", start=None, model=None, \
            order='DESC', order_by='__key__'):
        """
        get queries the database on model, starting with key, ordered by
        order. It receives count + 1 items, returning count and setting a
        next field to the count + 1 item key. It then reverses the sort, and
        grabs count objects, returning the last as a the previous.

        Arguments:
            count:         The amount of entries to pull on query
            q_filter_attr: The attribute to filter on (optional)
            q_filter:      The filter value (optional)
            start:         The key to start the page from
            model:         The Model object to query against. This is not a
                           string, it must be a Model derived object.
            order:         The order in which to pull the values.
            order_by:      The attribute to order results by. This defaults to
                           __key__

        Returns a dict:
        {
            'next': next_key,
            'prev': prev_key,
            'items': entities_pulled
        }
        """

        # argument validation
        if model == None:
            raise ValueError('You must pass a model to query')

        if not model.gql:
            raise TypeError('model must be a valid model object.')

        # cache check
        c = cache.Cache()
        if c['gae_paginator_' + q_filter + "_index"]:
            return c['gae_paginator_' + q_filter + "_index"]

        # query
        