from django.urls import path

from ui_operations.views import get_tables, add_table, delete_table

urlpatterns = [
    path("", get_tables, name='home'),
    path('add/', add_table, name='add_table'),
    path('add_form/<str:table_name>/', delete_table, name='delete_table'),
]