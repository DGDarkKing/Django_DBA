from itertools import groupby

from django import shortcuts as short
from django.views.decorators import http as http_decor

from base_operations.dtos import PkDto, IndexDto
from base_operations.forms import PrimaryKeyDataForm, IndexDataForm
from base_operations.models import Columns
from utils import http_methods


@http_decor.require_GET
def get_keys(request, table_name):
    indexes = Columns.get_indexes(table_name)
    pk_list = [el for el in indexes if el[2]]
    pk = [
        PkDto(k, [row[1] for row in g])
        for k, g in groupby(pk_list, lambda x: x[0])
    ]
    indexes_list = [el for el in indexes if not el[2]]
    indexes = []
    for k, g in groupby(indexes_list, lambda x: x[0]):
        res = list(g)
        indexes.append(IndexDto(k, [row[1] for row in res], res[0][3]))

    return short.render(
        request,
        'table_data/keys/index.html',
        context={
            'context_data': 'keys',
            'table_name': table_name,
            'pk': pk,
            'indexes': indexes,
        }
    )


@http_decor.require_http_methods([http_methods.GET, http_methods.POST])
def add_primary_key(request, table_name):
    result = None
    form = None
    if request.method == http_methods.POST:
        form = PrimaryKeyDataForm(request.POST, table_name=table_name)
        if form.is_valid():
            Columns.add_pk(table_name, form.cleaned_data['name'], form.cleaned_data['columns'])
            result = short.redirect('keys', table_name)
    else:
        form = PrimaryKeyDataForm(table_name=table_name)
        result = short.render(
            request,
            'table_data/keys/index_work.html',
            context={
                'context_data': 'pk',
                'table_name': table_name,
                'form': form,
            }
        )

    return result


@http_decor.require_GET
def delete_primary_key(request, table_name, pk_name):
    Columns.delete_pk(table_name, pk_name)
    return short.redirect('keys', table_name)


@http_decor.require_http_methods([http_methods.GET, http_methods.POST])
def add_index(request, table_name):
    result = None
    form = None
    if request.method == http_methods.POST:
        form = IndexDataForm(request.POST, table_name=table_name)
        if form.is_valid():
            Columns.add_index(table_name, form.cleaned_data['name'], form.cleaned_data['is_unique'],
                              form.cleaned_data['columns'])
            result = short.redirect('keys', table_name)
    else:
        form = IndexDataForm(table_name=table_name)
        result = short.render(
            request,
            'table_data/keys/index_work.html',
            context={
                'context_data': 'index',
                'table_name': table_name,
                'form': form,
            }
        )

    return result


@http_decor.require_GET
def delete_index(request, table_name, index_name):
    Columns.delete_index(index_name)
    return short.redirect('keys', table_name)
