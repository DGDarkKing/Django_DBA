from django.urls import path, include

from advanced_operations import views

urlpatterns = [
    path('select_tables/', views.select_tables, name='start_select'),
    path('select_data/', views.select_data, name='select_data'),
    path('query/', views.create_query, name='query'),
    path('result/', views.repeat_query, name='repeat_query'),
]