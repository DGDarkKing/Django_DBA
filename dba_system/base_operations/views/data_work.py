from django import shortcuts as short
from django.db import connection
from django.http import HttpRequest
from django.views.decorators import http as http_decor

from base_operations.models import Columns
from utils import http_methods


@http_decor.require_GET
def select(request: HttpRequest, table_name: str):
    table_name.strip()
    query = (
        f'SELECT * FROM "{table_name}" '
    )
    pk = [index[1] for index in Columns.get_indexes(table_name) if index[2]]
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        pk_cols = None
        if pk:
            pk = [columns.index(name) for name in pk]
            pk_cols = [columns[index] for index in pk]
        return short.render(
            request,
            'table_data/data/index.html',
            context={
                'context_data': 'data_work',
                'table_name': table_name,
                'columns': columns,
                'data': data,
                'pk': pk,
                'pk_cols': pk_cols,
            }
        )


@http_decor.require_http_methods([http_methods.GET, http_methods.POST])
def insert(request: HttpRequest, table_name: str):
    ...


@http_decor.require_POST
def select_to_update(request: HttpRequest, table_name: str):
    pks = dict(request.POST)
    pks.pop('csrfmiddlewaretoken')
    condition = ' AND '.join([f'{key}={value[0]}' for key, value in pks.items()])


@http_decor.require_POST
def delete(request: HttpRequest, table_name: str):
    pks = dict(request.POST)
    pks.pop('csrfmiddlewaretoken')
    condition = ' AND '.join([f'{key}={value[0]}' for key, value in pks.items()])
    query = f'DELETE FROM "{table_name}" WHERE {condition}'
    with connection.cursor() as cursor:
        cursor.execute(query)
    return short.redirect('select_data', table_name)
