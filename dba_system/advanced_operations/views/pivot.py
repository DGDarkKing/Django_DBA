from django.db import connection
from django.http import HttpRequest
from django import shortcuts as short
from django.views.decorators import http as http_decor


@http_decor.require_GET
def input_pivot_data(
        request: HttpRequest
):
    return short.render(
        request,
        'pivot/index.html',
    )


"""
select t.prod,
       sum(case when t.supp = 'A' then t.num end) as "A",
       sum(case when t.supp = 'B' then t.num end) as "B",
       sum(t.num) as total_sum
from transactions t
group by rollup(t.prod);
"""

@http_decor.require_POST
def create_pivot_query(
        request: HttpRequest
):
    source_query: str = request.POST['query']
    table = source_query
    if not source_query.lower().strip().startswith('select'):
        table = f'public."{table}"'
        source_query = f'SELECT * FROM {table}'
    else:
        table = f'({table})'
    table = f'{table} t'
    column_x, column_y = request.POST['x'], request.POST['y']

    with connection.cursor() as cursor:
        cursor.execute(f'SELECT DISTINCT {column_x} FROM {table}')
        pivot_columns = cursor.fetchall()
    if request.POST['sort_x'] == 'on':
        pivot_columns = sorted(pivot_columns, key=lambda x: x[0])

    result_query = f'SELECT t.{column_y},\n'
    pivot_data = []
    func = request.POST['func']
    target_field = request.POST['target_field']
    for colm in pivot_columns:
        q = f'\t{func}(case when t.{column_x} = \'{colm[0]}\' then t.{target_field} end) as "{colm[0]}",\n'
        pivot_data.append(q)
    result_query = (f'{result_query}{"".join(pivot_data)}'
                    f'\t{func}(t.{target_field}) as "TOTAL"\n'
                    f'FROM {table}\nGROUP BY ROLLUP(t.{column_y})')
    if request.POST['sort_y'] == 'on':
        result_query = f'{result_query}\nORDER BY t.{column_y}'

    return short.render(
        request,
        'pivot/query.html',
        context={
            'query': result_query
        }
    )

