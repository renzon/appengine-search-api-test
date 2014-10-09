# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import search
from google.appengine.api.search import SortExpression

user_index = search.Index('userIndex')


def save_user_doc(main_user):
    fields = [search.AtomField('email', main_user.email),
              search.TextField('name', main_user.name),
              search.DateField('creation', main_user.creation)]
    fields.extend([search.AtomField('group', group) for group in main_user.groups])
    doc = search.Document(doc_id=unicode(main_user.key.id()),
                          fields=fields)
    user_index.put(doc)
    return doc


def get_or_create_user_document(main_user):
    doc = user_index.get(unicode(main_user.key.id()))
    if doc is None:
        doc = save_user_doc(main_user)
    return doc


def search_user(name, admin=False):
    query_str = 'name = %s' % name if not admin else 'name = %s AND group: ADMIN' % name
    # Build the SortOptions with 2 sort keys
    sort1 = search.SortExpression(expression='name', direction=SortExpression.ASCENDING)
    sort_opts = search.SortOptions(expressions=[sort1])

    # Build the QueryOptions
    # Create a FieldExpression
    expr2 = search.FieldExpression(name='name_snippet', expression='snippet("%s", name, 20)'%name)
    options=search.QueryOptions(sort_options=sort_opts,returned_expressions=[expr2])
    query=search.Query(query_str,options)
    return user_index.search(query)
