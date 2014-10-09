# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from search_indexes import search_user


@login_not_required
@no_csrf
def index(name='Renzo', group='false'):
    if group:
        group = group == 'true'
    result = search_user(name, group)
    context = {'name': name, 'group': group, 'doc_search': result}
    return TemplateResponse(context)

