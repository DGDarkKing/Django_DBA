import json

from django.db import connection
from django.http import HttpRequest
from django import shortcuts as short
from django.views.decorators import http as http_decor

from advanced_operations.forms import TablesForm
from advanced_operations.models import Columns


# Create your views here.


@http_decor.require_GET
def select_tables(request: HttpRequest):
    form = TablesForm()
    return short.render(
        request,
        'select_work/index.html',
        context={
            'form': form,
        }
    )


@http_decor.require_POST
def select_data(request: HttpRequest):
    form = TablesForm(request.POST)
    form.is_valid()
    tables = form.cleaned_data['tables']
    tables = {table_name: Columns.get_column_name(table_name) for table_name in tables}
    with connection.cursor() as cursor:
        cursor.execute('SELECT aggfnoid FROM pg_aggregate GROUP BY aggfnoid')
        aggregation_functions = cursor.fetchall()
    aggregation_functions = {
        agg_func_fullname[0]
            if '.' not in agg_func_fullname[0]
            else agg_func_fullname[0][agg_func_fullname[0].find('.')+1:]
        for agg_func_fullname in aggregation_functions
    }
    return short.render(
        request,
        'select_work/select_data.html',
        context={
            'tables': tables,
            'aggregation_funcs': aggregation_functions
        }
    )


@http_decor.require_POST
def create_query(request: HttpRequest):
    data = json.loads(request.POST['data'])

    tables = []
    for i, table_data in enumerate(data):
        table_name = table_data['tableName']
        table_name_alias = f'T{i}'
        table_name = f'public."{table_name}" AS {table_name_alias}'
        tables.append(table_name)
        table_data['tableName'] = table_name_alias
    query = f'FROM {tables[0]}'
    if len(tables) > 1:
        tables = "\n".join([f'JOIN {table}\n\tON !!!' for table in tables[1:]])
        query = f'{query}\n{tables}'

    select = []
    aggregation_select = []
    where = []
    group_by = []
    having = []
    for table in data:
        table_name = table['tableName']

        for aggregation in [row for row in table['rows'] if row['aggregationFunc']]:
            aggregate = f'{aggregation["aggregationFunc"]}({table_name}.{aggregation["columnName"]})'
            aggregation_select.append(aggregate)
            if aggregation['condition']:
                having.append(aggregation['condition'].format(aggregate))

        simple = [row for row in table['rows'] if row['isSelect'] and not row['aggregationFunc']]
        for col in simple:
            col_name = f'{table_name}.{col["columnName"]}'
            if col['condition']:
                where.append(col['condition'].format(col_name))

            if col['expressionSelect']:
                select.append(col['expressionSelect'].format(col_name))
            else:
                select.append(col_name)

    aliases = [f'Col{i}' for i in range(len(select))]
    if aggregation_select:
        group_by.extend(aliases)

    select = [f'{col} AS {alias}' for col, alias in zip(select, aliases)]
    select.extend([f'{agg_col} AS Col{i}' for i, agg_col in enumerate(aggregation_select, len(select))])

    query = (f'SELECT {", ".join(select)}\n'
             f'\t{query}')
    if where:
        query = f'{query}\n\tWHERE {" AND ".join(where)}'
    if group_by:
        query = f'{query}\n\tGROUP BY {", ".join(group_by)}'
    if having:
        query = f'{query}\n\tHAVING {" AND ".join(having)}'

    return short.render(
        request,
        'select_work/query.html',
        context={
            'query': query,
        }
    )

@http_decor.require_POST
def repeat_query(request: HttpRequest):
    query = request.POST['query']

    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    return short.render(
        request,
        'data.html',
        context={
            'query': query,
            'columns': columns,
            'data': data,
        }
    )