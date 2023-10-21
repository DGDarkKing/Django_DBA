import json

from django import shortcuts as short
from django.db import connection
from django.http import HttpRequest
from django.views.decorators import http as http_decor

from base_operations.models import Columns
from utils import http_methods


@http_decor.require_GET
def select(request: HttpRequest, table_name: str):
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


@http_decor.require_GET
def get_insert_page(request: HttpRequest, table_name: str):
    columns = [col['column_name'] for col in Columns.get_columns(table_name)]
    pk_cols = [index[1]  for index in Columns.get_indexes(table_name) if index[2]]
    pk_index = [columns.index(pk_col) for pk_col in pk_cols]
    return short.render(
        request,
        'table_data/data/insert.html',
        context={
            'table_name': table_name,
            'columns': columns,
            'pk_cols': pk_cols,
            'pk_index': pk_index,
        }
    )

@http_decor.require_POST
def insert(request: HttpRequest, table_name: str):
    data = json.loads(request.POST['data'])
    cols = data['cols']
    data = data['data']
    cols = '(' + ', '.join(cols) + ')'
    res_data = []
    for row in data:
        row_data = '( '
        row_data += ', '.join([f'\'{value}\'' for value in row])
        row_data += " )"
        res_data.append(row_data)
    res_data = ', '.join(res_data)
    query = f'INSERT INTO "{table_name}" {cols} VALUES {res_data}'
    with connection.cursor() as cursor:
        cursor.execute(query)
    return short.redirect('select_data', table_name)


@http_decor.require_POST
def select_to_update(request: HttpRequest, table_name: str):
    pks = dict(request.POST)
    pks.pop('csrfmiddlewaretoken')
    condition = ' AND '.join([f'{key}=\'{value[0]}\'' for key, value in pks.items()])
    query = (
        f'SELECT * FROM "{table_name}" '
        f'  WHERE {condition}'
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
            'table_data/data/update.html',
            context={
                'table_name': table_name,
                'columns': columns,
                'data': data[0],
                'pk': pk,
                'pk_cols': pk_cols,
            }
        )


@http_decor.require_POST
def update(request: HttpRequest, table_name: str):
    data = json.loads(request.POST['data'])
    pk = data['pk']
    data = data['data']

    condition = ' AND '.join([f'{key}=\'{value[0]}\'' for key, value in pk.items()])
    data = ', '.join([f'{key}=\'{value}\'' if value != "" else f'{key}=NULL' for key, value in data.items()])
    query = f'UPDATE "{table_name}" SET {data} WHERE {condition}'
    with connection.cursor() as cursor:
        cursor.execute(query)
    return short.redirect('select_data', table_name)



@http_decor.require_POST
def delete(request: HttpRequest, table_name: str):
    pks = dict(request.POST)
    pks.pop('csrfmiddlewaretoken')
    condition = ' AND '.join([f'{key}=\'{value[0]}\'' for key, value in pks.items()])
    query = f'DELETE FROM "{table_name}" WHERE {condition}'
    with connection.cursor() as cursor:
        cursor.execute(query)
    return short.redirect('select_data', table_name)
