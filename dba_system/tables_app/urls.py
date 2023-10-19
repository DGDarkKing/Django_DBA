from django.urls import path

from tables_app.views import get_tables, add_table, delete_table

urlpatterns = [
    path("", get_tables, name='home'),
    path('add/', add_table, name='add_table'),
    path('delete/<str:table_name>/', delete_table, name='delete_table'),
]