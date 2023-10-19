from dataclasses import asdict

from django import http
from django import shortcuts as short
from django.views.decorators import http as http_decor

from base_operations.dtos import ColumnDataDto
from base_operations.forms import ColumnDataForm
from base_operations.models import Columns
from utils import http_methods


@http_decor.require_GET
def get_structure(request, table_name):
    fields = Columns.get_columns(table_name).order_by("ordinal_position")
    return short.render(
        request,
        'table_data/index.html',
        context={
            'context_data': 'structure',
            'table_name': table_name,
            'fields': fields
        }
    )


@http_decor.require_http_methods([http_methods.GET, http_methods.POST])
def add_field(request, table_name):
    result = None
    if request.method == http_methods.POST:
        target_form = ColumnDataForm(request.POST)
        if target_form.is_valid():
            data = target_form.cleaned_data
            Columns.add_column(table_name, ColumnDataDto(**data))
            result = short.redirect('table_detail', table_name)
    else:
        target_form = ColumnDataForm()
        result = short.render(
            request,
            'table_data/columns/add_field.html',
            context={
                'form': target_form,
                'table_name': table_name
            }
        )

    return result


@http_decor.require_http_methods([http_methods.GET, http_methods.POST])
def change_field(request, table_name, field):
    result = None
    if request.method == http_methods.POST:
        target_form = ColumnDataForm(request.POST)
        if target_form.is_valid():
            Columns.change_field(table_name, field, ColumnDataDto(**target_form.cleaned_data))
            result = short.redirect('table_detail', table_name)
    else:
        column_data = Columns.get_column_data(table_name, field)
        if not column_data.default_value:
            column_data.default_value = ''
        target_form = ColumnDataForm(asdict(column_data))
        result = short.render(
            request,
            'table_data/columns/change_field.html',
            context={
                'form': target_form,
                'table_name': table_name,
                'field': field,
            }
        )

    return result


@http_decor.require_GET
def delete_field(request, table_name, field):
    Columns.delete_column(table_name, field)
    return short.redirect('table_detail', table_name)
