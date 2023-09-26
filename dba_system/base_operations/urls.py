from django.urls import path

from base_operations.views.main import get_details
from base_operations.views import structure as structure_views

urlpatterns = [
    path("<str:table_name>/", get_details, name="table_detail"),

    path("structure/<str:table_name>/", structure_views.get_structure, name="table_structure"),
    path("structure/<str:table_name>/add/", structure_views.get_add_field_form, name="add_field_form"),
    path("structure/<str:table_name>/add/", structure_views.add_field, name="add_field"),
    path("structure/<str:table_name>/change/<str:field>/", structure_views.get_change_field_form, name="change_field_form"),
    path("structure/<str:table_name>/change/", structure_views.change_field, name="change_field"),
    path("structure/<str:table_name>/delete/", structure_views.delete_field, name="delete_field"),

]
