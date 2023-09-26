from django import shortcuts as short
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators import http as http_decor

from tables_app.forms import CreateTableForm
from tables_app.models import Tables


# Create your views here.


@http_decor.require_GET
def get_tables(request: WSGIRequest):
    tables = Tables.get_table_names()
    return short.render(
        request,
        'index.html',
        context={
            'tables': tables
        }
    )


def add_table(request: WSGIRequest):
    result = None
    if request.method == 'POST':
        create_table_form = CreateTableForm(request.POST)
        if create_table_form.is_valid():
            Tables.create_table(create_table_form.cleaned_data['table_name'])
            result = short.redirect('home')
    else:
        create_table_form = CreateTableForm()

    if not result:
        result = short.render(
            request,
            'add_table.html',
            context={
                'form': create_table_form,
            }
        )

    return result


@http_decor.require_GET
def delete_table(request: WSGIRequest, table_name: str):
    Tables.delete_table(table_name)
    return short.redirect('home')
