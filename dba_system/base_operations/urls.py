from django.urls import path, include

from base_operations.views import data_work
from base_operations.views.main import get_details
from base_operations.views import structure as structure_views, keys

urls_structure = [
    path("", structure_views.get_structure, name="table_structure"),
    path("add/", structure_views.add_field, name="add_field"),
    path("change/<str:field>/", structure_views.change_field, name="change_field"),
    path("delete/<str:field>", structure_views.delete_field, name="delete_field"),
]

keys_urls = [
    path('', keys.get_keys, name='keys'),
    path('primary_key/add/', keys.add_primary_key, name='add_pk'),
    path('primary_key/delete/<str:pk_name>/', keys.delete_primary_key, name='delete_pk'),
    path('index/add/', keys.add_index, name='add_index'),
    path('index/delete/<str:index_name>/', keys.delete_index, name='delete_index'),

]

data_work_urls = [
    path('', data_work.select, name='select_data'),
    path('insert_data/', data_work.get_insert_page, name='insert_data'),
    path('insert/', data_work.insert, name='insert'),
    path('update_data/', data_work.select_to_update, name='update_data'),
    path('update/', data_work.update, name='update'),
    path('delete/', data_work.delete, name='delete_data'),

]

urlpatterns = [
    path('<str:table_name>/', get_details, name="table_detail"),
    path('structure/<str:table_name>/', include(urls_structure)),
    path('keys/<str:table_name>/', include(keys_urls)),
    path('data_work/<str:table_name>/', include(data_work_urls))
]
