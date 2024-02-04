from django.urls import path, include

from advanced_operations.views import select as select_view
from advanced_operations.views import pivot as pivot_view

urlpatterns = [
    path('select_tables/', select_view.select_tables, name='start_select'),
    path('select_data/', select_view.select_data, name='select_data'),
    path('query/', select_view.create_query, name='query'),
    path('result/', select_view.repeat_query, name='repeat_query'),
    path('pivot/start/', pivot_view.input_pivot_data, name='pivot'),
    path('pivot/query', pivot_view.create_pivot_query, name='pivot_query'),
]