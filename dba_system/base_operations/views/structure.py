from django import http
from django import shortcuts as short
from django.views.decorators import http as http_decor

from base_operations.models import Columns


@http_decor.require_GET
def get_structure(request, table_name):
    fields = Columns.get_fields(table_name).order_by("ordinal_position")
    return short.render(
        request,
        'table_data/index.html',
        context={
            'context_data': 'structure',
            'table_name': table_name,
            'fields': fields
        }
    )


@http_decor.require_GET
def get_add_field_form(request, table_name):
    return http.HttpResponseBadRequest('Получение Формы создания столбца'
                                       f'\nTbale: {table_name}')


@http_decor.require_POST
def add_field(request, table_name):
    return http.HttpResponseBadRequest('Создание столбца'
                                       f'\nTbale: {table_name}')


@http_decor.require_GET
def get_change_field_form(request, table_name, field):
    return http.HttpResponseBadRequest('Получение Формы изменения столбца'
                                       f'\nTbale: {table_name} field: {field}')


@http_decor.require_POST
def change_field(request, table_name):
    return http.HttpResponseBadRequest('Изменение столбца'
                                       f'\nTbale: {table_name}')


@http_decor.require_GET
def delete_field(request, table_name, field):
    return http.HttpResponseBadRequest('Удаление столбца'
                                       f'\nTbale: {table_name} field: {field}')
